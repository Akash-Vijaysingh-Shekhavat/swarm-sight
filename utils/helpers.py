# TODO: CSV utility functions used across agents
import pandas as pd
from typing import Optional

def load_csv(path: str) -> pd.DataFrame:
    """TODO: load and validate a CSV file."""
    raise NotImplementedError

def summarize_csv(df: pd.DataFrame) -> dict:
    """TODO: return shape, dtypes, nulls summary for a DataFrame."""
    raise NotImplementedError
