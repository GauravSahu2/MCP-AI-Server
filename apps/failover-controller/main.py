# apps/failover-controller/main.py
import asyncio
import httpx
import os

REGIONS = {
    "primary":   os.getenv("PRIMARY_API_URL", "https://aws.aegis.ai"),
    "secondary": os.getenv("SECONDARY_API_URL", "https://oci.aegis.ai"),
}

class FailoverController:
    def __init__(self):
        self.current_active = "primary"
        self.health_history = {"primary": True, "secondary": True}

    async def check_health(self, name, url):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{url}/health")
                return resp.status_code == 200
        except Exception:
            return False

    async def run(self):
        print(f"Sovereign Failover Controller started. Active Region: {self.current_active}")
        while True:
            primary_healthy = await self.check_health("primary", REGIONS["primary"])
            
            if not primary_healthy and self.current_active == "primary":
                print("CRITICAL: Primary Region (AWS) is DOWN. Initiating failover to Oracle...")
                self.current_active = "secondary"
                await self.trigger_failover("secondary")
            
            elif primary_healthy and self.current_active == "secondary":
                print("RECOVERY: Primary Region (AWS) is healthy. Failing back...")
                self.current_active = "primary"
                await self.trigger_failover("primary")

            await asyncio.sleep(30)

    async def trigger_failover(self, target):
        # In production, this would call Cloudflare/AWS Route53 API to update DNS
        # Or update Istio Gateway to shift traffic
        print(f"Global Traffic Shifted to: {target}")

if __name__ == "__main__":
    controller = FailoverController()
    asyncio.run(controller.run())
