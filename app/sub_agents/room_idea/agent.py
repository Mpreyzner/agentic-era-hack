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


room_idea_agent = Agent(
    model='gemini-2.5-pro',
    name='room_idea_agent',
    description="""An agent that generates, edits, and modifies images and answer questions about the images.""",
    instruction=""" You are an agent whose job is to generate an image of a room that user sent, give him an idea.
    """,
    tools=[generate_image],
)

