import os
import json
from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from utils.logger import logger

# Azure AI Foundry — reads AZURE_RESOURCE_NAME from environment.
# Authentication is handled by DefaultAzureCredential, which automatically
# tries (in order): env vars (AZURE_CLIENT_ID / TENANT_ID / CLIENT_SECRET),
# managed identity, Azure CLI, and VS Code credentials.
_credential = DefaultAzureCredential()
_token_provider = get_bearer_token_provider(
    _credential, "https://cognitiveservices.azure.com/.default"
)

client = AnthropicFoundry(
    azure_resource_name=os.environ["AZURE_RESOURCE_NAME"],
    azure_ad_token_provider=_token_provider,
)

MODEL = "claude-sonnet-4-20250514"

def call_claude(agent_name: str, system_prompt: str, user_message: str, max_tokens: int = 2000) -> dict:
    """Core function: call Claude API and return parsed JSON output."""
    logger.log(agent_name, f"Thinking...")

    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON matching the schema. No markdown, no explanation.",
        messages=[{"role": "user", "content": user_message}]
    )

    raw = response.content[0].text.strip()
    # Strip any accidental markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```")

    return json.loads(raw)
