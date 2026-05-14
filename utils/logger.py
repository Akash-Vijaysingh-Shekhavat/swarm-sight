# TODO: Implement SwarmLogger — powers the live activity feed in the Streamlit UI
# Must be called in every agent's run() function (per Cowork rules)

class SwarmLogger:
    def __init__(self):
        self.logs = []

    def log(self, agent: str, message: str, status: str = "info"):
        """TODO: implement logging that feeds into Streamlit's live feed."""
        raise NotImplementedError
