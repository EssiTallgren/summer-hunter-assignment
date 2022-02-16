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


    In my SQL query excercise I first get all of the fail, miss and success data and group them by
    user_id and put them in order by the success amounts. In the second SQL query I get the
    timestamps and results of the simulations of the novice users to visualize how their hoxhunt
    training affects their fail and miss rates.
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
            "COUNT(CASE WHEN outcome = 'MISS' THEN 1 END) AS misses",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
        ],
        table=DEFAULT_TABLE,
        group_by=["user_id"],
        order_by=["fails DESC"],
    )

    query_params2 = QueryParams(
        dimensions=[
            "timestamp",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
        ],
        table=DEFAULT_TABLE,
        condition=["type = 'Novice'"],
        group_by=["timestamp"],
        order_by=["timestamp"],
    )

    query_params3 = QueryParams(
        dimensions=[
            "timestamp",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
        ],
        table=DEFAULT_TABLE,
        condition=["type = 'Standard'"],
        group_by=["timestamp"],
        order_by=["timestamp"],
    )

    query_params4 = QueryParams(
        dimensions=[
            "timestamp",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
        ],
        table=DEFAULT_TABLE,
        condition=["type = 'Experienced'"],
        group_by=["timestamp"],
        order_by=["timestamp"],
    )
    # The function call above will result in the following query:
    # SELECT user_id, name, type, COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails
    # FROM training_result
    # GROUP BY user_id
    # ORDER BY fails DESC
    return query_db_to_df(query_params, result_columns=["user_id", "name", "type", "fails", "misses", "successes"]), \
        query_db_to_df(query_params2, result_columns=["timestamp", "fails", "successes"]), \
        query_db_to_df(query_params3, result_columns=["timestamp", "fails", "successes"]), \
        query_db_to_df(query_params4, result_columns=["timestamp", "fails", "successes"])


def main() -> None:
    """Run the entire simulation application."""
    create_records_into_db()
    logger.info("Training results successfully uploaded to the database")
    aggregated_data1, aggregated_data2, aggregated_data3, aggregated_data4= get_data_with_query()
    logger.info("Aggregated training results have been fetched from the db.")

    csv_filename = "visualize_outcomes.csv"
    csv_filename2 = "visualize_novice_learning_sum.csv"
    csv_filename3 = "visualize_standard_learning_sum.csv"
    csv_filename4 = "visualize_experienced_learning_sum.csv"

    aggregated_data1.to_csv(csv_filename, index=False)
    aggregated_data2.to_csv(csv_filename2, index=False)
    aggregated_data3.to_csv(csv_filename3, index=False)
    aggregated_data4.to_csv(csv_filename4, index=False)

    logger.info("Data ready for visualization can be found in %s", csv_filename)


if __name__ == "__main__":
    main()
