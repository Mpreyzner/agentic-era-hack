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
