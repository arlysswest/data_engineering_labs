import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Synthetic Employee Data

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Initialize Faker generators for different locales
locales = {
    'USA': 'en_US',
    'India': 'en_IN',
    'China': 'zh_CN',
    'Mexico': 'es_MX',
    'Canada': 'en_CA',
    'Philippines': 'en_PH',
    'Taiwan': 'zh_TW',
    'South Korea': 'ko_KR'
}

fakers = {country: Faker(locale) for country, locale in locales.items()}
Faker.seed(42)

# Country of birth distribution (based on 60% USA and 2019 H1B petition %)
country_distribution = {
    'USA': 0.60,
    'India': 0.26,
    'China': 0.09,
    'Mexico': 0.01,
    'Canada': 0.01,
    'Philippines': 0.01,
    'Taiwan': 0.01,
    'South Korea': 0.01
}
countries = list(country_distribution.keys())
weights = list(country_distribution.values())

# Gender distribution
genders = ['female', 'male', 'nonbinary']
gender_weights = [0.49, 0.49, 0.02]

# Dummy departments and roles (replace with actual data from the spreadsheet)
departments = {
    'Engineering': ['Software Engineer', 'DevOps Engineer'],
    'Sales': ['Sales Executive', 'Account Manager'],
    'HR': ['HR Specialist', 'Recruiter'],
    'Marketing': ['Marketing Manager', 'Content Strategist']
}
department_weights = [0.4, 0.3, 0.2, 0.1]  # Example distribution

# Salary ranges (replace with real values from the spreadsheet)
salary_ranges = {
    'Software Engineer': (80000, 150000),
    'DevOps Engineer': (85000, 140000),
    'Sales Executive': (50000, 100000),
    'Account Manager': (55000, 95000),
    'HR Specialist': (45000, 85000),
    'Recruiter': (50000, 90000),
    'Marketing Manager': (60000, 110000),
    'Content Strategist': (55000, 100000)
}

# Generate synthetic employee data
num_employees = 10000
employees = []

for i in range(num_employees):
    emp_id = random.randint(100_000_000, 999_999_999)

    country = random.choices(countries, weights=weights, k=1)[0]
    fake = fakers[country]

    name = fake.name()
    phone = fakers['USA'].phone_number()
    email = fake.email()
    gender = random.choices(genders, weights=gender_weights, k=1)[0]

    
    age = random.randint(20, 65)
    birthdate = datetime.today() - timedelta(days=age*365 + random.randint(0, 364))
    #min_hire_year = max(2010, birthdate.year + 20)
    #hiredate = datetime(min_hire_year, 1, 1) + timedelta(days=random.randint(0, 365 * (2024 - min_hire_year)))
    
    min_hire_year = max(2010, birthdate.year + 20)
    max_hire_year = min(2024, datetime.today().year)

    if min_hire_year > max_hire_year:
        hire_year = max_hire_year  # fallback to most recent valid year
    else:
        hire_year = random.randint(min_hire_year, max_hire_year)

    hiredate = datetime(hire_year, 1, 1) + timedelta(days=random.randint(0, 364))

    dept = random.choices(list(departments.keys()), weights=department_weights, k=1)[0]
    role = random.choice(departments[dept])
    salary_range = salary_ranges[role]
    salary = random.randint(salary_range[0], salary_range[1])

    ssid = fakers['USA'].ssn()

    employees.append({
        'employeeID': emp_id,
        'CountryOfBirth': country,
        'name': name,
        'phone': phone,
        'email': email,
        'gender': gender,
        'birthdate': birthdate.date(),
        'hiredate': hiredate.date(),
        'department': dept,
        'role': role,
        'salary': salary,
        'SSID': ssid
    })

# Create DataFrame
emp_df = pd.DataFrame(employees)

# Save to CSV
emp_df.to_csv('emp_df.csv', index=False)

#2. 
#A. Show a screenshot of the output of emp_df.describe(include=’all’)
twoA=emp_df.describe(include='all')
print(f"2.A output of emp_df.describe(include='all'): {twoA}")
#B. Show a screenshot of the output of emp_df.head(10)
twoB=emp_df.head(10)
print(f"2.B output of emp_df.head(10): {twoB}")
#C. How much will this company pay in yearly payroll?
twoC=emp_df['salary'].sum()
print(f"comoany pays in yearly payroll: ${twoC}")

#3. Provide screenshots of each of the following. Display each visualization on its own slide.
'''
#A. A bar chart displaying counts of each CountryOfBirth. Order the bars from most frequent country to least frequent.
print("3A.A bar chart displaying counts of each CountryOfBirth. Order the bars from most frequent country to least frequent." )
plt.figure(figsize=(10,6))
emp_df['CountryOfBirth'].value_counts().plot(kind='bar')
plt.title("Employees by Country of Birth")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("3A_country.png")
plt.show()
plt.close()
#B. A bar chart displaying employee counts for each Department. Order the bars from largest department to smallest.
print("3B. A bar chart displaying employee counts for each Department. Order the bars from largest department to smallest.")
plt.figure(figsize=(10,6))
emp_df['department'].value_counts().plot(kind='bar')
plt.title("Employees by Department")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("3B_department.png")
plt.show()
'''

#C. A bar chart with X axis of “day of the week” showing all seven days of the week. The Y axis represents the number of employees hired on each day of the week.
print("3C. A bar chart with X axis of “day of the week” showing all seven days of the week. The Y axis represents the number of employees hired on each day of the week.")
emp_df['hiredate'] = pd.to_datetime(emp_df['hiredate'])
emp_df['hire_day'] = emp_df['hiredate'].dt.day_name()
plt.figure(figsize=(10,6))
sns.countplot(x='hire_day', data=emp_df, order=[
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title("Hires by Day of the Week")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("3C_hireday.png")
plt.show()
'''
#D. A KDE plot of salaries
print("3D. A KDE plot of salaries")
plt.figure(figsize=(10,6))
sns.kdeplot(emp_df['salary'], fill=True)
plt.title("KDE of Salaries")
plt.xlabel("Salary")
plt.tight_layout()
plt.savefig("3D_kde_salary.png")
plt.show()
plt.close()
'''
'''
#E. A line plot showing number of birthdates over time. The X axis shows the years from earliest birth year to most recent, and the Y axis represents the number of employees born in each year.
print("3E. A line plot showing number of birthdates over time. The X axis shows the years from earliest birth year to most recent, and the Y axis represents the number of employees born in each year.")
emp_df['birth_year'] = pd.to_datetime(emp_df['birthdate']).dt.year
birth_counts = emp_df['birth_year'].value_counts().sort_index()
plt.figure(figsize=(12,6))
birth_counts.plot()
plt.title("Employees Born per Year")
plt.xlabel("Birth Year")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("3E_births.png")
plt.show()
plt.close()
'''
'''
#F. A single diagram with KDE plots of salaries for each Department.
print("3F. A single diagram with KDE plots of salaries for each Department.")
plt.figure(figsize=(12,6))
sns.kdeplot(data=emp_df, x='salary', hue='department', fill=True)
plt.title("KDE of Salaries by Department")
plt.tight_layout()
plt.savefig("3F_kde_department_salary.png")
plt.show()
plt.close()
'''
#4. Sampling
print("4.sampling")
#Use DataFrame sample() to produce a new 500 element sample of the data from emp_df.  Use the weights parameter to synthetically bias the sample such that employees with ages 40-49 are three times as likely to be sampled as employees in other age ranges. Name this new DataFrame smpl_df
emp_df['age'] = (pd.Timestamp('today') - pd.to_datetime(emp_df['birthdate'])).dt.days // 365
weights = emp_df['age'].apply(lambda x: 3 if 40 <= x <= 49 else 1)
smpl_df = emp_df.sample(n=500, weights=weights)
#A. Show a screenshot of the output of smpl_df.describe(include=’all’)
fourA=smpl_df.describe(include='all')
print(f"4A. output of smpl_df.describe(include='all'): {fourA}")
#B. Show a screenshot of the output of smpl_df.head(10)
fourB=smpl_df.head(10)
print(f"4B. output of smple_df.head(10): {fourB}")

#5. Perturbation
print("5.Perturbation")
#Perturb the salary values of emp_df using Gaussian noise to produce a new DataFrame named prtrb_df
#A. How might you choose the standard deviation parameter for the noise? 
#   You can use 5–10% of the salary mean or std as the noise level:
noise_std = emp_df['salary'].std() * 0.1
prtrb_df = emp_df.copy()
prtrb_df['salary'] = (prtrb_df['salary'] + np.random.normal(0, noise_std, len(prtrb_df))).round().astype(int)
#B. Show a screenshot of the output of prtrb_df.describe(include=’all’)
fiveB=prtrb_df.describe(include='all')
print(f"5B. output of prtrb_df.describe(include='all'): {fiveB}")
#C. Show a screenshot of the output of prtrb_df.head(10)
fiveC=prtrb_df.head(10)
print(f"5C. output of prtrb_df.head(10): {fiveC}")

#7. save as cvs file "emp_df.csv"