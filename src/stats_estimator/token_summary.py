from typing import List, Dict
from tokencost import (
    calculate_prompt_cost,
    calculate_completion_cost,
    count_message_tokens,
    count_string_tokens
)
from openai import OpenAI
import json

class OpenAiTokenizer:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def prepare_prompt(self, posts: List[str]) -> str:
        formatted_posts = "\n".join([f"{i+1}. \"{post}\"" for i, post in enumerate(posts)])
        prompt = f"""
        Here are some LinkedIn posts by a user:
    {formatted_posts}

    Can you summarize the user's tone, themes, and content focus?
    """
        return prompt

    def calculate_token_and_cost_usage(self, posts: List[str]) -> dict:
        prompt = self.prepare_prompt(posts)
        message = [{"role": "user", "content": prompt}]
        
        prompt_cost = calculate_prompt_cost(message, model=self.model)
        prompt_tokens = count_message_tokens(message, model=self.model)
        
        return {
            "prompt_cost": prompt_cost,
            "prompt_tokens": prompt_tokens
        }

    def get_summary(self,posts: List[str]) -> dict:
        prompt = self.prepare_prompt(posts)
        message = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message,
            temperature=0.7
        )

        completion_text = response.choices[0].message.content
        completion_cost = calculate_completion_cost(completion_text, model=self.model)
        completion_tokens = count_string_tokens(completion_text, model=self.model)

        return {
            "summary": completion_text,
            "completion_cost": completion_cost,
            "completion_tokens": completion_tokens
        }
        
#     def get_engagement_insights(self, profile_comparison_data: Dict) -> dict:
        
#         formatted_json = json.dumps(profile_comparison_data, indent=2)

#         prompt = f"""
# You are a LinkedIn analytics expert.

# Here is structured engagement data for two LinkedIn profiles:
# {formatted_json}

# Generate an **Engagement Insights** report with these sections:
# - **Key Observations** (3-4 bullet points): Compare video, post length, content types, time/day engagement, and trends.
# - **Timing Analysis** (40 words): Highlight best-performing days and hours for the competitor and what it suggests.
# - **Engagement Tactics** (3-4 bullet points): If not explicitly given, infer them from patterns. Use insights like hashtag use, comment timing, post structure, etc.
# Use second-person throughout. You = profile1, your competitor = profile2.
# Keep the style clean, crisp, and insightful like an executive dashboard summary.
# """

#         message = [{"role": "user", "content": prompt}]
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=message,
#             temperature=0.7
#         )

#         completion_text = response.choices[0].message.content
#         prompt_cost = calculate_prompt_cost(message, model=self.model)
#         completion_cost = calculate_completion_cost(completion_text, model=self.model)
#         prompt_tokens = count_message_tokens(message, model=self.model)
#         completion_tokens = count_string_tokens(completion_text, model=self.model)

#         return {
#             "insights_report": completion_text,
#             # "prompt_cost": prompt_cost,
#             # "completion_cost": completion_cost,
#             # "total_cost": prompt_cost + completion_cost,
#             # "prompt_tokens": prompt_tokens,
#             # "completion_tokens": completion_tokens,
#             # "total_tokens": prompt_tokens + completion_tokens
#         }
    
#     def get_executive_insights(self, profile_comparison_data: Dict) -> dict:
#         formatted_json = json.dumps(profile_comparison_data, indent=2)

#         prompt = f"""
#    You are a LinkedIn content strategist.

# Below is data comparing two LinkedIn profiles in terms of content strategy, posting behavior, engagement, and writing style first is yours and second is your competitor:

# {formatted_json}

# Write a crisp **Overall Report** in second-person tone. The sections should include:

# **Key Observations** (60-70 words): Use "Your competitor..." to highlight where they outperform you. Use clear comparisons (e.g., "7.6% vs your 4.2%"). Focus on post types, length, time slots, engagement trends.

# Use second-person throughout. You = profile1, your competitor = profile2.

# Be strategic, insight-driven, and clear—like you're writing an executive summary to improve performance. Avoid fluff.
#     """

#         message = [{"role": "user", "content": prompt}]
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=message,
#             temperature=0.7
#         )

#         completion_text = response.choices[0].message.content
#         prompt_cost = calculate_prompt_cost(message, model=self.model)
#         completion_cost = calculate_completion_cost(completion_text, model=self.model)
#         prompt_tokens = count_message_tokens(message, model=self.model)
#         completion_tokens = count_string_tokens(completion_text, model=self.model)

#         return {
#             "insights_report": completion_text,
#             # "prompt_cost": prompt_cost,
#             # "completion_cost": completion_cost,
#             # "total_cost": prompt_cost + completion_cost,
#             # "prompt_tokens": prompt_tokens,
#             # "completion_tokens": completion_tokens,
#             # "total_tokens": prompt_tokens + completion_tokens
#         }



    def get_executive_insights(self, profile_comparison_data: Dict) -> dict:
        formatted_json = json.dumps(profile_comparison_data, indent=2)

        prompt = f"""
    You are a LinkedIn Profile Analytics Assistant. Given comparison data between two LinkedIn profiles – (the user) and (the competitor) – analyze their performance and produce structured executive summary sections. Use the provided metrics (e.g. content formats used, engagement rates, audience demographics, post frequency, performance benchmarks, and any data like [Content Engagement Data]) to inform your analysis. Follow the format and instructions for each section below, replacing placeholders with the relevant data. Ensure the tone is professional and Qualitative, and the output is clear, consistent, and actionable.

    Goal: Provide a high-level overview comparing the two profiles. Highlight key performance strengths and gaps, and immediate opportunities for improvement for the user profile.
         
        - Content: 3-5 sentence paragraph summarizing the most critical differences. Focus on overall engagement levels, growth, and notable content performance differences.
        - Mention: Which profile leads in key metrics (e.g., higher engagement rate or follower count) and what strategic gap to address first.
        - Tone: Qualitative and factual (Within 450 Character) , e.g. “[UserProfileName]’s posts average X% engagement, trailing [CompetitorProfileName] by Y%. The competitor’s strength in [area] highlights an improvement opportunity. Immediate focus should be on [quick win improvement] to close the gap.”

    Below is the profile comparison data:
    {formatted_json}
    Use second-person throughout. You = profile1, your competitor = profile2
    Return the response in json format not string with keys Content,Mention,Tone
    
    """

        message = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message,
            temperature=0.7
        )

        completion_text = response.choices[0].message.content
        prompt_cost = calculate_prompt_cost(message, model=self.model)
        completion_cost = calculate_completion_cost(completion_text, model=self.model)
        prompt_tokens = count_message_tokens(message, model=self.model)
        completion_tokens = count_string_tokens(completion_text, model=self.model)
        print(type(completion_text))
        parsed_json = json.loads(completion_text)
        print(type(parsed_json))
        return {
            "insights_report": parsed_json,
            # "prompt_cost": prompt_cost,
            # "completion_cost": completion_cost,
            "total_cost": prompt_cost + completion_cost,
            # "prompt_tokens": prompt_tokens,
            # "completion_tokens": completion_tokens,
            # "total_tokens": prompt_tokens + completion_tokens
        }
        
    def get_engagement_insights(self, profile_comparison_data: Dict) -> dict:
        formatted_json = json.dumps(profile_comparison_data, indent=2)

        prompt = f"""
    You are a LinkedIn Profile Analytics Assistant. Given comparison data between two LinkedIn profiles – (the user) and (the competitor) – analyze their engagement performance and Insights, produce structured Engagement Insights summary sections. Use the provided metrics (e.g. engagement rates, post frequency, performance benchmarks, and any data like [Engagement Data]) to inform your analysis. Follow the format and instructions for each section below. Ensure the tone is professional and Qualitative, and the output is clear, consistent, and actionable.

    Goal: Given engagement comparison data between two LinkedIn profiles (a user and a competitor), analyze and summarize how audience engagement differs. Focus on highlighting performance gaps, behavioral patterns, and opportunities to improve. Use engagement rates, post types, frequency, and performance benchmarks to support your analysis.
         
        - Key Observations : Extract and compare important insights from the data. Focus on measurable patterns in post engagement, length, consistency, and audience interaction quality.
                
                - Instructions:
                       - Note which profile receives higher engagement overall.
                       - Mention the ideal post length range that drives better results.
                       - Identify whether engagement is increasing, stable, or declining over time for each.
                       - Highlight if one profile consistently gets more comments (indicating deeper interaction) while the other gets more likes or impressions.
                       - Include any clear advantage one profile holds in terms of content effectiveness
        
        - Timing Analysis: Evaluate the impact of posting times and days on engagement. Use engagement timing data to highlight differences and suggest optimal posting schedules.
               
               - Instructions:
                       - Identify which days and time slots generate peak engagement for each profile.
                       - Mention if one profile consistently performs better during specific business-hour windows.
                       - Suggest adjustments to the user’s posting schedule to match high-performing windows observed in the competitor’s data.
                    
                    
        - Engagement Tactics: Analyze the stylistic and strategic differences in how both profiles create content and engage their audience.
               
               - Instructions:
                       - Compare use of storytelling, personal anecdotes, questions, emojis, or calls to action.
                       - Note if one profile encourages more discussion or comments.
                       - Identify which post formats (e.g. carousels, text-only, polls) are driving stronger engagement.
                       - Suggest which of the competitor’s tactics could be adopted to improve performance.
    
    Below is the engagement analysis data:
    {formatted_json}
    Use second-person throughout. You = profile1, your competitor = profile2
    Return the response in json format not string with keys Key_Observations,Timing_Analysis,Engagement_Tactics
    
    """

        message = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message,
            temperature=0.7
        )

        completion_text = response.choices[0].message.content
        prompt_cost = calculate_prompt_cost(message, model=self.model)
        completion_cost = calculate_completion_cost(completion_text, model=self.model)
        prompt_tokens = count_message_tokens(message, model=self.model)
        completion_tokens = count_string_tokens(completion_text, model=self.model)
        print(type(completion_text))
        parsed_json = json.loads(completion_text)
        print(type(parsed_json))
        return {
            "insights_report": parsed_json,
            # "prompt_cost": prompt_cost,
            # "completion_cost": completion_cost,
            "total_cost": prompt_cost + completion_cost,
            # "prompt_tokens": prompt_tokens,
            # "completion_tokens": completion_tokens,
            # "total_tokens": prompt_tokens + completion_tokens
        }