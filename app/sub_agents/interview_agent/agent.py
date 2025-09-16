from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
# from google.adk.tools import google_search
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
# from google.adk.sessions import InMemorySessionService
# from google.adk.runners import Runner
# from google.genai import types # For creating message Content/Parts
# from google.adk.tools import VertexAiSearchTool
# import warnings
# from pydantic import BaseModel, Field
# from typing import List, Optional



interview_agent = Agent(
    name="interview_agent",
    model="gemini-2.0-flash",
  
    description=(f"""You are a helpful assistant that conducts a short interview with the user. Gether information about room to designe and preferences """
   ),
    instruction=(""" 
                 1.You conducts a short interview with the user.
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

# root_agent = Agent(
#     name="root_agent",
#     model=MODEL,
  
#     description=(f"""You are a helpful assistant who delegate tasks """
#    ),
#     instruction=("Greet the user.Use interview_agent to start intervew with user. Use `user_style` to summary  user style and goal"),
#     tools=[AgentTool(interview_agent)],
# )



