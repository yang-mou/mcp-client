import os
from typing import Any
from datetime import datetime

from bilibili_api import search, sync, video
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bilibili mcp server")

@mcp.tool()
def general_search(keyword: str) -> dict[Any, Any]:
    """
    Search Bilibili API with the given keyword.
    
    Args:
        keyword: Search term to look for on Bilibili
        
    Returns:
        Dictionary containing the search results from Bilibili
    """
    return sync(search.search(keyword))

@mcp.tool()
def get_daily_top_video(date: str = None) -> dict[str, Any]:
    """
    Get the most viewed Bilibili video for a specific date
    
    Args:
        date: Date in YYYY-MM-DD format (default: today)
        
    Returns:
        Dictionary containing the top video info
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Get popular videos for the day
    popular_videos = sync(video.get_popular())
    
    # Find video with max play count
    top_video = max(popular_videos, key=lambda v: v["stat"]["view"])
    
    return {
        "date": date,
        "title": top_video["title"],
        "author": top_video["owner"]["name"],
        "play_count": top_video["stat"]["view"],
        "url": f"https://www.bilibili.com/video/av{top_video['aid']}"
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')
