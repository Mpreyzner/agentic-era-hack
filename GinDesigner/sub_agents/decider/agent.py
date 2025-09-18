# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search


search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Finds inspiration on the internet based on user's style",
    instruction="""
        1. You are a helpful assistant that finds inspiration on the internet.
        2. Use the `google_search` tool to find inspiration related to the `user_style`.
        3. The output should be a list of URLs.
    """,
    tools=[google_search],
    output_key="inspiration_urls",
)

room_idea_agent = Agent(
    name="room_idea_agent",
    model="gemini-2.0-flash",
    description="Generates an idea for the room",
    instruction="""
        You are a professional room designer that based on user's room KEY_FEATURES generates anb idea of the room.
        Do it by generating a picture that could possibly suit the user. If the user approves your idea write back HURA,
        if not generate a new idea.
    """,
)

interview_agent = Agent(
    name="interview_agent",
    model="gemini-2.0-flash",
    description=(
        """You are a helpful assistant that conducts a short interview with the user. Gether information about room to designe and preferences """
    ),
    instruction=(
        """ 
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
    output_key="user_style",
)


decider_agent = Agent(
    name="decider_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are an agent that should decide whether the user wants to define what to do with his room or whether he wants a ready suggestion.
    - If he is willing to share his ideas transfer to the 'interview_agent'.
    - If he wants to recieve something ready/doesn't have any ideas transfer to the 'room_idea_agent'.
    """,
    sub_agents=[interview_agent, room_idea_agent]
)

