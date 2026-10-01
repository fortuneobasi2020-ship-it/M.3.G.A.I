from mcp.server.mcpserver import MCPServer
import asyncio
import httpx
import urllib.parse
import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

mcp = MCPServer("Doomsday")

@mcp.tool()
async def weather_api(city: str) -> str:
  try:
    async with httpx.AsyncClient() as client:
      url = f"https://wttr.in/{city}?format=j1"
      r = await client.get(url, timeout=10)
      data = r.json()
      curr = data["current_condition"][0]
      desc = curr['weatherDesc'][0]['value']
      return f"City: {desc}, {curr['temp_C']}C feels like {curr['FeelsLikeC']}C"
  except Exception:
    return "Could not connect to api"

@mcp.tool()
async def find_location(place: str) -> str:
  try:
    async with httpx.AsyncClient() as client:
      url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(place)}&format=json&limit=1"
      r = await client.get(url, headers={"User-Agent":"Doomsday/1.0"}, timeout=10)
      data = r.json()
      loc = data[0]
      lat = loc["lat"]
      lon = loc["lon"]
      google_map = f"https://www.google.com/maps?q={lat},{lon}"
      return f"Location: {loc['display_name']}| Latitude: {lat}| Longitude: {lon}| Browser mode: {google_map}"
  except Exception:
    return "Could not connect to api"

@mcp.tool()
async def github_create_repo(name: str, description: str = "", private: bool = False) -> str:
    token = os.getenv("GITHUB_TOKEN")
    async with httpx.AsyncClient() as client:
        r = await client.post("https://api.github.com/user/repos",
            headers={"Authorization": f"token {token}"},
            json={"name": name, "description": description, "private": private}
        )
        j = r.json()
        return f"Created: {j.get('html_url')}" if r.status_code == 201 else f"Error: {r.text}"

@mcp.tool()
async def github_create_issue(repo: str, title: str, body: str = "") -> str:
    token = os.getenv("GITHUB_TOKEN")
    async with httpx.AsyncClient() as client:
        r = await client.post(f"https://api.github.com/repos/{repo}/issues",
            headers={"Authorization": f"token {token}"},
            json={"title": title, "body": body}
        )
        j = r.json()
        return f"Issue created: {j.get('html_url')}" if r.status_code == 201 else f"Error: {r.text}"

@mcp.tool()
async def github_search_repos(query: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.github.com/search/repositories?q={query}&per_page=5")
        data = r.json()
        repos = [f"{x['full_name']}: {x['html_url']} - {x['description']}" for x in data.get('items', [])]
        return "\n".join(repos) or "No repos found"

@mcp.tool()
async def github_get_user(username: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.github.com/users/{username}")
        j = r.json()
        return f"{j['login']} - {j['name']} - Repos: {j['public_repos']} - Followers: {j['followers']} - {j['html_url']}"

@mcp.tool()
async def github_list_my_repos() -> str:
    token = os.getenv("GITHUB_TOKEN")
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com/user/repos?per_page=10&sort=updated", headers={"Authorization": f"token {token}"})
        repos = [f"{x['full_name']}: {x['html_url']}" for x in r.json()]
        return "\n".join(repos) or "No repos"

@mcp.tool()
async def send_email(owner: str, to: str, subject: str, html: str) -> str:
    """Send emails messages to anyone worldwide"""
    try:
        app_password = os.getenv("APP_PASSWORD")
        my_email = os.getenv("MY_EMAIL")
        yag = yagmail.SMTP(my_email, app_password)
        yag.send(to=to, subject=subject, contents=html)
        return "Message sent successfully"
    except Exception as e:
        return f"Message not sent: {e}"

if __name__== "__main__":
  mcp.run(transport="streamable-http", port=4000, host="0.0.0.0")
