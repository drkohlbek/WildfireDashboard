from backend.classes import *
import requests
from dash import Dash, html, dash_table, dcc

# intial API call, see https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-2025-interagency-fire-perimeters-to-date/about
API = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_YearToDate/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
response = requests.get(API)
data = response.json()

fires = EventUtils.load_fires(data)

# Delete eventually
fires_dict = [event.return_dict() for event in fires]
df = pd.DataFrame(fires_dict)

# Initialize Dash app
app = Dash()

# App layout
app.layout = [
    html.Div(children='Hello World'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=EventUtils.plot_map(fires))
]

if __name__ == '__main__':
    app.run(debug=True)
