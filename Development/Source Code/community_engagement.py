# Filename: community_engagement.py

import logging
from typing import List, Dict
import asyncio
from communication_module import CommunicationModule

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class CommunityEngagement:
    """Class to manage community engagement activities, such as fetching and posting comments."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.comm_module = CommunicationModule()

    async def fetch_comments(self, post_id: str) -> List[Dict]:
        """Fetch comments for a given post."""
        url = f"{self.base_url}/comments/{post_id}"
        response = await self.comm_module.fetch_data(url)
        if response:
            try:
                comments = json.loads(response)
                logging.info(f"Successfully fetched {len(comments)} comments for post {post_id}.")
                return comments
            except json.JSONDecodeError:
                logging.error("Failed to decode comments data.")
        return []

    async def post_comment(self, post_id: str, comment: Dict) -> None:
        """Post a comment to a given post."""
        url = f"{self.base_url}/comments/{post_id}"
        await self.comm_module.post_data(url, comment)
        logging.info(f"Posted a new comment to post {post_id}.")

    async def close(self):
        """Close the communication module's session."""
        await self.comm_module.close()

async def main():
    base_url = "http://example.com/api"
    community_engagement = CommunityEngagement(base_url)
    
    # Example post ID
    post_id = "123"
    
    # Fetch comments for a specific post
    comments = await community_engagement.fetch_comments(post_id)
    if comments:
        logging.info(f"Comments: {comments}")

    # Post a new comment
    new_comment = {
        "author": "Jacob Vespers",
        "content": "Thank you for this insightful post!"
    }
    await community_engagement.post_comment(post_id, new_comment)

    # Cleanup
    await community_engagement.close()

if __name__ == "__main__":
    asyncio.run(main())
