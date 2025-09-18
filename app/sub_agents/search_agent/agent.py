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
    output_key="inspiration_urls"
)

