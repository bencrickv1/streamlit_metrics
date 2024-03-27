import streamlit as st
import pandas as pd
import json


def get_db_data() -> pd.DataFrame:

    # Initialize connection
    conn = st.connection("postgresql", type="sql")

    # Perform query
    df = conn.query("SELECT * FROM metrics;", ttl="10m")

    map_data = []
    for row in df.itertuples():

        row_str = str(row.metrics).replace("'", '"').replace("True", "true")

        row_dict = json.loads(row_str)

        # st.write('--------------------')

        # for k, v in row_dict.items():
        # st.write(f'{k} | {v}')

        map_data.append(
            {
                "application_type": row_dict["application_type"],
                "fee": row_dict["fee"],
                "lat": row_dict["latitude"],
                "lon": row_dict["longitude"],
                "submission_date": row_dict["submission_date"][:10],
            }
        )

    map_df = pd.DataFrame(map_data)

    return map_df
