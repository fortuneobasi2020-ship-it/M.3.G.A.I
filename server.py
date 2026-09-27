from mcp.server.mcpserver import MCPServer
import asyncio
import httpx, urllib.parse

mcp = MCPServer("Doomsday")

@mcp.tool()
async def weather_api(city: str) -> str:
  """Get weather information about a city

  Args:
       city: The city you want to get the weather information for
  """
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
      r = await client.get(url, headers= {"User-Agent":"Doomsday/1.0"}, timeout=10)
      data = r.json()
      loc = data[0]
      lat = loc["lat"]
      lon = loc["lon"]

      google_map = f"https://www.google.com/maps?q={lat},{lon}"

      return f"Location: {loc['display_name']}| Latitude: {lat}| Longitude: {lon}| Browser mode: {google_map}"
  except Exception:
    return "Could not connect to api"


if __name__== "__main__":
  mcp.run(transport="streamable-http", port=4000, host="0.0.0.0")
