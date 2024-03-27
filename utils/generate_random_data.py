import random
import time
import pandas as pd
import geopandas as gpd
import json
from tqdm import tqdm


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, time_format):
    return str_time_prop(start, end, time_format, random.random())


"""
{
    "application_type": "pp.full.householder",
    "fee": 206,
    "fee_reduction": {
        "sports": true,
        "parishCouncil": true,
        "alternative": true
    },
    "applicant_type": "individual",
    "latitude": 51.4656522,
    "longitude": -0.1185926,
    "local_authority_district": [
        "Lambeth"
    ],
    "region": "London",
    "property_type": "residential.dwelling.house.terrace",
    "project_type": "extend.roof.dormer",
    "submission_date": "2023-10-02T00:00:00.00Z"
}
"""

# lower left: 50.930336462296516, -2.3574318068125324
# upper right: 52.735514499381004, 0.3884830933951188

application_type_descriptions = []
application_type_values = []

schema_file = f"schema/schema_v0.4.0.json"

with open(schema_file) as schema_json_file:
    schema_dict = json.load(schema_json_file)

for obj in schema_dict["definitions"]["ApplicationType"]["anyOf"]:
    description = obj["properties"]["description"]["const"]
    value = obj["properties"]["value"]["const"]
    application_type_descriptions.append(description)
    application_type_values.append(value)

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

application_category_types = {category: [] for category in application_categories}

for application_type in set(application_type_descriptions):
    for application_category in application_categories:
        if (
            application_type.strip()[: len(application_category)]
            == application_category
        ):
            application_category_types[application_category].append(application_type)


def generate_random_application(
    date_range=("2023-01-01", "2023-12-31"),
    date_format="%Y-%m-%d",
    # latitude_range = (50.930336462296516, 52.735514499381004 ),
    # longitude_range = (-2.3574318068125324, 0.3884830933951188),
    fee_range=(200, 400000),
    application_types=application_type_descriptions,
    boundary_gdf=None,
    boundary_geometry=None,
):

    fee_mu = (fee_range[0] - fee_range[1]) * 0.25 + fee_range[0]
    fee_sigma = (fee_range[0] - fee_range[1]) * 0.25

    fee = fee_range[0] - 1
    while fee < fee_range[0] or fee > fee_range[1]:
        fee = int(random.normalvariate(mu=fee_mu, sigma=fee_sigma))

    boundary_row = boundary_gdf.sample(n=1).iloc[0]

    boundary_geometry = boundary_row.geometry
    boundary_name = boundary_row.LPA21NM

    min_x, min_y, max_x, max_y = boundary_geometry.bounds

    point_geometry = gpd.points_from_xy(x=[min_x - 1], y=[min_y - 1])[0]

    while not boundary_geometry.contains(point_geometry):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        point_geometry = gpd.points_from_xy(x=[x], y=[y])

    application_category = random.choice(list(application_category_types.keys()))
    application_type = random.choice(application_category_types[application_category])

    return {
        "application_type": application_type,
        "fee": fee,
        "latitude": y,
        "longitude": x,
        "submission_date": random_date(date_range[0], date_range[1], date_format),
        "local_planning_authority": boundary_name,
    }


def generate_application_dataframe(n):

    return pd.DataFrame([generate_random_application() for _ in range(n)])


def write_random_data_rows_multi(n_files, n):

    boundary_geojson = "geo_data/Local_Planning_Authorities_May_2021_UK_BFE_2022_8497080629868369416.geojson"

    print("Reading boundary geometry...")
    boundary_gdf = gpd.read_file(boundary_geojson).to_crs("EPSG:4326")
    # print('Calculating boundary unary union...')
    # boundary_geometry = boundary_gdf.geometry.unary_union

    for i in range(1, n_files + 1):

        out_json = f"generated_data/01_raw/generated_data_{i}.json"

        applications = []

        for _ in tqdm(range(n)):
            application = generate_random_application(boundary_gdf=boundary_gdf)
            applications.append(application)

        with open(out_json, "w") as fo:
            json.dump(applications, fo)


if __name__ == "__main__":
    write_random_data_rows_multi(10, 1000)
