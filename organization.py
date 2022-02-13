from collections import Counter
from datetime import datetime, timedelta
from typing import List

import pandas as pd

from config import TABLE_COLUMNS
from user import DummyUser, User


class Organization:
    """Class for a hypothetical customer organization."""

    def __init__(self, n_users: int, n_simulations: int, training_interval_days: int) -> None:
        """Init the object."""
        self.n_users = n_users
        self.n_simulations = n_simulations
        self.training_interval_days = training_interval_days
        self.users = self._populate_organization()
        assert all(
            issubclass(type(user), User) for user in self.users
        ), "Please create your users as subclasses of the abstract User class."

    def _populate_organization(self) -> List:
        # TODO(Task 2):
        # 1. import your own user types created in Task 1 from the user.py module
        # 2. change this to populate the organization with your own user types
        # 3. change the distribution from uniform to something a bit more realistic
        users = []
        for i in range(self.n_users):
            users.append(DummyUser())
        return users

    def do_training(self) -> None:
        """Train organization with Hoxhunt simulations."""
        for i in range(self.n_simulations):
            timestamp = datetime.now() + timedelta(days=self.training_interval_days * i)
            for user in self.users:
                user.complete_simulation(timestamp=timestamp)

    def get_result(self) -> pd.DataFrame:
        """Fetch the results of training."""
        org_history = []
        for user in self.users:
            org_history += user.history
        return pd.DataFrame(org_history, columns=TABLE_COLUMNS)

    def __repr__(self) -> str:
        """Update the representation of a class object."""
        user_names = [user.name for user in self.users]
        name, amount = Counter(user_names).most_common(1)[0]
        return (
            f"Organization(n_users={self.n_users}, n_simulations={self.n_simulations}, "
            f"training_interval_days={self.training_interval_days}, "
            f"random_fact=The most common name in your organization is {name}, "
            f"there are {amount} of them... I wonder who's the best performer 🤔)"
        )
