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


decider_agent = Agent(
    name="decider_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are an agent that should decide what will be the next point in creating the user's dreem room.
    Ask the user if he has something in mind or not. Store his decision in the state variable 'user_decision'.
    Possible values of 'user_decision' are:
    - begin interview
    - generate idea
    """,
    output_key = "user_decision"
)
