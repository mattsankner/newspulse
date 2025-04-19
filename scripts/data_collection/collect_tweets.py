#!/usr/bin/env python3
"""
Script to collect tweets on political topics and save them to a file.
Usage: python collect_tweets.py --query "politics" --output tweets.json
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the backend directory to sys.path to import the app modules
root_path = str(Path(__file__).resolve().parent.parent.parent)
print(f"Adding to Python path: {root_path}")
sys.path.insert(0, root_path)
print(f"Python path is now: {sys.path}")

from backend.app.services.twitter_client import TwitterClient
from backend.app.models.tweet import Tweet
from backend.app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Collect tweets on political topics")
    parser.add_argument("--query", required=True, help="Search query to use")
    parser.add_argument("--output", default="tweets.json", help="Output file path")
    parser.add_argument("--max-results", type=int, default=100, help="Maximum number of tweets to collect")
    parser.add_argument("--days-back", type=int, default=7, help="Number of days back to search")
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    args = parse_args()
    
    # Create Twitter client
    try:
        client = TwitterClient()
    except ValueError as e:
        logger.error(f"Error creating Twitter client: {e}")
        return 1
    
    # Search for tweets
    logger.info(f"Searching for tweets with query: {args.query}")
    tweets = client.search_recent_tweets(
        query=args.query,
        max_results=args.max_results,
        days_back=args.days_back
    )
    
    if not tweets:
        logger.warning("No tweets found")
        return 0
    
    # Save tweets to output file
    output_path = Path(args.output)
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert Tweet objects to dictionaries
    tweets_data = [tweet.dict() for tweet in tweets]
    
    # Convert datetime objects to strings
    for tweet in tweets_data:
        if isinstance(tweet["created_at"], datetime):
            tweet["created_at"] = tweet["created_at"].isoformat()
    
    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tweets_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Saved {len(tweets)} tweets to {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())