# Middleware file to instantiate data that will be passed to app.py and it's pages

from backend.classes import *
from backend.api import data

# Array of fire objects
fires = EventUtils.load_fires(data)

# Map figure
figure = EventUtils.plot_map(fires)

# Statistics
stats = EventUtils.get_stats(fires)

# Stack of fires
stack = EventUtils.load_stack(fires)

# Dict representation of fires in stack
fires_dict = reversed([event.return_dict() for event in stack.events])

# Top three fires
top_three = stack.get_top_three()
