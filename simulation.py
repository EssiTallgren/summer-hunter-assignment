from dataclasses import dataclass

SIMULATION_OUTCOMES = ["SUCCESS", "MISS", "FAIL"]


@dataclass
class SimulationResult:
    """A record that is stored for each completed simulation."""

    timestamp: str
    user_id: str
    name: str
    type: str
    outcome: str
