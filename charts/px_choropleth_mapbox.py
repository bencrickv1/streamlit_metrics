import plotly.express as px
from .field_labels import field_labels


def px_choropleth_mapbox(
    area_gdf, colour_field, colour_scale, title, showlegend=True, legend_title=None
):

    hover_name = "LPA21NM"
    hover_data = {
        "OBJECTID": False,
        "LPA21CD": False,
        "LPA21NM": True,
        "BNG_E": False,
        "BNG_N": False,
        "LONG": False,
        "LAT": False,
        "GlobalID": False,
        "LPA_area_km2": True,
        "LPA_population": True,
        "number_of_applications": True,
        "total_fee": True,
        "applications_per_capita": True,
        "applications_per_km2": True,
        "total_fee_per_capita": True,
        "total_fee_per_km2": True,
    }

    fig_choropleth = px.choropleth_mapbox(
        data_frame=area_gdf,
        geojson=area_gdf.geometry,
        locations=area_gdf.index,
        color=colour_field,
        color_continuous_scale=colour_scale,
        mapbox_style="carto-darkmatter",
        hover_name=hover_name,
        hover_data=hover_data,
        labels=field_labels,
        opacity=0.25,
        title=title,
        height=800,
        width=800,
        center={"lat": 55.36274150310406, "lon": -3.440547563580056},
        zoom=4.5,
    )

    fig_choropleth.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        showlegend=showlegend,
    )

    if legend_title:
        fig_choropleth.update_layout(legend_title_text=legend_title)

    return fig_choropleth
