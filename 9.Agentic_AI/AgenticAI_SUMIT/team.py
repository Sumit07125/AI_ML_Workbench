from agno.team import Team
from agno.agent import Agent
from agno.models.openrouter import OpenRouter 
from agno.tools.duckduckgo import DuckDuckGoTools

import os
from dotenv import load_dotenv
load_dotenv()

english_agent = Agent(name="English Agent", role="You answer questions in English")
chinese_agent = Agent(name="Chinese Agent", role="You answer questions in Chinese")
hindi_agent = Agent(name="Hindi Agent", role="You answer questions in Hindi")

team_leader= Team(
             name="Multilingual Team",
             members=[english_agent, chinese_agent, hindi_agent],
             model=OpenRouter(id="openai/gpt-4o-mini"),
             tools=[DuckDuckGoTools()],
             description="A team of agents that can answer questions in multiple languages.",
             instructions="ans in all 3 languages use all agents to answer the question",
             show_members_responses=True,
             markdown=True
             )

team_leader.print_response("What is the capital of India?")