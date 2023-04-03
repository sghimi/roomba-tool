import json
import matplotlib.pyplot as plt

# Load the JSON data
with open('map.json') as f:
    data = json.load(f)

border_nums = data['umf']['maps'][0]['borders'][0]['geometry']['ids']
border_layer = data['umf']['maps'][0]['points2d']

# Create a dictionary mapping border IDs to coordinates
id_to_coord = {}
for point in border_layer:
    id_to_coord[point['id']] = point['coordinates']

# Get the coordinates associated with border_nums IDs
border_coords = [id_to_coord[id] for id in border_nums[0]]




# Loop through all layers in the map
for layer in data['umf']['maps'][0]['layers']:
    
    # Check the layer type and get the corresponding coordinates
    if layer['layer_type'] == 'coverage':
        coverage_layer = layer['geometry']['coordinates']

    elif layer['layer_type'] == 'coverage_poly':
        coverage_poly_layer = layer['geometry']['coordinates']
        coverage_poly_layer = coverage_poly_layer[0][0] # Get the first set of coordinates


        print('Coverage poly layer coordinates:', coverage_poly_layer)

print("cov layer\n\n",coverage_layer)
print ("cov_poly\n\n",coverage_poly_layer)
print("border \n\n",border_nums)
print("border \n\n",border_coords)


# Create a figure and axes
fig, ax = plt.subplots()

# Plot the border coordinates
x, y = zip(*border_coords)
ax.plot(x, y,label='Border')

# Plot the coverage layer coordinates
x, y = zip(*coverage_poly_layer)
ax.scatter(x, y, label='Coverage')



# Show the plot
plt.show()

