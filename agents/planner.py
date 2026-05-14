# TODO: Implement this agent
# Pattern: SYSTEM prompt constant + run(input) -> AgentOutput function
# Requirements:
#   - Import call_claude from agents.base
#   - Import SwarmLogger from utils.logger
#   - Import relevant Pydantic schema from utils.schemas
#   - Call logger.log() at start and end of run()
#   - Return typed output matching the schema

from agents.base import call_claude
from utils.logger import SwarmLogger
from utils.schemas import AgentOutput  # replace with correct schema class

logger = SwarmLogger()

SYSTEM_PROMPT = ""  # TODO: write the system prompt for this agent

def run(input_data: dict) -> dict:
    """TODO: implement this agent's run() function."""
    raise NotImplementedError
