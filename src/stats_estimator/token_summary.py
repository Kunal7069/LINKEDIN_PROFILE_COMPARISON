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
        
    def get_engagement_insights(self, profile_comparison_data: Dict) -> dict:
        
        formatted_json = json.dumps(profile_comparison_data, indent=2)

        prompt = f"""
You are a LinkedIn analytics expert.

Here is structured engagement data for two LinkedIn profiles:
{formatted_json}

Generate an **Engagement Insights** report with these sections:
- **Key Observations** (4–5 bullet points): Compare video, post length, content types, time/day engagement, and trends.
- **Timing Analysis** (1 paragraph): Highlight best-performing days and hours for the competitor and what it suggests.
- **Engagement Tactics** (5–6 bullet points): If not explicitly given, infer them from patterns. Use insights like hashtag use, comment timing, post structure, etc.

Keep the style clean, crisp, and insightful like an executive dashboard summary.
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

        return {
            "insights_report": completion_text,
            # "prompt_cost": prompt_cost,
            # "completion_cost": completion_cost,
            # "total_cost": prompt_cost + completion_cost,
            # "prompt_tokens": prompt_tokens,
            # "completion_tokens": completion_tokens,
            # "total_tokens": prompt_tokens + completion_tokens
        }
    
    def get_executive_insights(self, profile_comparison_data: Dict) -> dict:
        formatted_json = json.dumps(profile_comparison_data, indent=2)

        prompt = f"""
   You are a LinkedIn content strategist.

Below is data comparing two LinkedIn profiles in terms of content strategy, posting behavior, engagement, and writing style first is yours and second is your competitor:

{formatted_json}

Write a crisp **Overall Report** in second-person tone. The sections should include:

**Key Observations** (4–5 bullet points): Use "Your competitor..." to highlight where they outperform you. Use clear comparisons (e.g., "7.6% vs your 4.2%"). Focus on post types, length, time slots, engagement trends.

**Timing Analysis** (1 paragraph): Describe which days and hours your competitor performs best. Recommend how you can improve your timing to match.

**Engagement Tactics** (5–6 bullet points): If explicit data isn’t given, infer patterns your competitor uses (e.g., hashtags, timing, use of questions, video style). Be specific.

Use second-person throughout. You = profile1, your competitor = profile2.

Be strategic, insight-driven, and clear—like you're writing an executive summary to improve performance. Avoid fluff.
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

        return {
            "insights_report": completion_text,
            # "prompt_cost": prompt_cost,
            # "completion_cost": completion_cost,
            # "total_cost": prompt_cost + completion_cost,
            # "prompt_tokens": prompt_tokens,
            # "completion_tokens": completion_tokens,
            # "total_tokens": prompt_tokens + completion_tokens
        }
