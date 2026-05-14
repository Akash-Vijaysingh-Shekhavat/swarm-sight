# TODO: Define Pydantic models for all agent outputs
# IMPORTANT: Do NOT rename fields once defined — Cowork rules prohibit schema field changes
from pydantic import BaseModel
from typing import Optional, List

class AgentOutput(BaseModel):
    """Base schema — replace with specific models per agent."""
    pass

# TODO: Add PlannerOutput, CleanerOutput, AnalystOutput, ValidatorOutput, ReporterOutput
