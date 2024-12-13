from loadgraph import cities_data, output_dir
import pandas as pd
import os

all_nodes = {}
for city, coords in cities_data.items():
    filename = os.path.join(output_dir, f"{city.split(',')[0].lower()}.csv")
    city_data = pd.read_csv(filename, low_memory=False)
    all_nodes[city] = {
        "gdf_nodes": city_data.iloc[::5],
        "lat": coords["lat"],
        "lon": coords["lon"]
    }