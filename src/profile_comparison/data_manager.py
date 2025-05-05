import http.client
import json
import re
from settings.rapid_api_management import rapid_api_management
from stats_estimator.content_summary import ContentSummarizer
from stats_estimator.engagement_analysis import PostStats
from database.main import services
content_summrizer = ContentSummarizer()
posts_stats = PostStats()

class LinkedinPostFetcher:
    def __init__(self, rapidapi_key, rapidapi_host=rapid_api_management.BASE_URL):
        self.rapidapi_key = rapidapi_key
        self.rapidapi_host = rapidapi_host

    
    def get_profile_analysis(self, username, post_limit=0,caching = "no"):
        """Fetches posts for a given LinkedIn username with optional reactions/comments and slicing."""

        if not username:
            return {"error": "Username is required"}
        if caching == "no":
            endpoint_base = f"/get-profile-posts?username={username}"
            all_posts = self.fetch_paginated_posts(endpoint_base, post_limit)

            posts = all_posts[:post_limit]
        
            profile_data = self.get_profile_info(username)
            print(profile_data)
            profile_data['username']=username
            # services['profile_service'].save_profile(profile_data)
                
        else : 
            
            posts = services['post_service'].get_recent_posts(username,post_limit)
            profile_data = services['profile_service'].get_profiles_by_name(username)
            
        try:
            data = []
            # profile_data = self.get_profile_info(username)
            if len(posts)>0:
                for post in posts:
                    if isinstance(post, dict):
                        documents = post.get("document", {})
                        polls = post.get("poll", {})
                    # STEP 1: Save post only
                        temporary_data = {
                            "text": post.get("text"),
                            "totalreactions": post.get("totalReactionCount") or 0,
                            "totalcomments": post.get("commentsCount") or 0,
                            "postedDate":post.get("postedDate"),
                            "images": post.get("image") or post.get("resharedPost", {}).get("image") or [],
                            "original_post_text": post.get("resharedPost", {}).get("text", "No original post text available"),
                            "video": post.get("video") or [],
                            "documents":  len(documents) if isinstance(documents, dict) else 0,
                            "polls": len(polls) if isinstance(polls, dict) else 0
                        }
                        
                        if len(temporary_data['images'])>0:
                            temporary_data['is_images']="yes"
                        else:
                            temporary_data['is_images']="no"
                        
                        if len(temporary_data['video'])>0:
                            temporary_data['is_videos']="yes"
                        else:
                            temporary_data['is_videos']="no"
                        
                        if temporary_data['documents']!=0:
                            temporary_data['is_documents']="yes"
                        else:
                            temporary_data['is_documents']="no"
                            
                        if temporary_data['polls']!=0:
                            temporary_data['is_polls']="yes"
                        else:
                            temporary_data['is_polls']="no"
                            
                        if temporary_data["text"] and temporary_data["text"].strip():
                            temporary_data["is_text"] = "yes"
                        else:
                            temporary_data["is_text"] = "no"
                                                
                        data.append({**temporary_data})
                
                # if caching == "no":
                #     services['post_service'].save_posts(data,username)
                
                
        
                posting_frequency_data=content_summrizer.posting_frequency(data)
                content_type_usage = content_summrizer.content_type_usage(data)
                stats = posts_stats.calculate_stats(data)
                engagement_analysis = {"day_wise":posts_stats.get_weekday_normalized_engagement(data,profile_data['follower_count']) ,
                                    "hour_wise":posts_stats.get_hourly_normalized_engagement(data,profile_data['follower_count']),
                                    "month_wise":posts_stats.get_monthly_normalized_engagement(data,profile_data['follower_count']),
                                    "post_length_wise":posts_stats.get_length_based_engagement_percentage(data,profile_data['follower_count']),
                                    "content_type_wise":posts_stats.get_content_type_engagement_percentage(data,profile_data['follower_count'])
}
                writing_style = content_summrizer.get_writing_style_metrics(data)
                return {"profile_data":profile_data,"posting_frequency_data":posting_frequency_data,"content_type_usage":content_type_usage,"post_stats":stats,
                        "engagement_analysis":engagement_analysis,"writing_style":writing_style}
            else:
                return {"profile_data":profile_data,"posting_frequency_data":{},"content_type_usage":{},"post_stats":{},
                        "engagement_analysis":{},"writing_style":{}}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from API"}
        
    
    
    def get_profile_info(self, username):
        """Fetches basic profile info such as connection count for a given LinkedIn username."""
        if not username:
            return {"error": "Username is required"}

        conn = http.client.HTTPSConnection(self.rapidapi_host)
        headers = {
            'x-rapidapi-key': self.rapidapi_key,
            'x-rapidapi-host': self.rapidapi_host
        }

        endpoint = f"/data-connection-count?username={username}"
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()

        try:
            json_data = json.loads(data.decode("utf-8"))
            temporary_data = {
                        "name": json_data.get("data")['firstName']+" "+json_data.get("data")['lastName'],
                        "headline" : json_data.get("data")['headline'] or '',
                        "follower_count": json_data.get("follower") or 0,
                        "connection_count":json_data.get("connection") or 0,
                        "industry":json_data.get("data")["position"][0]["companyName"] or ''
                        
                    }
            return temporary_data
        except json.JSONDecodeError:
            return {"error": "Failed to parse profile info response"}
        
    def fetch_paginated_posts(self, endpoint_base: str, post_limit: int) -> list:
        conn = http.client.HTTPSConnection(self.rapidapi_host)
        headers = {
            'x-rapidapi-key': self.rapidapi_key,
            'x-rapidapi-host': self.rapidapi_host
        }

        all_posts = []
        start = 0
        pagination_token = None

        while len(all_posts) < post_limit:
            endpoint = f"{endpoint_base}&start={start}"
            if pagination_token:
                endpoint += f"&paginationToken={pagination_token}"

            conn.request("GET", endpoint, headers=headers)
            res = conn.getresponse()
            data = res.read()

            try:
                json_data = json.loads(data.decode("utf-8"))
                if "message" in json_data and not json_data.get("success", False):
                    raise ValueError(json_data["message"])
                
                posts = json_data.get("data", [])
                all_posts.extend(posts)

                if len(all_posts) >= post_limit:
                    break

                pagination_token = json_data.get("paginationToken")
                if not pagination_token:
                    break

                start += 50  # adjust for next batch

            except json.JSONDecodeError:
                raise ValueError("Failed to parse response")

        return all_posts[:post_limit]
