import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter 
from agno.tools.duckduckgo import DuckDuckGoTools
# 1. Load the environment variables from your .env file
load_dotenv()

def build_agent():
    return Agent(
        model=OpenRouter(id="openai/gpt-4o-mini"), 
        tools=[DuckDuckGoTools()],
        markdown=True,
        instructions="You are a helpful and expert travel agent. You will help the user plan their trip, provide recommendations, and answer any questions they have about their destination.",
        add_datetime_to_context=True,
    )

openrouter_agent = build_agent()
openrouter_agent.print_response("is it safe to travel to UAE Today? ")