
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
from numerize.numerize import numerize

# from mock_data import planning_permission_data_rows
from generated_data import generated_data
from utils.field_option_selector import field_option_checkboxes, field_option_multiselect
from utils.get_db_data import get_db_data
from charts.px_scatter_mapbox import px_scatter_mapbox
from charts.px_bar_chart import px_bar_chart

# FEES DETAIL PAGE
st.set_page_config(
    page_title='Location by Application Type',
    page_icon='📊',
    layout='wide'
)
st.sidebar.header='Location by Application Type'

colours = st.session_state.colours
display_gdf = st.session_state.display_gdf

st.markdown('# Location by Application Category and Application Type')

col1, col2 = st.columns(2, gap="large")

n_colours = len(list(set(display_gdf['application_category'])))

application_categories = sorted(list(set(display_gdf['application_category'])))

col = col1

for colour, application_category in zip(colours, application_categories):

    category_gdf = display_gdf.loc[display_gdf['application_category']==application_category]

    colour_scale_2 = 'Plotly3_r' # Viridis, HSV, mygbm, Edge, Plasma, Rainbow, Jet, Plotly3
    n_colours_2 = len(list(set(category_gdf['application_type'])))
    if n_colours_2 > 1:
        colours_2 = px.colors.sample_colorscale(
            colour_scale_2, [n / (n_colours_2 - 1) for n in range(n_colours_2)]
        )
    else:
        colours_2 = px.colors.sample_colorscale(colour_scale_2, 0.0)

    fig_map = px_scatter_mapbox(
        display_gdf=category_gdf,
        colour_field='application_type',
        colours=colours_2,
        size='fee',
        title=f'Application Category - {application_category}: Locations by Application Type',
        legend_title='Application Type'
    )

    with col:
        st.plotly_chart(fig_map, use_container_width=True)
    col = col1 if col == col2 else col2

