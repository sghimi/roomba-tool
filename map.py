import json
import matplotlib.pyplot as plt

# Load the JSON data
with open('map.json') as f:
    data = json.load(f)

# Extract the coverage layer coordinates
layer = [l for l in data['umf']['maps'][0]['layers'] if l['layer_type'] == 'coverage'][0]
coordinates = layer['geometry']['coordinates']

# Plot the coordinates
x = [c[0] for c in coordinates]
y = [c[1] for c in coordinates]
plt.plot(x, y, 'o')
plt.show()
