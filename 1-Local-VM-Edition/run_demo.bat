@echo off
echo ==============================================================
echo   High-Assurance AI Architecture | Interactive Demo Launcher
echo ==============================================================
echo.
echo Launching the multi-cloud portfolio locally via Docker Compose...
echo.

docker compose up -d --build

echo.
echo Waiting for the backend microservices to stabilize (15s)...
timeout /t 15 /nobreak >nul

echo.
echo Booting Next.js Dashboard!
start http://localhost:3000

echo.
echo Demo is running in the background. To stop the environment later, run:
echo docker compose down
pause
