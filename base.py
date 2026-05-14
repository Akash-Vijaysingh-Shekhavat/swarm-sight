import os
import json
import anthropic
from utils.logger import logger

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
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
