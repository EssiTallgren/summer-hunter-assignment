import pandas as pd

from config import DEFAULT_TABLE, N_SIMULATIONS, N_USERS, TRAINING_INTERVAL_DAYS, logger
from organization import Organization
from sql import QueryParams, db_connection, query_db_to_df


def create_records_into_db() -> None:
    """Create database records from Hoxhunt training."""
    dummy_organization = Organization(
        n_users=N_USERS, n_simulations=N_SIMULATIONS, training_interval_days=TRAINING_INTERVAL_DAYS
    )
    logger.info("Organization created: %s", dummy_organization)
    dummy_organization.do_training()
    logger.info("Organization has now been trained in Hoxhunt!")
    result = dummy_organization.get_result()
    result.to_sql(DEFAULT_TABLE, db_connection, if_exists="replace", index=None)


def get_data_with_query() -> pd.DataFrame:
    """Load records from the database into a DataFrame.

    Query to fetch the raw data if you want to inspect it:

    from config import TABLE_COLUMNS
    query_params = QueryParams(
        dimensions=["*"],
        table=DEFAULT_TABLE
    )
    query_db_to_df(query_params, result_columns=TABLE_COLUMNS)
    """
    # TODO(Task 3):
    # Write a SQL query that aggregates the simulated data to a format that you want to visualize
    # To do this, you will use a Jinja template that compiles a query from a set of given arguments
    # You are allowed to write multiple queries if you wish to visualize multiple things.
    # EXAMPLE: Get number of fails per user.
    query_params = QueryParams(
        dimensions=[
            "user_id",
            "name",
            "type",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
        ],
        table=DEFAULT_TABLE,
        group_by=["user_id"],
        order_by=["fails DESC"],
    )
    # The function call above will result in the following query:
    # SELECT user_id, name, type, COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails
    # FROM training_result
    # GROUP BY user_id
    # ORDER BY fails DESC
    return query_db_to_df(query_params, result_columns=["user_id", "name", "type", "fails"])


def main() -> None:
    """Run the entire simulation application."""
    create_records_into_db()
    logger.info("Training results successfully uploaded to the database")
    aggregated_data = get_data_with_query()
    logger.info("Aggregated training results have been fetched from the db.")
    csv_filename = "visualize.csv"
    aggregated_data.to_csv(csv_filename, index=False)
    logger.info("Data ready for visualization can be found in %s", csv_filename)


if __name__ == "__main__":
    main()
