class ContentScore:
    def __init__(self):
        pass

    def normalize(self, value, min_val, max_val, max_points):
        if value <= min_val:
            return 0.0
        if value >= max_val:
            return max_points
        return round(((value - min_val) / (max_val - min_val)) * max_points, 2)

    def get_max_values(self, data):
        max_engagement = 0
        max_posts_per_week = 0
        max_formats_used = 0
        max_avg_hashtags = 0
        max_avg_emojis = 0
        max_avg_words = 0

        for profile in data.values():
            likes = profile["post_stats"]["average_likes"]
            comments = profile["post_stats"]["average_comments"]
            raw_engagement = likes + 2 * comments
            max_engagement = max(max_engagement, raw_engagement)

            posts_per_week = profile["posting_frequency_data"]["average_posts_per_week"]
            max_posts_per_week = max(max_posts_per_week, posts_per_week)

            content_usage = profile["content_type_usage"]
            formats_used = sum([
                1 if content_usage.get("text_percent", 0) > 0 else 0,
                1 if content_usage.get("images_percent", 0) > 0 else 0,
                1 if content_usage.get("videos_percent", 0) > 0 else 0,
                1 if content_usage.get("documents_percent", 0) > 0 else 0,
                1 if content_usage.get("polls_percent", 0) > 0 else 0,
            ])
            max_formats_used = max(max_formats_used, formats_used)

            avg_hashtags = profile["writing_style"]["average_hashtags"]
            avg_emojis = profile["writing_style"]["average_emojis"]
            avg_words = profile["writing_style"]["average_words"]

            max_avg_hashtags = max(max_avg_hashtags, avg_hashtags)
            max_avg_emojis = max(max_avg_emojis, avg_emojis)
            max_avg_words = max(max_avg_words, avg_words)

        return (max_engagement, max_posts_per_week, max_formats_used,
                max_avg_hashtags, max_avg_emojis, max_avg_words)

    def get_optimized_ratio(self, day_scores, hour_scores):
        total_day_engagement = sum(day_scores.values()) or 1
        total_hour_engagement = sum(hour_scores.values()) or 1
        best_days = sorted(day_scores, key=day_scores.get, reverse=True)[:2]
        best_hours = sorted(hour_scores, key=hour_scores.get, reverse=True)[:2]
        optimized_day_engagement = sum(v for k, v in day_scores.items() if k in best_days)
        optimized_hour_engagement = sum(v for k, v in hour_scores.items() if k in best_hours)
        return ((optimized_day_engagement / total_day_engagement) +
                (optimized_hour_engagement / total_hour_engagement)) / 2

    def calculate_scores(self, data):
        max_vals = self.get_max_values(data)
        (max_engagement, max_posts_per_week, max_formats_used,
         max_avg_hashtags, max_avg_emojis, max_avg_words) = max_vals

        results = {}

        for profile_key, profile in data.items():
            likes = profile["post_stats"]["average_likes"]
            comments = profile["post_stats"]["average_comments"]
            posts_per_week = profile["posting_frequency_data"]["average_posts_per_week"]
            avg_hashtags = profile["writing_style"]["average_hashtags"]
            avg_emojis = profile["writing_style"]["average_emojis"]
            avg_words = profile["writing_style"]["average_words"]

            content_usage = profile["content_type_usage"]
            formats_used = sum([
                1 if content_usage.get("text_percent", 0) > 0 else 0,
                1 if content_usage.get("images_percent", 0) > 0 else 0,
                1 if content_usage.get("videos_percent", 0) > 0 else 0,
                1 if content_usage.get("documents_percent", 0) > 0 else 0,
                1 if content_usage.get("polls_percent", 0) > 0 else 0,
            ])

            day_scores = profile.get("engagement_analysis", {}).get("day_wise", {})
            hour_scores = profile.get("engagement_analysis", {}).get("hour_wise", {})
            optimized_ratio = self.get_optimized_ratio(day_scores, hour_scores)

            # Score each area
            engagement_score = self.normalize(likes + 2 * comments, 0, max_engagement, 35)
            consistency_score = self.normalize(posts_per_week, 0, max_posts_per_week, 15)
            variety_score = self.normalize(formats_used, 0, max_formats_used, 10)
            timing_score = self.normalize(optimized_ratio, 0, 1, 15)
            hashtag_score = self.normalize(avg_hashtags, 0, max_avg_hashtags, 10)
            emoji_score = self.normalize(avg_emojis, 0, max_avg_emojis, 5)
            length_score = self.normalize(avg_words, 0, max_avg_words, 10)

            total_score = round(sum([
                engagement_score, consistency_score, variety_score,
                timing_score, hashtag_score, emoji_score, length_score
            ]), 2)

            results[profile_key] = {
                "engagement_rate": engagement_score,
                "post_consistency": consistency_score,
                "post_variety": variety_score,
                "post_timing": timing_score,
                "hashtags_usage": hashtag_score,
                "emojis_usage": emoji_score,
                "length_usage": length_score,
                "total_score": total_score
            }

        return results
