#Arlyss West
#CS-410 Data Engineering
#Detecting Bias Lab Assignment

import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import StringIO
from scipy.stats import binomtest
from scipy.stats import ttest_1samp

#%%
#1. Input Data
# "trimet_relpos_2022-12-07.csv"
# "trimet_stopevents_2022-12-07(1).html"
#2. Transform the Data
#The TriMet Stop Event data is in .html form. Use python, BeautifulSoup and pandas to transform it into one DataFrame (called stops_df) containing these columns: 
#trip_id, vehicle_number, tstamp, location_id, ons, offs
#The tstamp column should be a datetime value computed using the arrive_time column in the stop event data (arrive_time indicates seconds since midnight) 
#The DataFrame should contain 91932 stop events. 
# Load HTML stop event data
with open("trimet_stopevents_2022-12-07 (1).html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Extract table
table = soup.find_all("table")
df_raw = pd.read_html(StringIO(str(table)))

# Combine all the DataFrames into one
df_raw = pd.concat(df_raw, ignore_index=True)

# Rename and transform
df_raw.columns = [col.lower().strip() for col in df_raw.columns]
stops_df = df_raw[["trip_number", "vehicle_number", "arrive_time", "location_id", "ons", "offs"]].copy()


# Convert arrive_time to timestamp (assume date is 2022-12-07)
midnight = datetime(2022, 12, 7)
stops_df["tstamp"] = stops_df["arrive_time"].apply(lambda x: midnight + timedelta(seconds=int(x)))

# Ensure correct dtypes
stops_df["vehicle_number"] = stops_df["vehicle_number"].astype(str)
stops_df["location_id"] = stops_df["location_id"].astype(str)
#%%

#%%
# Final check
#assertation error?????
#assert stops_df.shape[0] == 91932 
num_stops= stops_df.shape[0]
if num_stops==91932:
    print("The number of stop events is 91932. This is what is expected")
else: 
    print(f"The number of stop events is {num_stops}. This is unexpected behavior")


#A. How many vehicles are contained in the data?
num_vehicles = stops_df["vehicle_number"].nunique()
print(f"number of vehicles contained in the data: {num_vehicles}")

#B. How many stop locations (how many unique values of location_id)?
num_locations = stops_df["location_id"].nunique()
print(f"number of stop locations: {num_locations}")

#C. Min and Max values of tstamp? 
min_tstamp = stops_df["tstamp"].min()
print(f"minimum valie of tstamp: {min_tstamp} ")
max_tstamp = stops_df["tstamp"].max()
print(f"maximum value of tstamp: {max_tstamp}")

#D. How many stop events at which at least one passenger boarded (stop events for which ons >= 1)?
stops_with_boardings = stops_df[stops_df["ons"] >= 1].shape[0]
print(f"stop events at which at least one passenger boarded: {stops_with_boardings} ")

#E. Percentage of stop events with at least one passenger boarding?
percent_boardings = (stops_with_boardings / stops_df.shape[0]) * 100
print(f"percentage of stop events with at least one passenger borading: {percent_boardings}")

#3. Validate
#A. For location 6913
location_df = stops_df[stops_df["location_id"] == "6913"]
print("3. Validation")
print ("A. Location 6913")
    #1. How many stops made at this location?
num_stops_location = location_df.shape[0]
print(f"There are {num_stops_location} stops at this location")
    #2. How many different buses stopped at this location?
unique_vehicles_location = location_df["vehicle_number"].nunique()
print(f"number of different buses stopped at this location: {unique_vehicles_location}")
    #3. For what percentage of stops at this location did at least one passenger board?
boarding_percent_location = (location_df[location_df["ons"] >= 1].shape[0] / num_stops_location) * 100
print(f"the perecentage of stops at this location where at least one passenger boarded: {boarding_percent_location}")
#B. For vehicle 4062:
print("B. Vehicle 4062")
vehicle_df = stops_df[stops_df["vehicle_number"] == "4062"]
    #1. How many stops made by this vehicle?
num_stops_vehicle = vehicle_df.shape[0]
print(f"stops made my this vehicle: {num_stops_vehicle}")
    #2. How many total passengers boarded this vehicle? 
total_boarded = vehicle_df["ons"].sum()
print(f"total passengers boarded this vehicle: {total_boarded}")
    #3. How many passengers deboarded this vehicle?
total_deboarded = vehicle_df["offs"].sum()

print(f"number of passengers deboarded this vehicle: {total_deboarded}")
    #4. For what percentage of this vehicle’s stop events did at least one passenger board?
if num_stops_vehicle != 0:
    boarding_percent_vehicle = (vehicle_df[vehicle_df["ons"] >= 1].shape[0] / num_stops_vehicle) * 100
    print(f"percentage of this vehicles stop events where at least one passenger boarded: {boarding_percent_vehicle}")

#%%
#4. Find vehicles with biased boarding data (“ons”)
#The “ons” column shows the number of passengers who boarded the bus during a stop event.  Use a binomial test to determine which (if any) buses have biased “ons” data. 
print("4. find vehicles with boased boarding data 'ons' ")
#A. For each bus in the system:
overall_prob = percent_boardings / 100
vehicle_bias_results = []
for vehicle, group in stops_df.groupby("vehicle_number"):
    total = group.shape[0]
    success = group["ons"].ge(1).sum()
    pval = binomtest(success, total, overall_prob).pvalue
    vehicle_bias_results.append((vehicle, pval))
    #1. count the number of stops events 
print(f"number of stops: {total}")
    #2. count the number of stop events for which the bus had at least one passenger board
print(f"number of stop events which the bus had at least one passenger on board: {success}")
    #3. determine the percentage of stop events with boardings.
percentage = success/total
print(f"percentage of stop events with boardings: {percentage}")
    #4. Use a binomial test to determine p, the probability that the observed proportion of stops-with-boardings might occur given the overall proportion of stops-with-boardings for the entire system (which you calculated in step 2E)
print(f"probability: {pval}")
#B. List the IDs of vehicles, and their corresponding p values, for vehicles having p values less than alpha=5% 
biased_boarding_vehicles = [(v, p) for v, p in vehicle_bias_results if p < 0.05]
print(f"ids of vehicles and thier corresponding p values: {biased_boarding_vehicles}")
#C. List at least three potential reasons or causes for such bias 
    #1. ???
    #2. ???
    #3. ???
#5. Find vehicles with biased GPS data
#The TriMet Relative Position Data indicates whether a vehicle’s GPS position was found to be left, right or exactly where it is predicted to be relative to the route being serviced by the vehicle. The data is a single floating point number (called ‘RELPOS’) that indicates whether the vehicle’s breadcrumb lat/lon coordinates were measured to be left (value < 0.0), right (value > 0.0) or exactly perfect (value == 0.0) at a given moment during the day. 
#Breadcrumb lat/lon locations might be left or right of expected locations due to various factors, but for an entire day, any irregularities should cancel out and the relative position values should average to near 0.0. Unfortunately, sometimes the data contains bias.
print("5. Find vehicles with biased gps data")
#A. For the entire data set:
    #1. store all RELPOS values for all vehicles as an array to be used in the t-test below
relpos_df = pd.read_csv("trimet_relpos_2022-12-07.csv")
all_relpos = relpos_df["RELPOS"].values

#B. For each vehicle in the system:
gps_bias_results = []

for vehicle, group in relpos_df.groupby("VEHICLE_NUMBER"):
    vehicle_relpos = group["RELPOS"].values
    if len(vehicle_relpos) > 1:  # avoid t-test on tiny samples
        pval = ttest_1samp(vehicle_relpos, popmean=all_relpos.mean()).pvalue
        gps_bias_results.append((vehicle, pval))
    #1. find all RELPOS values for the vehicle
print(f"RELPOS values: {vehicle_relpos}")
    #2. Use a t-test to determine the probability that the vehicle’s observed RELPOS values occurred given the (null hypothesis) that there is no bias in the data as compared to the RELPOS values for all vehicles.
print(f"probability that the vehicles observed replos values occured given the null hypothesis (null hypothesis) that there is no bias .... {pval}")
#C. List the IDs of vehicles (and their corresponding p values) having p < 0.005 
biased_gps_vehicles = [(v, p) for v, p in gps_bias_results if p < 0.005]
print(f"ids od vehicles and corresponding p values: {biased_gps_vehicles} ")
#D. List at least three potential reasons or causes for such bias  
#1. 
#2. 
#3. 

