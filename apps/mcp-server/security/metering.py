# apps/mcp-server/security/metering.py
import tiktoken

class CostMeter:
    def __init__(self):
        # Default to cl100k_base (GPT-4 / Claude-3 tokenizer equivalent for estimation)
        try:
            self.encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.encoder = None

    def estimate_tokens(self, text: str) -> int:
        if not self.encoder:
            # Fallback to word-count based estimation (rough)
            return len(text.split()) * 1.3
        return len(self.encoder.encode(text))

    def calculate_cost(self, tokens: int, rate_per_1k=0.002):
        return (tokens / 1000) * rate_per_1k

cost_meter = CostMeter()
