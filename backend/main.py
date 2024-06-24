import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import stripe
from dotenv import load_dotenv

logger = logging.getLogger("uvicorn")

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")