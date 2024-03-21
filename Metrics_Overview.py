
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
import plotly.io as pio
from numerize.numerize import numerize

# from mock_data import planning_permission_data_rows
# from generated_data import generated_data
from utils.field_option_selector import field_option_checkboxes, field_option_multiselect
from utils.get_db_data import get_db_data
from utils.gpd_load_cached import gpd_load_cached
from utils.field_definitions import metric_area_fields, metric_single_fields
from charts.px_scatter_mapbox import px_scatter_mapbox
from charts.px_bar_chart import px_bar_chart
from charts.px_choropleth_mapbox import px_choropleth_mapbox

# MAIN PAGE
st.set_page_config(
    page_title='Metrics Overview',
    page_icon='📖',
    layout='wide'
)
st.sidebar.header='Metrics Overview'

st.markdown("# Metrics Overview")

col1, col2 = st.columns(2, gap="large")


# Load data

# data_df = get_db_data()

display_gdf = gpd_load_cached('generated_data/02_preprocessed/preprocessed_data_1.json')
# LPA_gdf = gpd_load_cached('generated_data/03_area/area_1.json')



# for metric_variable in metric_area_fields:
#     for metric_unit in metric_area_fields[metric_variable]:
#         with open(f'generated_data/04_plotly/{metric_variable}_{metric_unit}_choropleth.json', 'r') as fi:
#             metric_area_fields[metric_variable][metric_unit]['fig'] = pio.from_json(fi.read())



# Value metric selector
metric_variable_selected = st.sidebar.radio(
    "Select metric",
    ['Number of Planning Applications', 'Total Fee']
)

# Metric type selector
# metric_type_selected = st.sidebar.radio(
#     "Metric units",
#     ['Number', 'Per Capita', 'Per Square Kilometre']
# )

metric_field = metric_single_fields[metric_variable_selected]['number']
metric_readable_field = metric_single_fields[metric_variable_selected]['readable']
# metric_area_field = metric_area_fields[metric_variable_selected][metric_type_selected]['field']
# metric_area_display_name = metric_area_fields[metric_variable_selected][metric_type_selected]['display_name']



# Date picker
start_date = st.sidebar.date_input('Start date', min(display_gdf['submission_date']))
end_date = st.sidebar.date_input('End date', max(display_gdf['submission_date']))

# Category filters
use_categories = field_option_checkboxes(display_gdf, 'application_category')

# Filter dataframe according to selected options
display_gdf = display_gdf.loc[
    (display_gdf['submission_date'] >= pd.to_datetime(start_date)) &
    (display_gdf['submission_date'] <= pd.to_datetime(end_date)) &
    (display_gdf['application_category'].isin(use_categories))
]
st.session_state.display_gdf = display_gdf


# Set up colours
colour_scale = 'Viridis' # Viridis, HSV, mygbm, Edge, Plasma, Rainbow, Jet, Plotly3
n_colours = len(list(set(display_gdf['application_category'])))
colours = px.colors.sample_colorscale(
    colour_scale, [n / (n_colours - 1) for n in range(n_colours)]
)
st.session_state.colour_scale = colour_scale
st.session_state.colours = colours


# Aggregated by application category data
by_category_df = display_gdf.groupby(['application_category']).agg({
    'geometry': 'count',
    'fee': 'sum',
}).reset_index().rename(columns={
    'geometry': 'number_of_applications',
    'fee': 'total_fee'
})
by_category_df['readable_fee'] = by_category_df.apply(lambda row: numerize(row['total_fee'], 2), axis=1)
by_category_df['readable_number'] = by_category_df.apply(lambda row: numerize(row['number_of_applications'], 2), axis=1)
st.session_state.by_category_df = by_category_df

# Aggregated by application type data
by_application_type_df = display_gdf.groupby([
    'application_category',
    'application_type'
]).agg({
    'geometry': 'count',
    'fee': 'sum',
}).reset_index().rename(columns={
    'geometry': 'number_of_applications',
    'fee': 'total_fee'
})
by_application_type_df['readable_fee'] = by_application_type_df.apply(lambda row: numerize(row['total_fee'], 2), axis=1)
by_application_type_df['readable_number'] = by_application_type_df.apply(lambda row: numerize(row['number_of_applications'], 2), axis=1)
st.session_state.by_application_type_df = by_application_type_df



# Scatter map
fig_map = px_scatter_mapbox(
    display_gdf=display_gdf,
    colour_field='application_category',
    colours=colours,
    size='fee',
    title='Locations by Application Category',
    legend_title='Application Category'
)
with col1:
    st.plotly_chart(fig_map, use_container_width=True)

# By category bar chart
fig_bar = px_bar_chart(
    display_df=by_category_df,
    colour_field='application_category',
    colours=colours,
    x_field='application_category',
    y_field=metric_field,
    text_field=metric_readable_field,
    title=f'{metric_variable_selected} by Application Category',
    legend_title='Application Category'
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