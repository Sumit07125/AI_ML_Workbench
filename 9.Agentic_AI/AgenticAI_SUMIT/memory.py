from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
import os
load_dotenv()

from agno.db.sqlite import SqliteDb
from rich.pretty import pprint

db = SqliteDb(db_file="agno.db")
db.clear_memories()


def build_agent():
    return Agent(
        model=OpenRouter(id="openai/gpt-4o-mini"), 
        db=db,
        markdown=True,
        add_history_to_context=True,
        enable_user_memories=True        
        )

agent = build_agent()
user_id = "sumitmali07225@gmail.com"
agent.print_response("My name is Sumit. currently I am at 3rd year of my graduation. I am interested in learning about AI and its applications.",user_id=user_id)

agent.print_response("Who am I? and what do I like and what i do? ",user_id=user_id)

memories = db.get_user_memories(user_id=user_id)
pprint(memories)


