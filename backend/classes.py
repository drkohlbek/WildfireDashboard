import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import reverse_geocode
import requests

# Using numbers from https://www.nifc.gov/fire-information/statistics/suppression-costs,
# the total cost per acre to suppress wildfires in 2023 was ~$1,177
COST_PER_ACRE = 1177

# Class definitions

# Class for wildifre events


class Event():

    """
    Class to store information about a wildfire event.

    See https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-2025-interagency-fire-perimeters-to-date/about
    for more information regarding the attributes of a wildfire event.

    Attributes
    ----------
    ID: int
      Unique ID for wildfire event
    IncidentName: str
      Name of wildfire event
    Acres: float
      Total aceres covered by fire of the event
    CreateDate: esriFieldTypeDate/int
      Date of event creation, eventually converted into Python datetime.datetime
    CurrentDate: datetime.datetime
      Date the program is run, aka the current date
    FireBehaviorGeneral: str
      General behavior of the fire (minimal, moderate, high)
    FireCause: str
      Cause (if known) of the fire
    FireCauseSpecific: str
      More specific cause of the fire
    IncidentShortDescription: str
      Short description of the fire
    Coordinates: list
      Coordinates in [Longitude, Lattitude], see EventUtils.get_coordinates() in the next cell
    InitialLatitude: float
      Initial latitude (if available) of the fire
    InitialLongitude: float
      Initial longitude (if available) of the fire
    POOCity: str
      Starting city of the fire (if available)
    POOCounty: str
      Starting county of the fire (if available)
    Priority: float
      Priority of the fire, see EventUtils.determine_priority() for more info.
      User is also able to set this value manually.

    Methods
    -------
    __init__(**atributes)
      init function
    __str__()
      returns basic information about wildfire event
    detailed_description()
      returns all information on wildfire event in string format
    convert_date(date)
      converts ersiFieldTypeDate to datetime.datetime object
      ref: https://pro.arcgis.com/en/pro-app/latest/help/mapping/time/convert-string-or-numeric-time-values-into-data-format.htm
    time_elapsed(self)
      returns time since start of fire
    return_dict()
      returns a dict representation of the object

    """

    def __init__(self, ID, IncidentName, Acres, CreateDate, FireBehaviorGeneral, FireCause, FireCauseSpecific, IncidentShortDescription, InitialLatitude, InitialLongitude, Priority=None):
        self.ID = int(ID)
        self.IncidentName = IncidentName
        self.Acres = Acres
        self.CreateDate = CreateDate
        self.CurrentDate = datetime.datetime.now()
        self.FireBehaviorGeneral = FireBehaviorGeneral
        self.FireCause = FireCause
        self.FireCauseSpecific = FireCauseSpecific
        self.IncidentShortDescription = IncidentShortDescription
        self.InitialLatitude = InitialLatitude
        self.InitialLongitude = InitialLongitude

        # Run reverse_geocode and extract location info
        location_info = EventUtils.get_reverse_geocode(
            InitialLatitude, InitialLongitude)
        if location_info != None:
            self.City = location_info["city"]
            self.State = location_info["state"]
            try:
                self.County = location_info["county"]
            except KeyError:
                self.County = None
        else:
            self.City = None
            self.State = None
            self.County = None

        # Allow user to overide priority
        if Priority != None:
            self.Priority = Priority
        else:
            self.Priority = EventUtils.determine_priority(self)

        # Determine estimated fire supression costs
        if self.Acres != None:
            self.Cost = self.Acres * COST_PER_ACRE
        else:
            self.Cost = None

    # return general information about the event in a string

    def __str__(self):
        return f"Information on wildfire {self.ID} in {self.City}, {self.State}:\n \
Incident Name: {self.IncidentName}\n Coverage in Acres: {self.Acres}\n Start Date: {self.convert_date(self.CreateDate)}\n Time Elapsed: {str(self.time_elapsed())}\n Fire Behavior: {self.FireBehaviorGeneral}\n Cause: {self.FireCause}\n Estimated Cost: {self.Cost}\n\n \
Description of the Incident:\n {self.IncidentShortDescription}"

    # TODO
    def detailed_description(self):
        return f"ID: {self.ID}, "

    # convert ersi date integer to datetime
    def convert_date(self, date):
        """
        convert_date converts ersiFieldTypeDate integer to datetime.datetime object
        ref: https://pro.arcgis.com/en/pro-app/latest/help/mapping/time/convert-string-or-numeric-time-values-into-data-format.htm
        """
        if date != None:
            return datetime.datetime.fromtimestamp((date/1000) - 18000)
        return None

    # return total time since fire began
    def time_elapsed(self):
        """
        time_elapsed() calculate and returns the time since the start of the wildfire
        """
        if self.CreateDate != None:
            return self.CurrentDate - self.convert_date(self.CreateDate)
        return None

    # return a dict representation of information stored in the object
    def return_dict(self):
        """
        return_dict() returns a dict representation of all the attributes of
        the object
        """
        return {
            'ID': self.ID,
            'IncidentName': self.IncidentName,
            'Acres': self.Acres,
            'CreateDate': self.convert_date(self.CreateDate),
            'CurrentDate': self.CurrentDate,
            'State': self.State,
            'City': self.City,
            'County': self.County,
            'Priority': self.Priority,
            'Estimated Cost': self.Cost,
            'InitialLatitude': self.InitialLatitude,
            'InitialLongitude': self.InitialLongitude,
            'FireBehaviorGeneral': self.FireBehaviorGeneral,
            'FireCause': self.FireCause,
            'FireCauseSpecific': self.FireCauseSpecific,
            'IncidentShortDescription': self.IncidentShortDescription,
        }

# Stack class to store wildfire events based on priority


class EventStack():
    def __init__(self):
        self.events = []

    def isEmpty(self):
        return self.events == []

    def push(self, item):
        self.events.append(item)

    def pop(self):
        return self.events.pop()

    def peek(self):
        return self.events[len(self.events)-1]

    def size(self):
        return len(self.events)

    # TODO: get element by ID function
    def get_by_ID(self, ID):
        for event in self.events:
            if event.ID == ID:
                return event.return_dict()

    def get_top_three(self):
        events = []
        events.append(self.events[-1])
        events.append(self.events[-2])
        events.append(self.events[-3])

        return events


class EventUtils():
    """
    Class that contains useful static methods used throughout the program.

    Attributes
    ----------
    None

    Methods
    -------
    __init__()
      init function
    determine_priority(feature) -> float
      Determines the priority of a wildfire event by calculating the ratio of acres
      to the time elapsed of a wildfire.
    get_coordinates(feature) -> list
      Gets the coordinates of a wildfire event by taking the mean value of the
      coordinates of the permiter of the event


    """

    def __init__(self):
        pass

    @staticmethod
    def determine_priority(event):
        """
        Determine priority of a wildfire event by measureing the ratio of acres
        to time elapsed of a wildfire; a higher ratio means a higher priorty.

        Priority index = acres / time elapsed (seconds)

        For cases where their is no entry for CreateDate, return the number of acres
        as the priority.

        For cases where there is no entry for Acres, return 0.
        """
        if event.Acres and event.time_elapsed():
            priority = event.Acres / event.time_elapsed().total_seconds()
            return priority
        elif event.Acres:
            return event.Acres
        return 0

    @staticmethod
    def get_coordinates(feature):
        """
        Get coordinates of a wildfire event by taking the mean value
        of the coordinates of the perimeter of the event.

        This is necessary since many enteries in the database do not have
        attr_InitialLatitude and attr_InitialLongitude values defined.

        Dimension of coordinate arrays is not consistent across all entries. There
        are some entries with multiple 2D arrays in them. A workaround for this is
        to only take the arrays with .ndim = 1 as shown below.
        """

        orig_coords = np.array(
            [x for x in feature['geometry']['coordinates'][0]])
        coords = orig_coords.mean(axis=0)

        if coords.ndim > 1:
            return coords[0]
        return coords

    @staticmethod
    def partition(fires, low, high):
        pivot = fires[high]
        i = low - 1

        for j in range(low, high):
            if fires[j].Priority <= pivot.Priority:
                i += 1
                fires[i], fires[j] = fires[j], fires[i]

        fires[i+1], fires[high] = fires[high], fires[i+1]
        return i+1

    def quicksort(fires, low=0, high=None):
        if high == None:
            high = len(fires) - 1

        if low < high:
            pi = EventUtils.partition(fires, low, high)
            EventUtils.quicksort(fires, low, pi-1)
            EventUtils.quicksort(fires, pi+1, high)

    @staticmethod
    def plot_map(fires):
        # Dict array of wildfire events for plotting
        fires_dict_array = [event.return_dict() for event in fires]
        # Store dict array in dataframe
        df = pd.DataFrame(fires_dict_array)

        df.fillna({'Acres': 0}, inplace=True)

        # Set custom size for each point on the map.
        # The size of each point will be the same as the acres covered, unless
        # it is less than 500, then the point size will be 500.
        df['size'] = df['Acres']

        for i in range(len(df)):
            if df.loc[i, "size"] < 500:
                df.loc[i, "size"] = 500

        # plot
        fig = px.scatter_map(df, lat=df["InitialLatitude"], lon=df["InitialLongitude"],
                             hover_name="IncidentName", hover_data={'ID': True, 'InitialLatitude': True, 'InitialLongitude': True, 'Acres': True, 'size': False}, color="Acres", zoom=3, size=df["size"], height=700)
        # setting renderer to notebook stops VScode from outputting a blank map, ref: https://community.plotly.com/t/new-plotly-express-scatter-map-not-working/87232/6
        return fig

    # Method to load fires from data into list
    @staticmethod
    def load_fires(data) -> list:
        fires = []
        for feature in data['features']:
            properties = feature['properties']

            # Only select wild fires, not prescribed fires
            if properties['poly_FeatureCategory'] != 'Prescribed Fire':
                coords = EventUtils.get_coordinates(feature)
                # event = Event(properties['OBJECTID'], properties['poly_IncidentName'], properties['poly_GISAcres'], properties['poly_CreateDate'], properties['poly_DateCurrent'], properties['attr_FireBehaviorGeneral'], properties['attr_FireCause'], properties['attr_FireCauseSpecific'], properties['attr_IncidentShortDescription'], EventUtils.get_coordinates(feature), properties['attr_InitialLatitude'], properties['attr_InitialLongitude'], properties['attr_POOCity'], properties['attr_POOCounty'])
                event = Event(ID=properties['OBJECTID'], IncidentName=properties['poly_IncidentName'], Acres=properties['poly_GISAcres'], CreateDate=properties['poly_CreateDate'], FireBehaviorGeneral=properties['attr_FireBehaviorGeneral'],
                              FireCause=properties['attr_FireCause'], FireCauseSpecific=properties['attr_FireCauseSpecific'], IncidentShortDescription=properties['attr_IncidentShortDescription'], InitialLatitude=coords[1], InitialLongitude=coords[0])
                fires.append(event)
        return fires

    @staticmethod
    def load_stack(fires) -> EventStack:
        stack = EventStack()
        EventUtils.quicksort(fires)

        for event in fires:
            stack.push(event)

        return stack

    @staticmethod
    def get_stats(fires):
        stats = dict()

        # Total fires in array
        stats["total_fires"] = len(fires)

        # Total acerage covered
        total_acres = 0
        for event in fires:
            if event.Acres != None:
                total_acres += event.Acres
        stats["total_acres"] = round(total_acres)

        # Total estimated cost
        stats["estimated_cost"] = stats["total_acres"] * COST_PER_ACRE

        # Create histogram of acres covered by fire in the US
        """
        fig, ax = plt.subplots()

        acres_per_event = []
        for event in fires:
            acres_per_event.append(event.Acres)

        ax.hist(acres_per_event, bins=10)

        stats["figure"] = fig
        """
        return stats

    @staticmethod
    def get_reverse_geocode(lat, lon):
        """
        geolocator = Nominatim(user_agent="wildfires")
        location = geolocator.reverse(f"{lat}, {lon}", timeout=None)

        print(location.raw)
        """
        if lat != None and lon != None:
            coord = lat, lon
            return (reverse_geocode.get(coord))

        return None
