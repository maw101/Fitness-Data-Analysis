import gpxpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import gmplot
from math import sqrt, floor
from geopy import distance
import haversine

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

# plot longitude vs latitude graph
plt.plot(df['lon'], df['lat'])
plt.show()

# plot time vs elevation
fig, ax = plt.subplots()
ax.plot('ele', data=df)  # plot time against elevation
## setup titles
ax.set_title('Time vs Elevation')
ax.set_xlabel('Time')
ax.set_ylabel('Elevation')
## setup x axis labels
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # format timestamps to display hours and minutes only
loc = mdates.MinuteLocator(byminute=range(0, 61, 5), interval=1)  # add a tick every 5 minutes
ax.xaxis.set_major_locator(loc)  # set the tick locations
fig.autofmt_xdate()  # rotate x axis labels
plt.show()

# plot data over google map - will watermark 'for development purposes' this is as GM is no longer free
min_lat, max_lat, min_lon, max_lon = min(df['lat']), max(df['lat']), min(df['lon']), max(df['lon'])
googleMap = gmplot.GoogleMapPlotter(min_lat + (max_lat - min_lat) / 2, min_lon + (max_lon - min_lon) / 2, 16)
googleMap.plot(df['lat'], df['lon'], 'blue', edge_width=1)
googleMap.draw('gm_plot.html')

# calculate distance values - need to first transform data as distance between two GPS points is a spherical
#   line (NOT STRAIGHT). We will use two formulas Haversine and Vincenty.
distance_haversine = [0]
distance_vincenty = [0]
elevation_difference = [0]
time_difference = [0]
distance_haversine_no_elevation = [0]
distance_vincenty_no_elevation = [0]
distance_difference_haversine_2d = [0]
distance_difference_vincenty_2d = [0]