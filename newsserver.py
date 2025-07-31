
import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Create MCP server
mcp = FastMCP("News")

@mcp.tool()
def get_news(topic: str, limit: int = 3) -> str:
    """Get latest news headlines for a topic"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "Error: News API key not configured"
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "apiKey": api_key,
            "sortBy": "publishedAt",
            "pageSize": limit,
            "language": "en"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return f"No news found for topic: {topic}"
        
        news_text = f"Latest news about '{topic}':\n\n"
        for i, article in enumerate(articles, 1):
            news_text += (f"{i}. {article['title']}\n"
                        f"   {article['description'] or 'No description'}...\n"
                        f"   {article['url']}\n\n")
        
        return news_text
    
    except Exception as e:
        return f"Error getting news for {topic}: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")