from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database.models.post import LinkedInPost, PostImage, PostVideo


class LinkedInPostService:
    def __init__(self, db: Session):
        self.db = db

    def save_posts(self, posts_data: List[dict], username: str):
        saved_posts = []
        for post_data in posts_data:
            try:
    
                # Check if post already exists for the user with the same posted_date
                exists = self.db.query(LinkedInPost).filter_by(
                    username=username,
                    posted_date=post_data.get("postedDate")
                ).first()

                if exists:
                    continue 

                post = LinkedInPost(
                    username=username,
                    text=post_data.get("text"),
                    original_post_text=post_data.get("original_post_text", "No original post text available"),
                    totalreactions=post_data.get("totalreactions", 0),
                    totalcomments=post_data.get("totalcomments", 0),
                    posted_date=post_data.get("postedDate"),
                )

                for img in post_data.get("images", []):
                    post.images.append(PostImage(
                        url=img["url"],
                        width=img.get("width"),
                        height=img.get("height")
                    ))

                for vid in post_data.get("video", []):
                    post.videos.append(PostVideo(
                        url=vid["url"],
                        width=vid.get("width"),
                        height=vid.get("height")
                    ))

                self.db.add(post)
                saved_posts.append(post)

            except Exception as e:
                print(f"Error saving a post: {e}")
                self.db.rollback()

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Commit failed: {e}")
        return saved_posts
    
    def get_recent_posts(self, username: str, limit: int = 10) -> List[dict]:
        try:
            posts = (
                self.db.query(LinkedInPost)
                .filter(LinkedInPost.username == username)
                .order_by(LinkedInPost.posted_date.desc())
                .limit(limit)
                .all()
            )

            result = []
            for post in posts:
                result.append({
                    "text": post.text,
                    "original_post_text": post.original_post_text,
                    "totalReactionCount": post.totalreactions,
                    "commentsCount": post.totalcomments,
                    "postedDate": post.posted_date,
                    "image": [
                        {"url": img.url, "width": img.width, "height": img.height}
                        for img in post.images
                    ],
                    "video": [
                        {"url": vid.url, "width": vid.width, "height": vid.height}
                        for vid in post.videos
                    ],
                })

            return result

        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []
