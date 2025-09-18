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
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from google.genai import types # For creating message Content/Parts
from google.adk.tools import load_artifacts
from google.genai import Client
from google.adk.tools.tool_context import ToolContext
from vertexai.preview.vision_models import ImageGenerationModel
import base64


def append_to_state(
    tool_context: ToolContext, field: str, response: str
) -> dict[str, str]:
    """Append new output to an existing state key.

    Args:
        field (str): a field name to append to
        response (str): a string to append to the field

    Returns:
        dict[str, str]: {"status": "success"}
    """
    existing_state = tool_context.state.get(field, [])
    tool_context.state[field] = existing_state + [response]
    return {"status": "success"}


client = Client()
async def generate_image(prompt: str, tool_context: 'ToolContext'):
  """Generates or edits an image based on the prompt."""
  response = client.models.generate_images (
      model='imagen-4.0-generate-001',
      prompt=prompt,
      config={'number_of_images': 1},

  )
  if not response.generated_images:
    return {'status': 'failed'}
  image_bytes = response.generated_images[0].image.image_bytes
  await tool_context.save_artifact(
      'image.png',
      types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
  )
  return {
      'status': 'success',
      'detail': 'Image generated successfully and stored in artifacts.',
      'filename': 'image.png',
  }


image_agent = Agent(
    model='gemini-2.5-pro',
    name='image_agent',
    description="""An agent that generates, edits, and modifies images and answer questions about the images.""",
    instruction=""" You are an agent whose job is to generate an image based on 'INTERVIEW_RESULTS'
    """,
    tools=[generate_image],
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

    2.Final output: Store infromation in 'INTERVIEW_RESULTS' within state using 'append_to_state' tool.
    The structure of 'INTERVIEW_RESULTS' should be as following schema:
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
    3. After finished interview transfer to the 'image_agent'.            
    """
    ),
    tools = [append_to_state],
    sub_agents=[image_agent],
)
