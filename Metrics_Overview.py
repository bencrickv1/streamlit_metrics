import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
import plotly.io as pio
from numerize.numerize import numerize

from utils.field_option_selector import field_option_checkboxes, field_option_multiselect
from utils.get_db_data import get_db_data
from utils.gpd_load_cached import gpd_load_cached
from utils.field_definitions import metric_area_fields, metric_single_fields
from charts.px_scatter_mapbox import px_scatter_mapbox
from charts.px_bar_chart import px_bar_chart
from charts.px_choropleth_mapbox import px_choropleth_mapbox
from utils.update_data_state import update_data_state
from utils.file_io import convert_df_to_csv

# MAIN PAGE
st.set_page_config(page_title="Metrics Overview", page_icon="📖", layout="wide")
st.sidebar.header = "Metrics Overview"

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("# Metrics Overview")

with col2:
    st.markdown("# ")

st.session_state.colour_scale = (
    "Viridis"  # Viridis, HSV, mygbm, Edge, Plasma, Rainbow, Jet, Plotly3
)

# Load data

# data_df = get_db_data()

st.session_state.data_gdf = gpd_load_cached(
    "generated_data/02_preprocessed/preprocessed_data_1.json"
)
# LPA_gdf = gpd_load_cached('generated_data/03_area/area_1.json')

st.session_state.minimum_date = min(st.session_state.data_gdf["submission_date"])
st.session_state.maximum_date = max(st.session_state.data_gdf["submission_date"])

st.session_state.application_categories = sorted(
    list(set(st.session_state.data_gdf["application_category"]))
)

st.session_state.LPAs = sorted(
    list(set(st.session_state.data_gdf["local_planning_authority"]))
)

# for metric_variable in metric_area_fields:
#     for metric_unit in metric_area_fields[metric_variable]:
#         with open(f'generated_data/04_plotly/{metric_variable}_{metric_unit}_choropleth.json', 'r') as fi:
#             metric_area_fields[metric_variable][metric_unit]['fig'] = pio.from_json(fi.read())


# Data initialisation
st.session_state.metric_variable_options = [
    "Number of Planning Applications",
    "Total Fee",
]
if not "metric_variable_selected" in st.session_state:
    st.session_state.metric_variable_selected = (
        st.session_state.metric_variable_options[0]
    )

if not "start_date" in st.session_state:
    st.session_state.start_date = st.session_state.minimum_date
if not "end_date" in st.session_state:
    st.session_state.end_date = st.session_state.maximum_date

if not "use_categories" in st.session_state:
    st.session_state.use_categories = st.session_state.application_categories

if not "cur_toggle_LPAs" in st.session_state:
    st.session_state.cur_toggle_LPAs = True

if not "cur_use_LPAs" in st.session_state:
    st.session_state.cur_use_LPAs = st.session_state.LPAs

# Value metric selector
st.session_state.metric_variable_selected = st.sidebar.radio(
    "Select metric",
    st.session_state.metric_variable_options,
    index=st.session_state.metric_variable_options.index(
        st.session_state.metric_variable_selected
    ),
)

# Metric type selector
# metric_type_selected = st.sidebar.radio(
#     "Metric units",
#     ['Number', 'Per Capita', 'Per Square Kilometre']
# )

st.session_state.metric_field = metric_single_fields[
    st.session_state.metric_variable_selected
]["number"]
st.session_state.metric_readable_field = metric_single_fields[
    st.session_state.metric_variable_selected
]["readable"]
# metric_area_field = metric_area_fields[st.session_state.metric_variable_selected][metric_type_selected]['field']
# metric_area_display_name = metric_area_fields[st.session_state.metric_variable_selected][metric_type_selected]['display_name']

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
    for _ in range(3):
        st.markdown("# ")


# Scatter map
fig_map = px_scatter_mapbox(
    display_gdf=st.session_state.display_gdf,
    colour_field="application_category",
    colours=st.session_state.colours,
    size=st.session_state.map_size_field,
    title=f"Locations by Application Category{st.session_state.map_scale_note}",
    legend_title="Application Category",
)
with col1:
    st.plotly_chart(fig_map, use_container_width=True)

# By category bar chart
fig_bar = px_bar_chart(
    display_df=st.session_state.by_category_df,
    colour_field="application_category",
    colours=st.session_state.colours,
    x_field="application_category",
    y_field=st.session_state.metric_field,
    text_field=st.session_state.metric_readable_field,
    title=f"{st.session_state.metric_variable_selected} by Application Category",
    legend_title="Application Category",
)
with col2:
    st.plotly_chart(fig_bar, use_container_width=True)

# Choropleth map
# fig_choropleth = px_choropleth_mapbox(
#     area_gdf=LPA_gdf,
#     colour_field=metric_area_field,
#     colour_scale=colour_scale,
#     title=f'{metric_area_display_name} by Local Planning authority',
#     showlegend=True,
#     legend_title=metric_area_display_name
# )
# st.plotly_chart(fig_choropleth)
# st.plotly_chart(metric_area_fields[metric_variable][metric_unit]['fig'])
