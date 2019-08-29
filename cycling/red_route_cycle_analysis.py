import gpxpy

gpx_file = open('data/red_route_cycle.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

# point to data points
data = gpx.tracks[0].segments[0].points

start_position = data[0]
end_position = data[-1]