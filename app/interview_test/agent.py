from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from .config import MODEL
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from google.adk.tools import VertexAiSearchTool
import warnings

from pydantic import BaseModel, Field
from typing import List, Optional
# from .subagents.search_agent import search_agent
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging


# class Style(BaseModel):
#     """Details about the user's style preferences."""
#     preferred_style: str = Field(description="The user's preferred style (e.g., Scandinavian, Industrial).")
#     style_details: str = Field(description="Follow-up details about the style preference.")

# class ColorScheme(BaseModel):
#     """Details about the user's color preferences."""
#     palette: str = Field(description="The preferred color palette (e.g., light, dark).")
#     specific_preferences: str = Field(description="Any specific color preferences or details.")

# class Budget(BaseModel):
#     """Details about the user's budget."""
#     range: str = Field(description="The budget range (e.g., low, medium, high).")
#     specific_amount: Optional[float] = Field(description="A specific budget amount, if provided.")

# class Functionality(BaseModel):
#     """Details about the room's functional requirements."""
#     key_priorities: List[str] = Field(description="The most important functionalities for the room.")
#     additional_requirements: str = Field(description="Any other functional requirements.")

# class Inspiration(BaseModel):
#     """Details about the user's inspiration."""
#     links: List[str] = Field(description="Links to inspiration photos or products.")
#     description: str = Field(description="A description of the user's inspiration.")

# class InterviewOutput(BaseModel):
#     """The structured output of the user interview."""
#     room_to_furnish: str = Field(description="The room the user wants to design.")
#     style: Style
#     color_scheme: ColorScheme
#     budget: Budget
#     functionality: Functionality
#     inspiration: Inspiration
#     additional_notes: str = Field(description="Any other notes or preferences from the user.")


interview_agent = Agent(
    name="interview_agent",
    model=MODEL,
  
    description=(f"""You are a helpful assistant that conducts a short interview with the user. Gether information about room to designe and preferences """
   ),
    instruction=(""" User upload photo of the room.
                 1.You conducts a short interview with the user about room he upload and his goals.
This could be a conversational flow or an interactive quiz (e.g., visual tiles to choose from).
Sample questions:
Style: Which of these styles do you prefer? (e.g Scandinavian / Industrial / Japandi / Glamour / Boho)
Colors: Which color palette do you like most? e.g light / dark / contrast / pastel)
Budget: What budget range do you want to stay within? (e.g low / medium / high)
Functionality: What’s most important for this room? (e.g comfort / workspace / representative look / easy maintenance)
Inspiration: Do you have any pins, photos, or favorite products we can use as inspiration?
The agent can adapt questions dynamically based on the user’s answers.
For example, if the user picks “industrial,” the agent can follow up:
“Do you prefer raw, unfinished materials, or do you want a modern twist with industrial accents?

2.Final output: Store infromation in variables with schema:
                 {
"room_to_designe": "",
"style": {
"preferred_style": "",
"style_details": ""
},
"color_scheme": {
"palette": "",
"specific_preferences": ""
},
"budget": {
"range": "",
"specific_amount": null
},
"functionality": {
"key_priorities": [],
"additional_requirements": ""
},
"inspiration": {
"links": [],
"description": ""
},
"additional_notes": ""
}               
                 """
                 
                
),
output_key="user_style"

)

root_agent = Agent(
    name="root_agent",
    model=MODEL,
  
    description=(f"""You are a helpful assistant who delegate tasks """
   ),
    instruction=("Greet the user.Use interview_agent to start intervew with user. Use `user_style` to summary  user style and goal"),
    tools=[AgentTool(interview_agent)],
)



