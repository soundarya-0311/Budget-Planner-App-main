import os
from langchain_openai import ChatOpenAI
from fastapi import FastAPI


app = FastAPI(title = "Budget Buddy..$$")
llm = ChatOpenAI(model = os.getenv("MODEL"), api_key = os.getenv("OPENAI_API_KEY"), temperature= 0.5)

from routers import budgetplan_app,middleware
app.include_router(budgetplan_app.router)

