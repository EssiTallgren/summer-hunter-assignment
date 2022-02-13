import random
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import names

from simulation import SIMULATION_OUTCOMES, SimulationResult


class User(metaclass=ABCMeta):
    """The abstract baseclass for a user, please don't use this directly.

    Create your own subclass(es) with a '_get_simulation_outcome' private method.

    DummyUser is an example of how to do this.
    """

    def __init__(self, type: str = "Base") -> None:
        """Init the object."""
        self.id: str = uuid4().hex
        self.type: str = type
        self.name: str = names.get_first_name()
        self.history: List[Optional[SimulationResult]] = []

    @abstractmethod
    def _get_simulation_outcome() -> str:
        """Implement this method in your own subclass.

        It should always return one of the possible SIMULATION_OUTCOMES
        """
        pass

    def complete_simulation(self, timestamp: datetime) -> None:
        """Complete a simulation and store it in the user's history."""
        outcome = self._get_simulation_outcome()
        assert (
            outcome in SIMULATION_OUTCOMES
        ), "The outcome from your logic is not a valid simulation outcome."

        self.history.append(
            SimulationResult(
                timestamp=datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S"),
                user_id=self.id,
                type=self.type,
                name=self.name,
                outcome=outcome,
            )
        )

    @property
    def simulations_completed(self) -> int:
        """Return amount of simulations user has completed."""
        return len(self.history)

    def __repr__(self) -> str:
        """Update the representation of a class object."""
        return (
            f"User(id={self.id}, name={self.name}, type={self.type} "
            f"simulations_completed={self.simulations_completed})"
        )


# TODO(Task 1): Implement your own user classes.
# All classes should be inherited from the above User class.
# See the DummyUser class below user for an example.
class DummyUser(User):
    """Dummy user class."""

    def __init__(self) -> None:
        """Init the object."""
        super(DummyUser, self).__init__(type="Dummy")

    def _get_simulation_outcome(self) -> str:
        """
        Implement a dummy simulation completion logic.

        Please write your own classes and make the logic smarter! :)
        """
        # In your solution, tweak this logic to mimick your chosen user types instead
        # of picking a random simulation outcome
        return random.choice(SIMULATION_OUTCOMES)
