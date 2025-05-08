from datetime import datetime
from collections import defaultdict

class PostStats:
    def __init__(self):
        self.avg_likes = 0
        self.avg_comments = 0
        self.highest_likes = 0
        self.highest_comments = 0

    def calculate_stats(self, posts):
        """
        posts: List of dictionaries with keys 'likes' and 'comments'
        Example:
        posts = [
            {"likes": 100, "comments": 20},
            {"likes": 200, "comments": 30},
            ...
        ]
        """
        if not posts:
            print("No posts available.")
            return

        total_likes = 0
        total_comments = 0
        max_likes = 0
        max_comments = 0

        for post in posts:
            likes = post.get('totalreactions', 0)
            comments = post.get('totalcomments', 0)

            total_likes += likes
            total_comments += comments
            max_likes = max(max_likes, likes)
            max_comments = max(max_comments, comments)

        self.avg_likes = total_likes / len(posts)
        self.avg_comments = total_comments / len(posts)
        self.highest_likes = max_likes
        self.highest_comments = max_comments
        
        return {
            "average_likes": round(self.avg_likes, 2),
            "average_comments": round(self.avg_comments, 2),
            "highest_likes": self.highest_likes,
            "highest_comments": self.highest_comments
        }
        
    def get_weekday_normalized_engagement(self,post_data, followers):
        """
        Returns a dictionary mapping weekdays to total normalized engagement scores.
        Engagement = Likes + 2 × Comments
        Normalized Engagement = (Engagement / Followers) × 1000
        """
        if followers == 0:
            raise ValueError("Follower count must be greater than 0")

        weekday_engagement = defaultdict(float)

        for post in post_data:
            try:
                # Extract date, likes, comments
                posted_date_str = post['postedDate']
                likes = post.get('totalreactions', 0)
                comments = post.get('totalcomments', 0)
                
                # Parse posted date
                posted_date = datetime.strptime(posted_date_str.split(" ")[0], "%Y-%m-%d")
                weekday = posted_date.strftime("%A")  # Full weekday name

                # Calculate engagement and normalize
                engagement = likes + (2 * comments)
                normalized = (engagement / followers) * 1000

                # Add to weekday total
                weekday_engagement[weekday] += normalized

            except Exception as e:
                print(f"Error processing post: {e}")
        
        total_engagement = sum(weekday_engagement.values())
        if total_engagement == 0:
            return {}

        # Convert to percentages
        weekday_percentages = {
            day: round((value / total_engagement) * 100, 2)
            for day, value in weekday_engagement.items()
        }
        return dict(weekday_percentages)
    
    
    
    def get_monthly_normalized_engagement(self, post_data, followers):
        """
        Returns a dictionary mapping months to total normalized engagement percentages.
        
        Engagement = Likes + 2 × Comments  
        Normalized Engagement = (Engagement / Followers) × 1000  
        The result is returned as percentages of total monthly engagement.
        """
        if followers == 0:
            raise ValueError("Follower count must be greater than 0")

        monthly_engagement = defaultdict(float)

        for post in post_data:
            try:
                posted_date_str = post['postedDate']
                likes = post.get('totalreactions', 0)
                comments = post.get('totalcomments', 0)

                # Extract month name (e.g., 'January', 'February')
                posted_date = datetime.strptime(posted_date_str.split(" ")[0], "%Y-%m-%d")
                month = posted_date.strftime("%B")

                # Calculate normalized engagement
                engagement = likes + (2 * comments)
                normalized = (engagement / followers) * 1000

                monthly_engagement[month] += normalized

            except Exception as e:
                print(f"Error processing post: {e}")

        total_engagement = sum(monthly_engagement.values())
        if total_engagement == 0:
            return {}

        # Convert to percentage
        monthly_percentages = {
            month: round((value / total_engagement) * 100, 2)
            for month, value in monthly_engagement.items()
        }

        return dict(monthly_percentages)

    def get_length_based_engagement_percentage(self,post_data, followers):
        """
        Returns normalized engagement percentage for buckets based on post text length.
        Engagement = Likes + 2 × Comments
        Normalized Engagement = (Engagement / Followers) × 1000
        Output is % of total normalized engagement in each bucket.
        Buckets: 0-100, 101-250, 251-500, 501-1000, 1001+
        """
        if not followers or followers <= 0:
            raise ValueError("Follower count must be greater than 0")

        buckets = {
            "0-100": 0,
            "101-250": 0,
            "251-500": 0,
            "501-1000": 0,
            "1001+": 0
        }

        for post in post_data:
            try:
                text = post.get("text", "")
                text_length = len(text)
                likes = post.get("totalreactions", 0)
                comments = post.get("totalcomments", 0)

                engagement = likes + (2 * comments)
                normalized = (engagement / followers) * 1000

                if text_length <= 100:
                    bucket = "0-100"
                elif text_length <= 250:
                    bucket = "101-250"
                elif text_length <= 500:
                    bucket = "251-500"
                elif text_length <= 1000:
                    bucket = "501-1000"
                else:
                    bucket = "1001+"

                buckets[bucket] += normalized

            except Exception as e:
                print(f"Error processing post: {e}")

        total_engagement = sum(buckets.values())

        if total_engagement == 0:
            return {bucket: 0.0 for bucket in buckets}

        return {
            bucket: round((value / total_engagement) * 100, 2)
            for bucket, value in buckets.items()
        }
    
    def get_reshare_based_engagement_percentage(self, post_data, followers):
        """
        Returns normalized engagement percentage based on whether a post is reshared or original.
        Engagement = Likes + 2 × Comments
        Normalized Engagement = (Engagement / Followers) × 1000
        Output is % of total normalized engagement for 'reshared' and 'original' posts.
        """
        if not followers or followers <= 0:
            raise ValueError("Follower count must be greater than 0")

        buckets = {
            "reshared": 0,
            "original": 0
        }

        for post in post_data:
            try:
                likes = post.get("totalreactions", 0)
                comments = post.get("totalcomments", 0)
                reshared = post.get("reshared", "no").lower()

                engagement = likes + (2 * comments)
                normalized = (engagement / followers) * 1000

                if reshared == "yes":
                    buckets["reshared"] += normalized
                else:
                    buckets["original"] += normalized

            except Exception as e:
                print(f"Error processing post: {e}")

        total_engagement = sum(buckets.values())

        if total_engagement == 0:
            return {bucket: 0.0 for bucket in buckets}

        return {
            bucket: round((value / total_engagement) * 100, 2)
            for bucket, value in buckets.items()
        }

    def get_time_slot(self,hour, minute):
        """Returns a time bucket label based on hour and minute"""
        total_minutes = hour * 60 + minute

        # Define time slots (start minute, end minute, label)
        time_slots = [
            (1, 180, '12am-3am'),
            (181, 360, '3am-6am'),
            (361, 540, '6am-9am'),
            (541, 720, '9am-12pm'),
            (721, 900, '12pm-3pm'),
            (901, 1080, '3pm-6pm'),
            (1081, 1260, '6pm-9pm'),
            (1261, 1440, '9pm-12am')
        ]

        for start, end, label in time_slots:
            if start <= total_minutes <= end:
                return label
        return 'unknown'  # fallback

    def get_hourly_normalized_engagement(self,post_data, followers):
        """
        Returns:
            - time_slot_engagement: dict of {3-hour time slot: total normalized engagement}
            - best_slot: highest performing time slot
            - worst_slot: lowest performing time slot (None if only 1 slot)
        """
        if followers == 0:
            raise ValueError("Follower count must be greater than 0")

        time_slot_engagement = defaultdict(float)

        for post in post_data:
            try:
                posted_date_str = post['postedDate']
                likes = post.get('totalreactions', 0)
                comments = post.get('totalcomments', 0)

                # Parse timestamp
                post_time = datetime.strptime(posted_date_str.split(" ")[1], "%H:%M:%S.%f")
                slot = self.get_time_slot(post_time.hour, post_time.minute)

                engagement = likes + (2 * comments)
                normalized = (engagement / followers) * 1000

                time_slot_engagement[slot] += normalized

            except Exception as e:
                print(f"Error processing post: {e}")

        time_slot_engagement = dict(time_slot_engagement)

        if not time_slot_engagement:
            return {}, None, None
        elif len(time_slot_engagement) == 1:
            best_slot = list(time_slot_engagement.keys())[0]
            worst_slot = None
        else:
            best_slot = max(time_slot_engagement, key=time_slot_engagement.get)
            worst_slot = min(time_slot_engagement, key=time_slot_engagement.get)
        
        total_engagement = sum(time_slot_engagement.values())
        if total_engagement == 0:
            return {}

        # Convert to percentages
        hourly_percentages = {
            day: round((value / total_engagement) * 100, 2)
            for day, value in time_slot_engagement.items()
        }
        return hourly_percentages
            
    def get_content_type_engagement_percentage(self,post_data, followers):
        """
        Returns normalized engagement percentage for different content types.
        Content types: text, images, videos, documents, polls
        Engagement = Likes + 2 × Comments
        Normalized = (Engagement / Followers) × 1000
        """
        if not followers or followers <= 0:
            raise ValueError("Follower count must be greater than 0")

        engagement_by_type = defaultdict(float)

        for post in post_data:
            try:
                engagement = post.get("totalreactions", 0) + (2 * post.get("totalcomments", 0))
                normalized = (engagement / followers) * 1000

                if post.get("is_text") == "yes":
                    engagement_by_type["text"] += normalized
                if post.get("is_images") == "yes":
                    engagement_by_type["images"] += normalized
                if post.get("is_videos") == "yes":
                    engagement_by_type["videos"] += normalized
                if post.get("is_documents") == "yes":
                    engagement_by_type["documents"] += normalized
                if post.get("is_polls") == "yes":
                    engagement_by_type["polls"] += normalized

            except Exception as e:
                print(f"Error processing post: {e}")

        total = sum(engagement_by_type.values())

        if total == 0:
            return {key: 0.0 for key in ["text", "images", "videos", "documents", "polls"]}

        return {
            key: round((value / total) * 100, 2)
            for key, value in engagement_by_type.items()
        }