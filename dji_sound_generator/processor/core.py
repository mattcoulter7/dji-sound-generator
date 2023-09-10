
import pandas as pd
import math
import numpy as np


def haversine(lat1, lon1, alt1, lat2, lon2, alt2):
    """
    Calculate the great-circle distance between two points
    on the Earth's surface, taking into account altitude.
    
    :param lat1: Latitude of the first point in degrees
    :param lon1: Longitude of the first point in degrees
    :param alt1: Altitude of the first point in meters
    :param lat2: Latitude of the second point in degrees
    :param lon2: Longitude of the second point in degrees
    :param alt2: Altitude of the second point in meters
    :return: Distance in meters
    """
    # Radius of the Earth in meters
    earth_radius = 6371000  # approximate value for mean radius
    
    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Calculate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dalt = alt2 - alt1
    
    # Haversine formula
    a = (math.sin(dlat/2)**2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Calculate distance
    distance = earth_radius * c
    
    # Add altitude difference
    distance += abs(dalt)
    
    return distance

def process(
    df: pd.DataFrame
) -> pd.DataFrame:
    df = df[0::10]  # reduce sample count to calculate speed over greater distances
    calculate_delta_time(df)
    map_coordinates(df)
    calculate_distances(df)
    calculate_speed(df)
    return df

def map_coordinates(df: pd.DataFrame):
    df['start_coord'] = df.apply(lambda row: (
        row['longitude'],
        row['latitude'],
        row['altitude']
    ), axis=1)
    df['end_coord'] = df.shift(-1)['start_coord']
    df['end_coord'].values[-1] = df['start_coord'].values[-1]

def calculate_delta_time(df: pd.DataFrame) -> None:
    df['endtime'] = df.shift(-1)['starttime']
    df['endtime'].values[-1] = df['starttime'].values[-1]
    df['delta_time'] = (df['endtime'] - df['starttime']) / np.timedelta64(1, 's')

def calculate_distances(df: pd.DataFrame) -> None:
    df['distance'] = df.apply(lambda row: haversine(
        lat1=row['start_coord'][0],
        lon1=row['start_coord'][1],
        alt1=row['start_coord'][2],
        lat2=row['end_coord'][0],
        lon2=row['end_coord'][1],
        alt2=row['end_coord'][2],
    ), axis=1)
    pass

def calculate_speed(df: pd.DataFrame):
    df['speed'] = df['distance'] / df['delta_time']
