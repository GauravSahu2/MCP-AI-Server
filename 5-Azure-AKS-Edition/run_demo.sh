#!/bin/bash
echo "=============================================================="
echo "  High-Assurance AI Architecture | Interactive Demo Launcher"
echo "=============================================================="
echo ""
echo "Launching the multi-cloud portfolio locally via Docker Compose..."
echo ""

docker compose up -d --build

echo ""
echo "Waiting for the backend microservices to stabilize (15s)..."
sleep 15

echo ""
echo "Booting Next.js Dashboard!"

# Open browser based on OS capability
if command -v xdg-open > /dev/null; then
  xdg-open http://localhost:3000
elif command -v open > /dev/null; then
  open http://localhost:3000
else
  echo "Please open your browser to http://localhost:3000"
fi

echo ""
echo "Demo is running in the background. To stop the environment later, run:"
echo "$ docker compose down"
