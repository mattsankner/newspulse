#!/usr/bin/env python3
"""
Script to collect news articles on political topics and save them to a file.
Usage: python collect_articles.py --topic "healthcare reform" --output articles.json
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
sys.path.insert(0, root_path)

from backend.app.services.news_client import NewsClient
from backend.app.models.article import Article
from backend.app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Collect news articles on political topics")
    parser.add_argument("--topic", required=True, help="Topic to search for")
    parser.add_argument("--output", default="articles.json", help="Output file path")
    parser.add_argument("--language", default="en", help="Language of articles")
    parser.add_argument("--days-back", type=int, default=7, help="Number of days back to search")
    parser.add_argument("--page-size", type=int, default=100, help="Number of articles per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--headlines", action="store_true", help="Get top headlines instead of searching by topic")
    parser.add_argument("--category", default="politics", help="Category for top headlines")
    parser.add_argument("--country", default="us", help="Country code for top headlines")
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    args = parse_args()
    
    # Create News API client
    try:
        client = NewsClient()
    except ValueError as e:
        logger.error(f"Error creating News API client: {e}")
        return 1
    
    # Get articles
    if args.headlines:
        logger.info(f"Getting top headlines in {args.category} for {args.country}")
        articles = client.get_top_headlines(
            category=args.category,
            country=args.country,
            page_size=args.page_size,
            page=args.page
        )
    else:
        logger.info(f"Searching for articles related to: {args.topic}")
        articles = client.get_articles_by_topic(
            topic=args.topic,
            language=args.language,
            days_back=args.days_back,
            page_size=args.page_size,
            page=args.page
        )
    
    if not articles:
        logger.warning("No articles found")
        return 0
    
    # Save articles to output file
    output_path = Path(args.output)
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert Article objects to dictionaries
    articles_data = [article.dict() for article in articles]
    
    # Convert datetime objects to strings
    for article in articles_data:
        if isinstance(article["published_at"], datetime):
            article["published_at"] = article["published_at"].isoformat()
    
    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Saved {len(articles)} articles to {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())