# Event class testing
"""
To show off the event class, we will create an instance of the class with 
dummy data and test the functionality. 
"""

from backend.classes import EventUtils
from backend.classes import Event
from backend.api import data

features = data['features']
# print(features[0]['properties']['poly_C'])

my_event = Event(22, "Test Event", 5544, 1738366578452, "Fast", "Human",
                 "Human lit a cigarrete in a forest", "Restaurant worker smoked on his break and caused a fire", 30, 30, None)

# __str__() demonstration
print(my_event)
print()

# convert_date() demonstration
print(my_event.convert_date(my_event.CreateDate))
print()

# time_elapsed() demonstration
print(my_event.time_elapsed())
print()

# return_dict() demonstration
print(my_event.return_dict())
print()


# EventStack testing
"""
first, well create more dummy Event objects and store them in an array. The we will use EventUtils.load_stack() 
to load the array and instatiate a stack. 
"""
my_event1 = Event(22, "Test Event 1", 5544, 1738366578400, "Fast", "Human",
                  "Human lit a cigarrete in a forest", "Restaurant worker smoked on his break and caused a fire", 30, 30, None)

my_event2 = Event(23, "Test Event 2", 200, 1738366578431, "Fast", "Human",
                  "Human lit a cigarrete in a dumpster", "Police officer tossed a cigarrrete in a dumpster and caused a fire", 45, 40, None)

my_event3 = Event(24, "Test Event 3", 1509, 1738366578452, "Fast", "Human",
                  "Human lit a cigarrete in a cafe", "Cafe attendee lit a cigarette and caused a fire", 63, 50, None)

my_stack = EventUtils.load_stack([my_event1, my_event2, my_event3])

# testing basic stack functionality
print("Checking if stack is empty")
print(my_stack.isEmpty())
print()

print("Popping from the stack")
popped_event = my_stack.pop()
print(popped_event)
print("Length of stack after popping: " + str(my_stack.size()))
print()

print("Pushing to the stack")
my_stack.push(popped_event)
print("Length of stack after pushing: " + str(my_stack.size()))
print()

print("Peeking into the stack")
print(my_stack.peek())
print()

# special functionality of the EventStack class
print("get_by_ID() demonstration")
print(my_stack.get_by_ID(24))
print()

print("get_top_three() demonstration")
top_three = my_stack.get_top_three()
for x in top_three:
    print(x.IncidentName)
print()


# EventUtils testing
print(
    f"EventUtils.determine_priority() demo: {EventUtils.determine_priority(my_event1)}")
print()

feature = features[0]
print(
    f"EventUtils.get_coordinates() demo: {EventUtils.get_coordinates(feature)}")
print()


fires = EventUtils.load_fires(data)
print(f"EventUitls.load_fires() first element in array: \n{fires[0]}\n")
print(f"Size of array {len(fires)}")
print()

stats = EventUtils.get_stats(fires)
print(f"EventUtils.get_stats() demo: ")
print(f"Total number of fires: {stats['total_fires']}")
print(f"Total acres covered: {stats['total_acres']}")
print(f"Estimated supression cost: {stats['estimated_cost']}")
print()

test_fire = fires[0]
print(
    f"EventUtils.get_reverse_geocode() demo: {EventUtils.get_reverse_geocode(test_fire.InitialLatitude, test_fire.InitialLongitude)}")
