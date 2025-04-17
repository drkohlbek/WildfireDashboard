import requests

# intial API call, see https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-2025-interagency-fire-perimeters-to-date/about
API = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_YearToDate/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
response = requests.get(API)
data = response.json()
