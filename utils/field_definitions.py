metric_area_fields = {
    "Number of Planning Applications": {
        "Number": {
            "field": "number_of_applications",
            "display_name": "Number of Planning Applications",
        },
        "Per Capita": {
            "field": "applications_per_capita",
            "display_name": "Number of Planning Applications per Capita",
        },
        "Per Square Kilometre": {
            "field": "applications_per_km2",
            "display_name": "Number of Planning Applications per Square Kilometre",
        },
    },
    "Total Fee": {
        "Number": {"field": "total_fee", "display_name": "Total Fee"},
        "Per Capita": {
            "field": "total_fee_per_capita",
            "display_name": "Total Fee per Capita",
        },
        "Per Square Kilometre": {
            "field": "total_fee_per_km2",
            "display_name": "Total Fee per Square Kilometre",
        },
    },
}

metric_single_fields = {
    "Number of Planning Applications": {
        "number": "number_of_applications",
        "readable": "readable_number",
    },
    "Total Fee": {"number": "total_fee", "readable": "readable_fee"},
}
