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
from google.adk.tools import Tool
from vertexai.generative_models import GenerativeModel, Part

def analyze_room_picture(picture: Part) -> str:
    """
    Analyzes a picture of a room and returns a description of its key features.

    Args:
        picture: A picture of the room to analyze.

    Returns:
        A string describing the key features of the room.
    """
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    response = model.generate_content(
        ["Describe the key features of this room.", picture]
    )
    return response.text


room_analyzer_agent = Agent(
    name="room_analyzer_agent",
    model="gemini-2.5-pro",
    instruction="You are an agent that analyzes room pictures and identifies key features.",
    tools=[
        Tool(
            name="analyze_room_picture",
            description="Analyzes a picture of a room and returns a description of its key features.",
            func=analyze_room_picture,
        )
    ],
)
