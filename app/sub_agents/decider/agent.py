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
# from .room_idea_agent import room_idea_agent


decider_agent = Agent(
    name="decider_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are an agent that should decide whether the user wants to define what to do with his room or whether he wants a ready suggestion.
    - If he is willing to share his ideas transfer to the 'interview_agent'.
    - If he wants to recieve something ready/doesn't have any ideas transfer to the 'room_idea_agent'.
    """,
    # sub_agents=[room_idea_agent]
)

    # If he wants a suggestion continue with the 'room_idea_agent'.
