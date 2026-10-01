# M.3.G.A.I - AI Agent with MCP

A powerful personal AI agent built with **FastAPI + MCP 2.2.0 + Groq + LangGraph** that can see images, search the web, check weather, and find locations.

## Features
- 👁️ **Vision** - Analyze uploaded images with Groq Vision
- 🌤️ **Weather** - Get live weather for any city
- 📍 **Location** - Lat/Lon + Google Maps link for any place
- 🔍 **Web Search** - DuckDuckGo real-time search
- ⚡ **MCP 2.2.0 Streamable-HTTP** - Modern MCP architecture
- **Github connection - Connecting to github account using PAT, performing github actions and many more
- **Send Email messages 


## Setup

### 1. Install
```bash
git clone https://github.com/fortuneobasi2020-ship-it/M.3.G.A.I.git
cd Doomsday
python -m venv AI
source AI/bin/activate
pip install mcp "mcp==2.2.0" httpx fastapi uvicorn python-dotenv langchain-groq langchain-community langgraph

# MCP server
python server.py
# Running on http://0.0.0.0:4000/mcp

# Run the API
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
