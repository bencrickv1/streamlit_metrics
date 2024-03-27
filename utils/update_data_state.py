import streamlit as st
import pandas as pd
import plotly.express as px
from numerize.numerize import numerize


def update_data_state(
    data_gdf, start_date, end_date, use_categories, use_LPAs, colour_scale
):

    # Filter dataframe according to selected options
    display_gdf = data_gdf.loc[
        (data_gdf["submission_date"] >= pd.to_datetime(start_date))
        & (data_gdf["submission_date"] <= pd.to_datetime(end_date))
        & (data_gdf["application_category"].isin(use_categories))
        & (data_gdf["local_planning_authority"].isin(use_LPAs))
    ]

    # Set up / update colours
    n_colours = len(use_categories)
    if n_colours == 1:
        colours = px.colors.sample_colorscale(colour_scale, [0.5])
    else:
        colours = px.colors.sample_colorscale(
            colour_scale, [n / (n_colours - 1) for n in range(n_colours)]
        )

    # Aggregated by application category data
    by_category_df = (
        display_gdf.groupby(["application_category"])
        .agg(
            {
                "geometry": "count",
                "fee": "sum",
            }
        )
        .reset_index()
        .rename(columns={"geometry": "number_of_applications", "fee": "total_fee"})
    )
    by_category_df["readable_fee"] = by_category_df["total_fee"].apply(
        lambda x: numerize(x, 2)
    )
    by_category_df["readable_number"] = by_category_df["number_of_applications"].apply(
        lambda x: numerize(x, 2)
    )

    # Aggregated by application type data
    by_application_type_df = (
        display_gdf.groupby(["application_category", "application_type"])
        .agg(
            {
                "geometry": "count",
                "fee": "sum",
            }
        )
        .reset_index()
        .rename(columns={"geometry": "number_of_applications", "fee": "total_fee"})
    )
    by_application_type_df["readable_fee"] = by_application_type_df["total_fee"].apply(
        lambda x: numerize(x, 2)
    )
    by_application_type_df["readable_number"] = by_application_type_df[
        "number_of_applications"
    ].apply(lambda x: numerize(x, 2))

    export_df = pd.DataFrame(display_gdf.drop(columns=["geometry", "readable_fee"]))

    return display_gdf, colours, by_category_df, by_application_type_df, export_df
