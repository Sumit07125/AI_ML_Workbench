import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter 
from agno.tools.duckduckgo import DuckDuckGoTools

from agno.tools.yfinance import YFinanceTools
# 1. Load the environment variables from your .env file
load_dotenv()

def build_agent():
    return Agent(
        model=OpenRouter(id="openai/gpt-4o-mini"), 
        tools=[DuckDuckGoTools(), YFinanceTools()],
        markdown=True,
        debug_mode=True,
        description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
        instructions=["Use give tool whenever possible .Format your response using markdown and use tables to display data where possible."]
    )

openrouter_agent = build_agent()
openrouter_agent.print_response("Share the NVDA stock price and analyst recommendations")