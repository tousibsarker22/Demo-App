# Video/Transcript → Process Document (Local Run)

This bundle lets you run the agent **locally** (no Docker required) and opens in a **new browser window**.

## Prerequisites
- **Python 3.10+** with `venv`
- **Node.js 18+** (includes `npm`)
- **ffmpeg** in PATH (for audio extraction)
- Azure credentials:
  - Azure OpenAI (deployment name, endpoint, API key)
  - Azure AI Speech (key, region)

## Quick Start
1. Unzip this archive somewhere on your local drive.
2. Create `backend/.env` by copying `backend/.env.example` and filling your keys.
3. **Windows (PowerShell)**
   ```powershell
   .\scripts\start_local.ps1
   ```
   **macOS/Linux**
   ```bash
   chmod +x scripts/start_local.sh
   ./scripts/start_local.sh
   ```
4. Your app opens at **http://localhost:3000**. Upload a video/audio or paste a transcript → **Build Process** → **Export Word**.

> If you prefer Docker, use `docker-compose up --build` instead.

## Notes
- The **/document** endpoint now responds with a direct file download, so the export button downloads the .docx in one click.
- If transcription is slow, try shorter clips or Azure Speech batch modes.

## Stop
- Close the Terminal/PowerShell windows.
- To fully stop, kill the backend process and `Ctrl+C` the frontend.

Generated on 2026-03-11 13:07:25
