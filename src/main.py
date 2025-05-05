
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from profile_comparison.data_manager import LinkedinPostFetcher
from database.main import services
from fastapi import Depends,FastAPI, HTTPException,APIRouter, Header,Security
from pydantic import BaseModel
from math import ceil
from typing import Dict, Any
from database.main import services
from stats_estimator.token_summary import OpenAiTokenizer
import asyncio
import json

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- This allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers including Authorization
)

print("✅ This is the correct FastAPI file running.")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

data_fetcher = LinkedinPostFetcher(RAPID_API_KEY)
openaitokenizer = OpenAiTokenizer(OPEN_AI_KEY)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

async def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer" or token != ACCESS_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid or missing token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

class PostRequest(BaseModel):
    username_1: str
    username_2:str
    limit: int
    caching: str


class ProfileComparisonRequest(BaseModel):
    profile_comparison_data: Dict[str, Any]


@app.post("/analyse", dependencies=[Depends(verify_token)])
def get_profile_analysis(request: PostRequest):
    data_1 = data_fetcher.get_profile_analysis(request.username_1, request.limit, request.caching)
    data_2 = data_fetcher.get_profile_analysis(request.username_2, request.limit, request.caching)
    result = {"profile1": data_1, "profile2":data_2}
    return {"profile1": data_1, "profile2":data_2}

@app.post("/calculate_summary_credits", dependencies=[Depends(verify_token)])
def calculate_summary_credits(request: PostRequest):
    data_1 = services['post_service'].get_recent_posts(request.username_1,request.limit)
    post_1=[]
    for i in data_1:
        post_1.append(i['text'])
    cost_1 = openaitokenizer.calculate_token_and_cost_usage(post_1)
        
    data_2 = services['post_service'].get_recent_posts(request.username_2,request.limit)
    post_2=[]
    for i in data_2:
        post_2.append(i['text'])
    cost_2 = openaitokenizer.calculate_token_and_cost_usage(post_2)
        
    return {"post1": post_1,"cost1":cost_1,"post2": post_2,"cost2":cost_2}

@app.post("/summary", dependencies=[Depends(verify_token)])
def summary(request: PostRequest):
    data_1 = services['post_service'].get_recent_posts(request.username_1,request.limit)
    post_1=[]
    for i in data_1:
        post_1.append(i['text'])
    cost_1 = openaitokenizer.get_summary(post_1)
        
    data_2 = services['post_service'].get_recent_posts(request.username_2,request.limit)
    post_2=[]
    for i in data_2:
        post_2.append(i['text'])
    cost_2 = openaitokenizer.get_summary(post_2)
        
    return {"post1": post_1,"cost1":cost_1,"post2": post_2,"cost2":cost_2}

@app.post("/credit_estimation", dependencies=[Depends(verify_token)])
def credit_estimation(request: PostRequest):
    credits=2 + (2 * ceil(request.limit / 50))
    return {"credits": credits}

@app.post("/engagement_summary", dependencies=[Depends(verify_token)])
def engagement_summary(request: ProfileComparisonRequest):
    result = openaitokenizer.get_engagement_insights(request.profile_comparison_data)
    return {"result":result}

@app.post("/executive_summary", dependencies=[Depends(verify_token)])
def executive_summary(request: ProfileComparisonRequest):
    result = openaitokenizer.get_executive_insights(request.profile_comparison_data)
    return {"result":result}


# @app.post("/engagement_summary", dependencies=[Depends(verify_token)])
# def engagement_summary(request: ProfileComparisonRequest):
#     return {"tes": 4}

    



    
