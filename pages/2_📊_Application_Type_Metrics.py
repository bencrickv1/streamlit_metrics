import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
from numerize.numerize import numerize

# from mock_data import planning_permission_data_rows
from generated_data import generated_data
from utils.field_option_selector import (
    field_option_checkboxes,
    field_option_multiselect,
)
from utils.field_definitions import metric_area_fields, metric_single_fields
from charts.px_scatter_mapbox import px_scatter_mapbox
from charts.px_bar_chart import px_bar_chart
from utils.update_data_state import update_data_state
from utils.file_io import convert_df_to_csv

# FEES DETAIL PAGE
st.set_page_config(page_title="Application Type Metrics", page_icon="📊", layout="wide")
st.sidebar.header = "Application Type Metrics"

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"# Metrics by Application Category and Type")


# Value metric selector
st.session_state.metric_variable_selected = st.sidebar.radio(
    "Select metric",
    st.session_state.metric_variable_options,
    index=st.session_state.metric_variable_options.index(
        st.session_state.metric_variable_selected
    ),
)

st.session_state.metric_field = metric_single_fields[
    st.session_state.metric_variable_selected
]["number"]
st.session_state.metric_readable_field = metric_single_fields[
    st.session_state.metric_variable_selected
]["readable"]

# Date picker
st.session_state.start_date = st.sidebar.date_input(
    label="Start date",
    value=st.session_state.start_date,
    min_value=st.session_state.minimum_date,
    max_value=st.session_state.maximum_date,
)
st.session_state.end_date = st.sidebar.date_input(
    label="End date",
    value=st.session_state.end_date,
    min_value=st.session_state.minimum_date,
    max_value=st.session_state.maximum_date,
)

# Category filters
st.session_state.use_categories = field_option_checkboxes(
    df=st.session_state.data_gdf,
    field_name="application_category",
    preselected=st.session_state.use_categories,
)

# Local Planning Authority filters
st.session_state.cur_toggle_LPAs, st.session_state.cur_use_LPAs = (
    field_option_multiselect(
        df=st.session_state.data_gdf,
        field_name="local_planning_authority",
        label="Local Planning Authority",
        pre_toggle=st.session_state.cur_toggle_LPAs,
        preselected=st.session_state.cur_use_LPAs,
        key="use_LPAs",
        toggle_key="toggle_LPAs",
    )
)

# Filter to selected data
(
    st.session_state.display_gdf,
    st.session_state.colours,
    st.session_state.by_category_df,
    st.session_state.by_application_type_df,
    st.session_state.export_df,
) = update_data_state(
    st.session_state.data_gdf,
    st.session_state.start_date,
    st.session_state.end_date,
    st.session_state.use_categories,
    st.session_state.use_LPAs,
    st.session_state.colour_scale,
)

# Download button
with col1:
    st.download_button(
        label="Download filtered data ⬇️",
        data=convert_df_to_csv(st.session_state.export_df),
        file_name=f"{st.session_state.start_date}_{st.session_state.end_date}_metrics.csv",
        mime="text/csv",
    )
with col2:
    for _ in range(4):
        st.markdown("# ")


col = col1

for colour, application_category in zip(
    st.session_state.colours, st.session_state.use_categories
):

    if not application_category in st.session_state.use_categories:
        continue

    category_df = st.session_state.by_application_type_df.loc[
        st.session_state.by_application_type_df["application_category"]
        == application_category
    ]

    fig_bar = px_bar_chart(
        display_df=category_df,
        colour_field="application_category",
        colours=[colour],
        x_field="application_type",
        y_field=st.session_state.metric_field,
        text_field=st.session_state.metric_readable_field,
        title=f"Application Category - {application_category}: {st.session_state.metric_variable_selected} by Application Type",
        showlegend=False,
    )

    with col:
        st.plotly_chart(fig_bar, use_container_width=True)
    col = col1 if col == col2 else col2
