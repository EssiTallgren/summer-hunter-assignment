from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import numpy as np
import names
from config import TRAINING_INTERVAL_DAYS

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
    def _get_simulation_outcome(self) -> str:
        """Implement this method in your own subclass.

        It should always return one of the possible SIMULATION_OUTCOMES
        """
        return

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

# The users' probabilities of failures and misses decrease when they go through
# training. The learning curve is logarithmic for the standard user and for the
# novice user it's linear. The experienced user doesn't learn much more from the
# training. Only after the first simulation as they will get a refresher on the
# topic.

class ExperiencedUser(User):
    """
    Experienced user class. Represents people who have training or knowledge in spotting
    phishing emails and knows how to react to them. For example; programmers, IT personnel.
    """

    def __init__(self) -> None:
        """Init the object."""
        super(ExperiencedUser, self).__init__(type="Experienced")

    def _get_simulation_outcome(self) -> str:
        # The probability of an experienced user getting caught in a phishing attack
        # is low, as is the propability of a miss.

        miss_prob = 0.10
        fail_prob = 0.10

        # After one training simulation the user gets better at spotting the phishing emails
        if len(self.history) >= 1:
            miss_prob = 0.04
            fail_prob = 0.02

        success_prob = 1-miss_prob-fail_prob

        outcome = np.random.choice(SIMULATION_OUTCOMES, p = [success_prob, miss_prob, fail_prob])

        return outcome

class StandardUser(User):
    """
    Standard user class. Represents people who have basic knowledge on phishing attacks (have
    heard of them at the least). Have some experience with computers, but might not know how to
    correctly react to phishing emails. For example; finance and marketing personnel or younger
    personnel with less experience with computers.
    """

    def __init__(self) -> None:
        """Init the object."""
        super(StandardUser, self).__init__(type="Standard")

    def _get_simulation_outcome(self) -> str:
        # The probability of a miss or a fail is higher than for an experienced user

        miss_prob = 0.35
        fail_prob = 0.15

        # training simulation amounts affect training effectivity logarithmicly
        training_curve = 5*np.log10(len(self.history))

        # after 100 simulations the curve gives a value of 10. This will be seen as the max
        # value of 'training'. Values bigger than 10 do not better the user's performance.
        # Minimum miss_probability is 0.04 and fail_probability 0.02. This is accounted to
        # human error.
        if training_curve is np.nan:
            pass
        elif 0 < training_curve <= 10:
            miss_prob = miss_prob-((miss_prob-0.04)*training_curve*0.1)
            fail_prob = fail_prob-((fail_prob-0.02)*training_curve*0.1)
        else:
            miss_prob = 0.04
            fail_prob = 0.02

        success_prob = 1-miss_prob-fail_prob

        outcome = np.random.choice(SIMULATION_OUTCOMES, p = [success_prob, miss_prob, fail_prob])

        return outcome

class NoviceUser(User):
    """
    Novice user class. Has no knowledge on phishing, doesn't know how to react to phishing emails.
    Might have close to no experience with computers and scams. For example: Older employees, human
    resources, public relations.
    """

    def __init__(self) -> None:
        """Init the object."""
        super(NoviceUser, self).__init__(type="Novice")

    def _get_simulation_outcome(self) -> str:
        # The probability of a fail or a miss is considerably higher than with the standard
        # and experienced user.

        miss_prob = 0.30
        fail_prob = 0.50

        # training simulation amounts affect the user's performance linearly.
        training_lin = 1/100*len(self.history)

        # after 100 training simulations, the user's performace doesn't increase. The minimum
        # miss_probability is 0.04 and fail_probability 0.02.
        if training_lin <= 1:
            miss_prob = miss_prob - ((miss_prob-0.04)*training_lin)
            fail_prob = fail_prob - ((fail_prob-0.02)*training_lin)
        else:
            miss_prob = 0.04
            fail_prob = 0.02

        success_prob = 1-miss_prob-fail_prob

        outcome = np.random.choice(SIMULATION_OUTCOMES, p = [success_prob, miss_prob, fail_prob])

        return outcome
