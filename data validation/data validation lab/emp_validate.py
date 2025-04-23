#Arlyss West CS410 data engineering 
#data validation Lab "emp_validate.py"

import csv #handle reading cvs files
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro

#2.Existance Assertion
#Assertion: every record has a non-null name field
#Write a python program called emp_validate.py (or something similar) that validates this assertion. The program should just count rows that do not satisfy this assertion. No need to modify or delete the invalid records. 
#How many records violate this assertion? -> 19
def validate_file(file_path):
    invalid_count = 0
# Open the CSV file in read mode
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Read each row as a dictionary

        for row in reader:
            name = row.get("name")  # Get the value of the 'name' field

            # Check for None, empty string, whitespace-only, or literal "null"
            if name is None or name.strip() == "" or name.strip().lower() == "null":
                invalid_count += 1  # Increment if name is invalid
    
    return invalid_count

#Define a new, different Existence Assertion
def validate_phone_existence(file_path):
    df = pd.read_csv(file_path)
    
    # Check if 'phone' column exists
    if 'phone' not in df.columns:
        print("Warning: 'phone' column is missing.")
        return 0  # Return 0 or an appropriate value if the column is missing
    
    # Check for null or empty phone values
    invalid_phones = df['phone'].isnull() | df['phone'].astype(str).str.strip().eq("")
    return invalid_phones.sum()

#3. Limit Assertion
#assertion: every employee was hired no earlier than 2015
#Add code to your program to validate this assertion 
#How many records violate this assertion? -> 18
# Ensure hire_date is datetime
def validate_hire_date(file_path):
    """
    Validates employee hire dates from a CSV file.

    - Checks how many were hired before 2015.
    - Returns the number of violations.

    Parameters:
    - file_path (str): Path to the employee CSV file.

    Returns:
    - int: Number of hire date violations (before 2015).
    """
    # ✅ Read CSV into DataFrame
    df = pd.read_csv(file_path)

    # ✅ Convert 'hire_date' to datetime
    df['hire_date'] = pd.to_datetime(df['hire_date'])

    # ✅ Find violations
    violations = df[df['hire_date'] < pd.Timestamp('2015-01-01')]

    return len(violations)

#Define a new, different Limit Assertion
#Salaries must be between $30,000 and $200,000
def validate_salary_range(file_path):
    df = pd.read_csv(file_path)
    violations = df[(df['salary'] < 30000) | (df['salary'] > 200000)]
    return len(violations)


#4. Intra-record Assertion
#Assertion: each employee was born before they were hired
#Add code to your program to validate this assertion
#How many records violate this assertion?
def validate_birth_before_hire(file_path):
    """
    Validates that each employee's birth_date is before their hire_date.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - int: Number of violations.
    - DataFrame: Rows that violate the assertion.
    """
    df = pd.read_csv(file_path)

    # Convert both columns to datetime
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df['hire_date'] = pd.to_datetime(df['hire_date'])

    # Find violations
    violations = df[df['birth_date'] >= df['hire_date']]

    #return len(violations), violations
    return len(violations)

#Define a new, different Intra-record Assertion
#Age at hire must be between 18 and 65
def validate_age_at_hire(file_path):
    df = pd.read_csv(file_path)
    df['birth_date'] = pd.to_datetime(df['birth_date'])
    df['hire_date'] = pd.to_datetime(df['hire_date'])
    df['age_at_hire'] = (df['hire_date'] - df['birth_date']).dt.days / 365.25
    violations = df[(df['age_at_hire'] < 18) | (df['age_at_hire'] > 65)]
    return len(violations)

#5. Inter-record Assertion
#Assertion: each employee has a manager who is a known employee
#Add code to your program to validate this assertion
#How many records violate this assertion?
# Assertion: Each employee's manager ID must exist as another employee ID
def validate_manager_ids(file_path):
    df = pd.read_csv(file_path)
  # Validate the assertion: Each employee has a manager who is a known employee
    invalid_records = df[~df['reports_to'].isin(df['eid'])]

# Count the number of records violating the assertion
    #violating_count = invalid_records.shape[0]
    violating_count = len(invalid_records)

    print(f"Number of records violating the assertion: {violating_count}")

#Define a new, different Inter-record Assertion
# New Inter-record Assertion: 
def validate_salary_against_manager(df):
    # Merge the employee dataset with itself to compare salaries
    merged_df = df.merge(df, left_on='reports_to', right_on='eid', suffixes=('', '_manager'))
    
    # Validate the assertion: employee's salary must be >= manager's salary
    invalid_salary_records = merged_df[merged_df['salary'] < merged_df['salary_manager']]
    
    # Count the number of records violating the new assertion
    violating_salary_count = invalid_salary_records.shape[0]
    
    return violating_salary_count

#6. Summary Assertion
#Assertion: each city has more than one employee
#Add code to your program to validate this assertion
#Is the data set valid with respect to this assertion? 
def validate_city_summary(file_path):
    """
    Validates the summary assertion:
    - Each city must have more than one employee.

    Returns:
    - int: Number of cities that violate the assertion.
    - list: Names of those cities.
    """
    df = pd.read_csv(file_path)

    # Group by city and count employees
    city_counts = df['city'].value_counts()

    # Find cities with only 1 employee
    violating_cities = city_counts[city_counts <= 1]

    #return len(violating_cities), list(violating_cities.index)
    return len(violating_cities)

#Define a new, different Summary Assertion
# New Summary Assertion: Each department has at least 5 employees
def validate_department_summary(file_path):
    df = pd.read_csv(file_path)
    dept_counts = df['title'].value_counts()
    violating_departments = dept_counts[dept_counts < 5]
    #return len(violating_departments), list(violating_departments.index)
    return len(violating_departments)

#7. Statistical Assertion
#Assertion: the salaries are normally distributed
#Add code to your program to validate this assertion
#Is the data set valid with respect to this assertion? For this show a screenshot of a histogram of salaries and state whether the histogram appears to resemble a normal distribution.
def validate_salary_distribution(file_path):
    """
    Validates if the 'salary' column is normally distributed using:
    - Histogram for visual check
    - Shapiro-Wilk test for normality (suitable for <5000 samples)

    Returns:
    - str: Shapiro-Wilk test result
    - bool: True if normally distributed, False otherwise
    """
    df = pd.read_csv(file_path)

    # Drop missing or invalid salary values
    salaries = df['salary'].dropna()

    # Plot histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(salaries, kde=True, bins=50, color='skyblue')
    plt.title('Histogram of Salaries')
    plt.xlabel('Salary')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('salary_histogram.png')  # Save for screenshot submission
    plt.show()

    # Shapiro-Wilk Test
    if len(salaries) > 5000:
        print("Sample too large for Shapiro-Wilk. Use D’Agostino’s test or sample the data.")
        sample = salaries.sample(5000, random_state=42)
    else:
        sample = salaries

    stat, p_value = shapiro(sample)

    if p_value > 0.05:
        result = "Salaries appear normally distributed (p = {:.4f})".format(p_value)
        is_normal = True
    else:
        result = "Salaries do NOT appear normally distributed (p = {:.4f})".format(p_value)
        is_normal = False

    return result, is_normal

#Define a new, different Statistical Assertion
#Standard deviation of salary must be under $50,000
def validate_salary_std(file_path):
    df = pd.read_csv(file_path)
    std_dev = df['salary'].std()
    is_valid = std_dev < 50000
    return std_dev, is_valid


#main - all problems
if __name__ == "__main__":

#1.  Call the validation function with the CSV file path
    #validate_file("employees.csv") 
    #file_path = "employees.csv"
    file_path = "/Users/arlysswest/Desktop/cs-410/data validation/data validation lab/employees.csv"
    df = pd.read_csv(file_path)

#2. EXISTANCE ASSERTATIONS
    #2.A. existance assertation: name validation count
    invalid_count = validate_file(file_path)
    print(f"Number of records with null or empty 'name': {invalid_count}")

    #2.B. new/different existance assertation
    invalid_phone_count = validate_phone_existence(file_path)
    print(f"Number of records with null or empty 'phone': {invalid_phone_count}")
    
#3. LIMIT ASSERTATIONS
    #3.A. limit assertation: validate hire date validation count
    invalid_hire_count = validate_hire_date(file_path)
    print(f"invalid hires(hired after 2015): {invalid_hire_count}")

    #3.B. new/different limit assertation
    print(f"Salaries outside $30k–$200k: {validate_salary_range(file_path)}")

#4. INTRA-RECORD ASSERTATIONS
    #4.A. intra-record assertation: births before hire date
    birth_hire_violations = validate_birth_before_hire(file_path)
    print(f"Births before hire violations: {birth_hire_violations}")

    #4.B. new/different intra-record assertation
    print(f"Invalid age at hire (not 18–65): {validate_age_at_hire(file_path)}")


#5. INTER-RECORD ASSERTATIONS
    #5.A. Inter-record Assertion
    violations = validate_manager_ids(file_path)
    print(f"employees who do not have a manager: {violations}")


    #5.B. new/different Inter-record Assertion
    violating_salary_count = validate_salary_against_manager(df)
    print(f"Number of records violating the salary assertion: {violating_salary_count}")

#6. SUMMARY ASSERTIONS
    #6.A. summary assertation 
    #cities, city_list = validate_city_summary(file_path)
    #print(f"Cities with ≤1 employee: {cities} — {city_list}")
    cities = validate_city_summary(file_path)
    print(f"Cities with ≤1 employee: {cities}")

    #6.B. new/different summary assertation
    #depts, dept_list = validate_department_summary(file_path)
    #print(f"Departments with <5 employees: {depts} — {dept_list}")
    depts = validate_department_summary(file_path)
    print(f"Departments with <5 employees: {depts}")


#7. STATISTICAL ASSERTATIONS
    #7.A. staistical assertaion
    result, is_normal = validate_salary_distribution(file_path)
    print(result)

    #7.B. new/different statistical assertation
    std, valid = validate_salary_std(file_path)
    print(f"Salary std dev: {std:.2f} — {'Valid' if valid else 'Too High'}")


#8. github
# class topics/labs repository: https://github.com/arlysswest/410-data_engineering-lab
# topic folder: https://github.com/arlysswest/410-data_engineering-lab/tree/main/data%20validation
# lab folder: https://github.com/arlysswest/410-data_engineering-lab/tree/main/data%20validation/data%20validation%20lab
# file: https://github.com/arlysswest/410-data_engineering-lab/blob/main/data%20validation/data%20validation%20lab/emp_validate.py