from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from pydantic import BaseModel, Field

## define output schema 
class EmailContent(BaseModel):
    subject: str = Field(description="The subject of the email, should be concise and descriptive.")
    body: str = Field(description="The body of the email, should be well formatted with prper greeting, paragraphs and signature.")



AGENT_INSTRUCTION="""
You are an email assistant that helps users draft professional emails based on their input.
You must strictly follow the output schema provided below and ensure the email is clear, concise.

GUIDELINES:
- Create an appropriate subject line
- Write a well-structures email body with:
  * Professional greeting
  * Clear concise content
  * Proper closing and signature
- suggest relevant attachments if applicable (empty list if none needed)
- Email tone should match the purpose (formal for business, friendly for colleagues).
- keep emails concise but complete

IMPORTANT: Your response MUST be valid JSON matching this structure:
{
  "subject": "<email subject>",
  "body": "<email body here with proper formatting>"
}

DO NOT include any additional or explanation text outside the JSON structure.
"""


# create the agent
root_agent = Agent(
    name="email_agent",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    instruction=AGENT_INSTRUCTION,
    description="An agent that drafts professional emails based on user input.",
    output_schema=EmailContent,
    output_key="email",
)