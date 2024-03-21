
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
from utils.field_definitions import metric_area_fields, metric_single_fields
from charts.px_scatter_mapbox import px_scatter_mapbox
from charts.px_bar_chart import px_bar_chart

# FEES DETAIL PAGE
st.set_page_config(
    page_title='Application Type Metrics',
    page_icon='📊',
    layout='wide'
)
st.sidebar.header='Application Type Metrics'

st.markdown(f'# Metrics by Application Category and Application Type')

col1, col2 = st.columns(2, gap="large")

# Value metric selector
metric_variable_selected = st.sidebar.radio(
    "Select metric",
    ['Number of Planning Applications', 'Total Fee']
)

metric_field = metric_single_fields[metric_variable_selected]['number']
metric_readable_field = metric_single_fields[metric_variable_selected]['readable']

colours = st.session_state.colours
by_application_type_df = st.session_state.by_application_type_df

n_colours = len(list(set(by_application_type_df['application_category'])))

application_categories = sorted(list(set(by_application_type_df['application_category'])))

col = col1

for colour, application_category in zip(colours, application_categories):

    category_df = by_application_type_df.loc[by_application_type_df['application_category']==application_category]

    fig_bar = px_bar_chart(
        display_df=category_df,
        colour_field='application_category',
        colours=[colour],
        x_field='application_type',
        y_field=metric_field,
        text_field=metric_readable_field,
        title=f'Application Category - {application_category}: {metric_variable_selected} by Application Type',
        showlegend=False
    )

    with col:
        st.plotly_chart(fig_bar, use_container_width=True)
    col = col1 if col == col2 else col2


