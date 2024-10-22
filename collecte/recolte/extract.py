import pandas as pd

class DataExtractor:
    def __init__(self, csv_file, json_file):
        self.csv_file = csv_file
        self.json_file = json_file

    def filter_csv_data(self, date, output_file):
        data = pd.read_csv(self.csv_file)
        filtered_data = data[data['Departure'].str.startswith(date)]
        selected_columns = filtered_data[['Departure', 'Departure station', 'Return station']]
        selected_columns.to_csv(output_file, index=False)

    def extract_coordinates_from_json(self):
        data = pd.read_json(self.json_file)
        def extract_coordinates(loc):
            if isinstance(loc, dict) and 'coordinates' in loc and loc['coordinates'] is not None:
                if len(loc['coordinates']) == 2:
                    return pd.Series([loc['coordinates'][1], loc['coordinates'][0]])
            return pd.Series([None, None])

        data[['latitude', 'longitude']] = data['location'].apply(extract_coordinates)
        data = data.dropna(subset=['latitude', 'longitude'])
        return data
