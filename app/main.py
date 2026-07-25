"""
Issue #10 -- FastAPI Scaffold -- app/main.py
"""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Customer Churn Prediction & BI Platform API")
app.include_router(router)