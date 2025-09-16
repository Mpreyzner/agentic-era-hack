from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
# from .config import MODEL
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from google.adk.tools import VertexAiSearchTool
from . import prompt
import warnings
from google.adk.tools import load_artifacts

from google.adk.memory import InMemorySessionService
from google.genai import Client
from google.adk.tools.tool_context import ToolContext
from vertexai.preview.vision_models import ImageGenerationModel



memory = InMemorySessionService()

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
  


nano_banana = Agent(
    model='gemini-2.5-pro',
    name='nano_banana',
    description="""An agent that generates, edits, and modifies images and answer questions about the images.""",
    instruction=""" You are an agent whose job is to generate or edit an image based on prompt provided. Use `load_artifacts` tool to gain acces to images already uploaded and edit it based on user prompt """
,
    tools=[generate_image,load_artifacts],
)

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    
  
    description=(f"""Your goal is To engage in natural language conversations with users, 
                 if request is related with image editing or generation delegate the task to subagent `nano-banana`` for execution
            """
   ),
    instruction=("""You are helpful assistant. Use `load_artifacts` tool to save uploaded images.
1.if user wants to edit or create images:
Action:Call `nano-banana` subagent
      * **Expected Output:`nano-banana` subagent shoul generate an image**    """),
tools=[AgentTool(nano_banana),load_artifacts],
)
