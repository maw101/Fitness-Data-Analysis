import gpxpy
import pandas as pd

gpx_file = open('data/red_route_cycle.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

# point to data points
data = gpx.tracks[0].segments[0].points

start_position = data[0]
end_position = data[-1]

# setup dataframe
df = pd.DataFrame(columns=['lon', 'lat', 'ele', 'time'])  # create empty dataframe
for point in data:  # iterate over all data points adding them to the dataframe
    df = df.append({'lon': point.longitude, 'lat': point.latitude, 'ele': point.elevation, 'time': point.time},
                   ignore_index=True)

df.index = df.time

print(df.head())  # print head of dataframe for debug