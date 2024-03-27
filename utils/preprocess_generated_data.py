import json
import pandas as pd
import geopandas as gpd
from numerize.numerize import numerize
from tqdm import tqdm


def preprocess_generated_data(input_json, output_json):

    with open(input_json, "r") as fi:
        generated_data = json.load(fi)

    data_df = pd.DataFrame(generated_data)

    # Preprocess the data

    data_df["submission_date"] = pd.to_datetime(
        data_df["submission_date"], format="ISO8601"
    )
    data_df["application_type"] = data_df.apply(
        lambda row: row["application_type"].replace(
            "Planning permission", "Planning Permission"
        ),
        axis=1,
    )

    application_categories = [
        "Planning Permission",
        "Full Planning Permission",
        "Consent",
        "Permission in Principle",
        "Lawful Development Certificate",
        "Notice",
        "Prior Approval",
        "Outline Planning Permission",
    ]

    application_category_map = {}

    for application_type in set(data_df["application_type"]):
        for application_category in application_categories:
            if (
                application_type.strip()[: len(application_category)]
                == application_category
            ):
                application_category_map[application_type] = application_category

    data_df["application_category"] = data_df.apply(
        lambda row: application_category_map[row["application_type"]], axis=1
    )

    display_gdf = gpd.GeoDataFrame(
        data=data_df,
        geometry=gpd.points_from_xy(
            data_df.longitude,
            data_df.latitude,
            crs="EPSG:4326",
        ),
        crs="EPSG:4326",
    )

    display_gdf.sort_values(
        by=["application_category", "application_type"], ascending=True, inplace=True
    )

    display_gdf["readable_fee"] = display_gdf.apply(
        lambda row: numerize(row["fee"], 2), axis=1
    )

    display_gdf.to_file(output_json)


def create_area_data(area_gdf, preprocessed_json, output_json):

    preprocessed_gdf = gpd.read_file(preprocessed_json)

    area_gdf["number_of_applications"] = 0
    area_gdf["total_fee"] = 0.0

    for row_area in tqdm(area_gdf.itertuples(), total=len(area_gdf)):

        for row_application in preprocessed_gdf.itertuples():

            if not row_area.geometry.contains(row_application.geometry):
                continue

            area_gdf.at[row_area.Index, "number_of_applications"] += 1
            area_gdf.at[row_area.Index, "total_fee"] += row_application.fee

    area_gdf["applications_per_capita"] = (
        area_gdf["number_of_applications"] / area_gdf["LPA_population"]
    )
    area_gdf["applications_per_km2"] = (
        area_gdf["number_of_applications"] / area_gdf["LPA_area_km2"]
    )

    area_gdf["total_fee_per_capita"] = (
        area_gdf["total_fee"] / area_gdf["LPA_population"]
    )
    area_gdf["total_fee_per_km2"] = area_gdf["total_fee"] / area_gdf["LPA_area_km2"]

    area_gdf.to_file(output_json)


if __name__ == "__main__":

    LPA_json = "geo_data/LPA_census_2021_population.geojson"

    LPA_gdf = gpd.read_file(LPA_json).to_crs("EPSG:4326")

    for i in tqdm(range(1, 11)):

        raw_generated_json = f"generated_data/01_raw/generated_data_{i}.json"
        preprocessed_json = f"generated_data/02_preprocessed/preprocessed_data_{i}.json"
        area_json = f"generated_data/03_area/area_{i}.json"

        preprocess_generated_data(raw_generated_json, preprocessed_json)

        create_area_data(
            area_gdf=LPA_gdf, preprocessed_json=preprocessed_json, output_json=area_json
        )
