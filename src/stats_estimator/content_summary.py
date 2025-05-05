from datetime import datetime
from collections import Counter
import calendar
import re

emoji_pattern = re.compile("[\U0001F600-\U0001F64F"  # Emoticons
                           "\U0001F300-\U0001F5FF"  # Symbols & pictographs
                           "\U0001F680-\U0001F6FF"  # Transport & map symbols
                           "\U0001F1E0-\U0001F1FF"  # Flags
                           "\U00002700-\U000027BF"  # Dingbats
                           "\U0001F900-\U0001F9FF"  # Supplemental symbols
                           "\U00002600-\U000026FF"  # Misc symbols
                           "]+", flags=re.UNICODE)

class ContentSummarizer:
    def __init__(self):
        pass

    def _parse_timestamps(self, posts):
        parsed = []
        for post in posts:
            timestamp = post.get("postedDate")
            if timestamp:
                try:
                    # Parsing "2023-12-25 11:51:47.405 +0000 UTC"
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f %z %Z")
                    parsed.append(dt)
                except ValueError as e:
                    print(f"Skipping invalid timestamp: {timestamp} ({e})")
        return sorted(parsed)

    def posting_frequency(self, posts):
        timestamps = self._parse_timestamps(posts)

        if not timestamps or len(timestamps) < 2:
            return {
                "average_posts_per_week": 0,
                "most_active_days": [],
                "total_posts": len(timestamps),
            }

        first = timestamps[0]
        last = timestamps[-1]

        total_days = (last - first).days
        total_weeks = max(total_days / 7, 1)

        total_posts = len(timestamps)
        avg_posts_per_week = round(total_posts / total_weeks, 2)

        day_counts = Counter()
        for dt in timestamps:
            day_name = calendar.day_name[dt.weekday()]
            day_counts[day_name] += 1

        max_count = max(day_counts.values(), default=0)
        most_active_days = [day for day, count in day_counts.items() if count == max_count]

        return {
            "average_posts_per_week": avg_posts_per_week,
            "most_active_days": most_active_days,
            "day_counts":day_counts
        }
    
    def content_type_usage(self, posts):
        total_posts = len(posts)
        
        text = 0
        images = 0
        videos = 0
        documents = 0
        polls=0
        for post in posts:
            if post['is_text']=="yes":
                text=text+1
            if post['is_videos']=="yes":
                videos=videos+1
            if post['is_images']=="yes":
                images=images+1
            if post['is_documents']=="yes":
                documents=documents+1
            if post['is_polls']=="yes":
                polls=polls+1
                
        
        text_count = text
        images_count = images
        videos_count = videos
        document_count = documents
        polls_count =  polls
        
        text_percent = (text *100) / total_posts
        images_percent = (images *100) / total_posts
        videos_percent = (videos *100) / total_posts
        documents_percent  = (documents *100) / total_posts
        polls_percent  = (polls *100) / total_posts
        
        return {
            "text_count": text_count,
            "text_percent": text_percent,
            "images_count": images_count,
            "images_percent":images_percent,
            "videos_count":videos_count,
            "videos_percent":videos_percent,
            "document_count":document_count,
            "documents_percent":documents_percent,
            "polls_count":polls_count,
            "polls_percent":polls_percent
            
        }
   
    def get_writing_style_metrics(self,posts):
        """
        Returns average word count, emoji count, and hashtag count across all posts.
        """
        total_words = 0
        total_emojis = 0
        total_hashtags = 0
        total_posts = len(posts)

        for post in posts:
            text = post.get("text", "")

            # Word count
            words = re.findall(r'\b\w+\b', text)
            total_words += len(words)

            # Hashtag count
            hashtags = re.findall(r"#\w+", text)
            total_hashtags += len(hashtags)

            # Emoji count using regex
            emojis = emoji_pattern.findall(text)
            total_emojis += len(emojis)

        if total_posts == 0:
            return {
                "average_words": 0,
                "average_emojis": 0,
                "average_hashtags": 0
            }

        return {
            "average_words": round(total_words / total_posts, 2),
            "average_emojis": round(total_emojis / total_posts, 2),
            "average_hashtags": round(total_hashtags / total_posts, 2)
        }