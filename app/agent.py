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

import datetime
import os
from zoneinfo import ZoneInfo

import google.auth
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.room_analyzer import room_analyzer_agent
from .sub_agents.interview_agent import interview_agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

extreme_makeover_team = SequentialAgent(
    name="extreme_makeover_team",
    description="""Generate perfect room idea. 
    Interview user to ask for user goals and preferances """,
    sub_agents=[
        room_analyzer_agent, interview_agent
    ],
)

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    description="Guides the user in room remake suggestions.",
    instruction="""
    - Let the user know you will help them with room remake ideas. Ask them for   
      a room image.
    - When they send the image transfer to the extreme_makeover_team.
    
    """,
    sub_agents=[extreme_makeover_team],
    # tools=[
    #     AgentTool(agent=room_analyzer_agent),
    # ],

)
