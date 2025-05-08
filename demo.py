# data = {
#     "profile1": {
#         "profile_data": {
#             "name": "Anupam Mittal",
#             "headline": "Founder & CEO @ People Group | Tech & D2C Builder & Investor\n🦈 @Shark Tank India",
#             "follower_count": 1305241,
#             "connection_count": 1371,
#             "industry": "Shaadi.com",
#             "username": "anupammittal007"
#         },
#         "posting_frequency_data": {
#             "average_posts_per_week": 2.5,
#             "most_active_days": [
#                 "Tuesday"
#             ],
#             "day_counts": {
#                 "Tuesday": 2,
#                 "Thursday": 1,
#                 "Monday": 1,
#                 "Friday": 1
#             }
#         },
#         "content_type_usage": {
#             "text_count": 5,
#             "text_percent": 100.0,
#             "images_count": 4,
#             "images_percent": 80.0,
#             "videos_count": 1,
#             "videos_percent": 20.0,
#             "document_count": 0,
#             "documents_percent": 0.0,
#             "polls_count": 0,
#             "polls_percent": 0.0
#         },
#         "post_stats": {
#             "average_likes": 2827.0,
#             "average_comments": 276.6,
#             "highest_likes": 4685,
#             "highest_comments": 512
#         },
#         "engagement_analysis": {
#             "day_wise": {
#                 "Tuesday": 36.36,
#                 "Friday": 32.49,
#                 "Monday": 29.17,
#                 "Thursday": 1.98
#             },
#             "hour_wise": {
#                 "6am-9am": 4.99,
#                 "3am-6am": 95.01
#             },
#             "month_wise": {
#                 "May": 37.48,
#                 "April": 62.52
#             },
#             "post_length_wise": {
#                 "0-100": 0.0,
#                 "101-250": 0.0,
#                 "251-500": 0.0,
#                 "501-1000": 0.0,
#                 "1001+": 100.0
#             },
#             "content_type_wise": {
#                 "text": 50.0,
#                 "images": 35.42,
#                 "videos": 14.58
#             }
#         },
#         "writing_style": {
#             "average_words": 219.4,
#             "average_emojis": 5.8,
#             "average_hashtags": 0.6
#         }
#     },
#     "profile2": {
#         "profile_data": {
#             "name": "Nitin Gadkari",
#             "headline": "Minister of Road Transport & Highways, Government of India at Government of India",
#             "follower_count": 1898719,
#             "connection_count": 2,
#             "industry": "Government of India",
#             "username": "nitin-gadkari-5b7b2b227"
#         },
#         "posting_frequency_data": {
#             "average_posts_per_week": 5.0,
#             "most_active_days": [
#                 "Monday"
#             ],
#             "day_counts": {
#                 "Monday": 5
#             }
#         },
#         "content_type_usage": {
#             "text_count": 5,
#             "text_percent": 100.0,
#             "images_count": 1,
#             "images_percent": 20.0,
#             "videos_count": 4,
#             "videos_percent": 80.0,
#             "document_count": 0,
#             "documents_percent": 0.0,
#             "polls_count": 0,
#             "polls_percent": 0.0
#         },
#         "post_stats": {
#             "average_likes": 410.6,
#             "average_comments": 14.6,
#             "highest_likes": 807,
#             "highest_comments": 29
#         },
#         "engagement_analysis": {
#             "day_wise": {
#                 "Monday": 100.0
#             },
#             "hour_wise": {
#                 "6pm-9pm": 14.96,
#                 "12pm-3pm": 85.04
#             },
#             "month_wise": {
#                 "May": 100.0
#             },
#             "post_length_wise": {
#                 "0-100": 14.96,
#                 "101-250": 18.42,
#                 "251-500": 27.65,
#                 "501-1000": 38.97,
#                 "1001+": 0.0
#             },
#             "content_type_wise": {
#                 "text": 50.0,
#                 "videos": 30.51,
#                 "images": 19.49
#             }
#         },
#         "writing_style": {
#             "average_words": 41.6,
#             "average_emojis": 0.6,
#             "average_hashtags": 2.0
#         }
#     }
# }


# # Update the procedural code to use dynamic max values

# # Separate functions for each part of the normalized score calculation

# def normalize(value, min_val, max_val, max_points):
#     if value <= min_val:
#         return 0.0
#     if value >= max_val:
#         return max_points
#     return round(((value - min_val) / (max_val - min_val)) * max_points, 2)

# def get_optimized_ratio(day_scores, hour_scores):
#     total_day_engagement = sum(day_scores.values()) or 1
#     total_hour_engagement = sum(hour_scores.values()) or 1
#     best_days = sorted(day_scores, key=day_scores.get, reverse=True)[:2]
#     best_hours = sorted(hour_scores, key=hour_scores.get, reverse=True)[:2]
#     optimized_day_engagement = sum(v for k, v in day_scores.items() if k in best_days)
#     optimized_hour_engagement = sum(v for k, v in hour_scores.items() if k in best_hours)
#     return ((optimized_day_engagement / total_day_engagement) +
#             (optimized_hour_engagement / total_hour_engagement)) / 2
    
# # Updated version that includes dynamic normalization for hashtags, emojis, and words
# def get_max_values(comparison_data):
#     max_engagement = 0
#     max_posts_per_week = 0
#     max_formats_used = 0
#     max_avg_hashtags = 0
#     max_avg_emojis = 0
#     max_avg_words = 0

#     for profile in comparison_data.values():
#         likes = profile["post_stats"]["average_likes"]
#         comments = profile["post_stats"]["average_comments"]
#         raw_engagement = likes + 2 * comments
#         max_engagement = max(max_engagement, raw_engagement)

#         posts_per_week = profile["posting_frequency_data"]["average_posts_per_week"]
#         max_posts_per_week = max(max_posts_per_week, posts_per_week)

#         content_usage = profile["content_type_usage"]
#         formats_used = sum([
#             1 if content_usage.get("text_percent", 0) > 0 else 0,
#             1 if content_usage.get("images_percent", 0) > 0 else 0,
#             1 if content_usage.get("videos_percent", 0) > 0 else 0,
#             1 if content_usage.get("documents_percent", 0) > 0 else 0,
#             1 if content_usage.get("polls_percent", 0) > 0 else 0,
#         ])
#         max_formats_used = max(max_formats_used, formats_used)

#         avg_hashtags = profile["writing_style"]["average_hashtags"]
#         avg_emojis = profile["writing_style"]["average_emojis"]
#         avg_words = profile["writing_style"]["average_words"]

#         max_avg_hashtags = max(max_avg_hashtags, avg_hashtags)
#         max_avg_emojis = max(max_avg_emojis, avg_emojis)
#         max_avg_words = max(max_avg_words, avg_words)

#     return (
#         max_engagement, max_posts_per_week, max_formats_used,
#         max_avg_hashtags, max_avg_emojis, max_avg_words
#     )

# def calculate_profile_score(profile, max_engagement, max_posts_per_week, max_formats_used,
#                             max_avg_hashtags, max_avg_emojis, max_avg_words):
#     likes = profile["post_stats"]["average_likes"]
#     comments = profile["post_stats"]["average_comments"]
#     posts_per_week = profile["posting_frequency_data"]["average_posts_per_week"]
#     avg_hashtags = profile["writing_style"]["average_hashtags"]
#     avg_emojis = profile["writing_style"]["average_emojis"]
#     avg_words = profile["writing_style"]["average_words"]

#     content_usage = profile["content_type_usage"]
#     used_formats = sum([
#         1 if content_usage.get("text_percent", 0) > 0 else 0,
#         1 if content_usage.get("images_percent", 0) > 0 else 0,
#         1 if content_usage.get("videos_percent", 0) > 0 else 0,
#         1 if content_usage.get("documents_percent", 0) > 0 else 0,
#         1 if content_usage.get("polls_percent", 0) > 0 else 0,
#     ])

#     day_scores = profile.get("engagement_analysis", {}).get("day_wise", {})
#     hour_scores = profile.get("engagement_analysis", {}).get("hour_wise", {})
#     optimized_ratio = get_optimized_ratio(day_scores, hour_scores)

#     engagement_score = normalize(likes + 2 * comments, 0, max_engagement, 65)
#     consistency_score = normalize(posts_per_week, 0, max_posts_per_week, 15)
#     variety_score = normalize(used_formats, 0, max_formats_used, 10)
#     timing_score = normalize(optimized_ratio, 0, 1, 15)
#     hashtag_score = normalize(avg_hashtags, 0, max_avg_hashtags, 10)
#     emoji_score = normalize(avg_emojis, 0, max_avg_emojis, 5)
#     length_score = normalize(avg_words, 0, max_avg_words, 10)

#     total_score = round(sum([
#         engagement_score, consistency_score, variety_score,
#         timing_score, hashtag_score, emoji_score, length_score
#     ]), 2)

#     return {
#         "engagement": engagement_score,
#         "consistency": consistency_score,
#         "variety": variety_score,
#         "timing": timing_score,
#         "hashtags": hashtag_score,
#         "emojis": emoji_score,
#         "length": length_score,
#         "total_score": total_score
#     }

# def calculate_normalized_scores(comparison_data):
#     max_vals = get_max_values(comparison_data)
#     return {
#         profile_key: calculate_profile_score(profile, *max_vals)
#         for profile_key, profile in comparison_data.items()
#     }




# result= calculate_normalized_scores(data)
# print(result)


{
    "profile1": {
        "profile_data": {
            "name": "Anupam Mittal",
            "headline": "Founder & CEO @ People Group | Tech & D2C Builder & Investor\n🦈 @Shark Tank India",
            "follower_count": 1305241,
            "connection_count": 1371,
            "industry": "Shaadi.com",
            "username": "anupammittal007"
        },
        "engagement_analysis": {
            "day_wise": {
                "Tuesday": 36.36,
                "Friday": 32.49,
                "Monday": 29.17,
                "Thursday": 1.98
            },
            "hour_wise": {
                "6am-9am": 4.99,
                "3am-6am": 95.01
            },
            "month_wise": {
                "May": 37.48,
                "April": 62.52
            },
            "post_length_wise": {
                "0-100": 0.0,
                "101-250": 0.0,
                "251-500": 0.0,
                "501-1000": 0.0,
                "1001+": 100.0
            },
            "content_type_wise": {
                "text": 50.0,
                "images": 35.42,
                "videos": 14.58
            }
        }
    },
    "profile2": {
        "profile_data": {
            "name": "Nitin Gadkari",
            "headline": "Minister of Road Transport & Highways, Government of India at Government of India",
            "follower_count": 1898719,
            "connection_count": 2,
            "industry": "Government of India",
            "username": "nitin-gadkari-5b7b2b227"
        },
        "engagement_analysis": {
            "day_wise": {
                "Monday": 100.0
            },
            "hour_wise": {
                "6pm-9pm": 14.96,
                "12pm-3pm": 85.04
            },
            "month_wise": {
                "May": 100.0
            },
            "post_length_wise": {
                "0-100": 14.96,
                "101-250": 18.42,
                "251-500": 27.65,
                "501-1000": 38.97,
                "1001+": 0.0
            },
            "content_type_wise": {
                "text": 50.0,
                "videos": 30.51,
                "images": 19.49
            }
        }
    }
}
