import pandas as pd
import numpy as np

df = pd.read_csv("hospital_dataset.csv")

print("Original Data:")
print(df.head())

df = df.drop_duplicates()

df['Disease'] = df['Disease'].fillna('Unknown')
df['Gender'] = df['Gender'].fillna('Not Specified')
df['Department'] = df['Department'].fillna('General')

df = df.dropna(subset=['Admission_Date', 'Discharge_Date', 'Age'])

df['Admission_Date'] = pd.to_datetime(df['Admission_Date'], errors='coerce')
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'], errors='coerce')

df = df.dropna(subset=['Admission_Date', 'Discharge_Date'])

df['Length_of_Stay'] = (df['Discharge_Date'] - df['Admission_Date']).dt.days

df = df[df['Length_of_Stay'] >= 0]

df['Disease'] = df['Disease'].str.lower().str.strip()
df['Department'] = df['Department'].str.strip()
df['Gender'] = df['Gender'].str.capitalize().str.strip()

df = df[(df['Age'] > 0) & (df['Age'] < 100)]

def age_group(age):
    if age < 18:
        return "Child"
    elif age < 40:
        return "Young Adult"
    elif age < 60:
        return "Adult"
    else:
        return "Senior"

df['Age_Group'] = df['Age'].apply(age_group)

df['Billing_Amount_INR'] = pd.to_numeric(df['Billing_Amount_INR'], errors='coerce')
df['Billing_Amount_INR'] = df['Billing_Amount_INR'].fillna(df['Billing_Amount_INR'].median())

df['Admission_Month'] = df['Admission_Date'].dt.month
df['Admission_Year'] = df['Admission_Date'].dt.year

print("\nCleaned Data:")
print(df.head())

df.to_csv("cleaned_hospital_data.csv", index=False)

print("\n✅ Cleaning completed. File saved as 'cleaned_hospital_data.csv'")