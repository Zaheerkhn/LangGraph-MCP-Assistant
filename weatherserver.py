
import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Create MCP server
mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: Weather API key not configured"
    
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return (f"Weather in {data['name']}, {data['sys']['country']}: "
                f"{data['main']['temp']}°C, {data['weather'][0]['description']}. "
                f"Humidity: {data['main']['humidity']}%, "
                f"Wind: {data['wind']['speed']} m/s")
    
    except Exception as e:
        return f"Error getting weather for {city}: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")