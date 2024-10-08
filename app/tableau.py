from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter, CreateMode

# Start Hyper process
with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:

    # Create Hyper file connection
    with Connection(endpoint=hyper.endpoint, database='output.hyper', create_mode=CreateMode.CREATE_AND_REPLACE) as connection:

        # Define the table schema
        table_definition = TableDefinition(table_name="Extract", columns=[
            ("id", SqlType.int()),
            ("name", SqlType.text()),
            ("age", SqlType.int()),
        ])

        # Create the table
        connection.catalog.create_table(table_definition)

        # Insert data from MySQL result set
        with Inserter(connection, table_definition) as inserter:
            inserter.add_rows(result)
            inserter.execute()