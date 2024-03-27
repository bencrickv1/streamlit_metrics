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
from utils.get_db_data import get_db_data
from charts.px_scatter_mapbox import px_scatter_mapbox
from charts.px_bar_chart import px_bar_chart
from utils.update_data_state import update_data_state
from utils.file_io import convert_df_to_csv

# FEES DETAIL PAGE
st.set_page_config(
    page_title="Location by Application Type", page_icon="📊", layout="wide"
)
st.sidebar.header = "Location by Application Type"

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("# Location by Application Category and Type")

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

st.session_state.map_size_field = (
    "fee" if "fee" in st.session_state.metric_variable_selected.lower() else None
)
st.session_state.map_scale_note = (
    " (scale ∝ fee)"
    if "fee" in st.session_state.metric_variable_selected.lower()
    else ""
)

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


n_colours = len(list(set(st.session_state.display_gdf["application_category"])))

application_categories = sorted(
    list(set(st.session_state.display_gdf["application_category"]))
)

col = col1

for colour, application_category in zip(
    st.session_state.colours, application_categories
):

    category_gdf = st.session_state.display_gdf.loc[
        st.session_state.display_gdf["application_category"] == application_category
    ]

    colour_scale_2 = (
        "Plotly3_r"  # Viridis, HSV, mygbm, Edge, Plasma, Rainbow, Jet, Plotly3
    )
    n_colours_2 = len(list(set(category_gdf["application_type"])))
    if n_colours_2 > 1:
        colours_2 = px.colors.sample_colorscale(
            colour_scale_2, [n / (n_colours_2 - 1) for n in range(n_colours_2)]
        )
    else:
        colours_2 = px.colors.sample_colorscale(colour_scale_2, 0.0)

    fig_map = px_scatter_mapbox(
        display_gdf=category_gdf,
        colour_field="application_type",
        colours=colours_2,
        size=st.session_state.map_size_field,
        title=f"Application Category - {application_category}: Locations by Application Type{st.session_state.map_scale_note}",
        legend_title="Application Type",
        y_mod=(
            0 + -0.1
            if application_category == "Planning Permission"
            else 0.0 + -0.4 if application_category == "Prior Approval" else 0.0
        ),
    )

    with col:
        st.plotly_chart(fig_map, use_container_width=True)
    col = col1 if col == col2 else col2
