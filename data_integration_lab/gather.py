import pandas as pd

#1. Gather the input datat
#2. Read and Trimp
# Read the CSV files into DataFrames
#A.read the three CSV files into individual DataFrames using  pandas.read_csv(). We will refer to these three DataFrames as cases_df, deaths_df and census_df respectively.
cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
census_df = pd.read_csv('acs2017_county_data.csv')

#B. Trim cases_df and deaths_df to only the needed columns: County Name, State and 2023-07-23.  2023-07-23 is the last column in each and provides the final cumulative data available for COVID cases and deaths for each countyTrim cases_df and deaths_df to only the needed columns: County Name, State and 2023-07-23.  2023-07-23 is the last column in each and provides the final cumulative data available for COVID cases and deaths for each county
# Trim to relevant columns
cases_df = cases_df[['County Name', 'State', '2023-07-23']]
deaths_df = deaths_df[['County Name', 'State', '2023-07-23']]

#rename columns
cases_df.rename(columns={'2023-07-23': 'Cases'}, inplace=True)
deaths_df.rename(columns={'2023-07-23': 'Deaths'}, inplace=True)

#C. Trim census_df so that only these columns remain: County, State, TotalPop, IncomePerCap, Poverty, Unemployment
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

#remane columns to match other data
census_df.rename(columns={'County': 'County Name'}, inplace=True)

#D. Show the list of column headers for cases_df, deaths_df and census_df
print("cases_df columns:", cases_df.columns.tolist())
print("deaths_df columns:", deaths_df.columns.tolist())
print("census_df columns:", census_df.columns.tolist())

#3. Integration Challenge #1
#Unfortunately, each county name listed in cases_df and deaths_df contains an extra space character at the end. This extra space complicates integrating the data with the county names listed in the census data. 

#A. Remove this trailing space in every county name.
cases_df['County Name'] = cases_df['County Name'].str.strip()
deaths_df['County Name'] = deaths_df['County Name'].str.strip()

#B. Test by searching for County Name == “Washington County” (without the trailing space) in both DataFrames.
washington_cases = cases_df[cases_df['County Name'] == 'Washington County']
washington_deaths = deaths_df[deaths_df['County Name'] == 'Washington County']

#C. How many counties are named “Washington County”?
print("Washington County in cases_df:", len(washington_cases))
print("Washington County in deaths_df:", len(washington_deaths))

#4. Integration Challenge #2
#Another issue with cases_df and deaths_df is that they contain counties that do not exist. Each one is named “Statewide Unallocated”, and both DataFrames contain one of these for each state.
 
#A. Remove these unneeded records from cases_df and deaths_df
# Remove "Statewide Unallocated" entries
cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']

#B. How many rows remain in each DataFrame?
print("Remaining rows in cases_df:", len(cases_df))
print("Remaining rows in deaths_df:", len(deaths_df))

#5. Integration Challenge #3 
#All three DataFrames need to agree on how to name counties and states. The county names already seem to be in agreement, but the state names are not. cases_df and deaths_df use state abbreviations whereas census_df uses full state names. 

# A. Modify cases_df and deaths_df so that they each use full state names as well. Use this public domain code to help with this step: us_state_abbrev.py 
us_state_abbrev = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
}
cases_df['State'] = cases_df['State'].map(us_state_abbrev)
deaths_df['State'] = deaths_df['State'].map(us_state_abbrev)


# B. Show the first few rows of cases_df (show the output of cases_df.head()) 
print(cases_df.head())

#6. Integration Challenge #4 
#Joining these three data sets will only work if they have matching key columns, i.e., columns that have unique, non-null values that can also be used as foreign key references across each pairwise combination of DataFrames. None of the current columns is unique, so you need to make matching key columns in all three DataFrames. 

# A. Create a column named “key” that is a simple string concatenation of the County and State columns. 
cases_df['key'] = cases_df['County Name'] + ', ' + cases_df['State']
deaths_df['key'] = deaths_df['County Name'] + ', ' + deaths_df['State']
census_df['key'] = census_df['County Name'] + ', ' + census_df['State']

# B. Use DataFrame.set_index() to set “key” as the index of each DataFrame. 
cases_df.set_index('key', inplace=True)
deaths_df.set_index('key', inplace=True)
census_df.set_index('key', inplace=True)

# C. Show the first few rows of census_df (show the output of census_df.head()) 
print(census_df.head())

#7. Integration Challenge #5 
# Both cases_df and deaths_df have a column named 2023-07-23. In cases_df this column indicates the final cumulative count of confirmed COVID cases for each county, and in deaths_df this column indicates the final cumulative count of COVID deaths. 

# A. Change this confusing column name to Cases in cases_df and Deaths in deaths_df
# ***already changed***

# B. Show the resulting list of column headers for both cases_df and deaths_dft (e.g., show the output of cases_df.columns.values.tolist())
print("cases_df columns:", cases_df.columns.tolist())
print("deaths_df columns:", deaths_df.columns.tolist())


#8. Do the Integration

# A. Next, integrate the three DataFrames with two calls to DataFrame.join() . We will refer to the new, joined DataFrame as join_df . 
# Drop overlapping columns from deaths_df and census_df before joining
deaths_df_clean = deaths_df.drop(columns=['County Name', 'State'])
census_df_clean = census_df.drop(columns=['County Name', 'State'])

# Join the cleaned DataFrames
join_df = cases_df.join(deaths_df_clean).join(census_df_clean)


# B. Add two new columns to join_df called CasesPerCap and DeathsPerCap which represent the number of Cases and Deaths (respectively) in each county divided by the population (TotalPop) of the county.
join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']

# C. How many rows does join_df contain?
print("Rows in join_df:", len(join_df))

#9. Analyze
#Construct a correlation matrix among the numeric columns of join_df using DataFrame.corr(). This will show strength of correlation (either positive or negative) between every pair of variables. 
correlation_matrix = join_df.corr(numeric_only=True)
print(f"correlation matrix:")
print(correlation_matrix)

#10. Visualize
#Create a heatmap of the correlation_matrix (the value returned by join_df.corr()) , like this:

import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

plt.title('Correlation Matrix Heatmap')
plt.show()

'''
# Step 10 - Visualize

import seaborn as sns
import matplotlib.pyplot as plt

# Compute the correlation matrix
correlation_matrix = join_df.corr(numeric_only=True)

# Create heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.show()
'''
