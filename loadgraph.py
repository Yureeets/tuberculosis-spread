import osmnx as ox
import pandas as pd
import os

cities_data = {
    "Kyiv, Ukraine": {"lat": 50.4501, "lon": 30.5234, "population": 2967360},
    "Lviv, Ukraine": {"lat": 49.8397, "lon": 24.0297, "population": 717803},
    "Kharkiv, Ukraine": {"lat": 49.9935, "lon": 36.2304, "population": 1430885},
    "Odesa, Ukraine": {"lat": 46.4825, "lon": 30.7233, "population": 1011579},
    "Dnipro, Ukraine": {"lat": 48.4647, "lon": 35.0462, "population": 968502},
    "Donetsk, Ukraine": {"lat": 48.0159, "lon": 37.8029, "population": 905364},
    "Zaporizhzhia, Ukraine": {"lat": 47.8388, "lon": 35.1390, "population": 722713},
    "Vinnytsia, Ukraine": {"lat": 49.2328, "lon": 28.4820, "population": 370834},
    "Mykolaiv, Ukraine": {"lat": 46.9750, "lon": 31.9946, "population": 475599},
    "Ivano-Frankivsk, Ukraine": {"lat": 48.9221, "lon": 24.7105, "population": 237686},
    "Uzhhorod, Ukraine": {"lat": 48.6206, "lon": 22.3034, "population": 115317},
    "Sumy, Ukraine": {"lat": 50.9073, "lon": 34.7980, "population": 266535},
    "Chernihiv, Ukraine": {"lat": 51.4913, "lon": 31.2890, "population": 286899},
    "Poltava, Ukraine": {"lat": 49.5882, "lon": 34.5514, "population": 283402},
    "Khmelnytskyi, Ukraine": {"lat": 49.4202, "lon": 26.9990, "population": 274582},
    "Chernivtsi, Ukraine": {"lat": 48.2923, "lon": 25.9358, "population": 267060},

    "Lisbon, Portugal": {"lat": 38.7169, "lon": -9.1390, "population": 544851},
    "Copenhagen, Denmark": {"lat": 55.6761, "lon": 12.5683, "population": 1346048},
    "Stockholm, Sweden": {"lat": 59.3293, "lon": 18.0686, "population": 975551},
    "Helsinki, Finland": {"lat": 60.1699, "lon": 24.9384, "population": 656250}
}

output_dir = 'graph'
os.makedirs(output_dir, exist_ok=True)


def save_graph(place_name):
    filename = os.path.join(output_dir, f"{place_name.split(',')[0].lower()}.csv")
    if not os.path.exists(filename):
        graph = ox.graph_from_place(place_name, network_type='walk')
        gdf_nodes = ox.graph_to_gdfs(graph, nodes=True, edges=False)
        gdf_nodes.to_csv(filename)
        print(f"Saved: {filename}")
    else:
        print(f"Already exists: {filename}")


for city in cities_data.keys():
    save_graph(city)

combined_csv = os.path.join(output_dir, "combined_graph.csv")

csv_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.csv')]

if not csv_files:
    print("No CSV files found in the directory to concatenate.")
else:
    combined_df = pd.concat([pd.read_csv(csv_file).iloc[::10] for csv_file in csv_files], ignore_index=True)

    combined_df.to_csv(combined_csv, index=False)
    print(f"Combined CSV saved as: {combined_csv}")

