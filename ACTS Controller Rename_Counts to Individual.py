# -*- coding: utf-8 -*-
"""
Created on Tue May 20 16:25:32 2025

@author: Gary.Lawson
"""

import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', 25)

# File Path
file_path = r"C:/Users/gary.lawson/Downloads/"

# Read in file from ACTS
df = pd.read_csv(file_path+"Pneumatic_Controllers (2).csv")

# Fill missing COUNT values.  Assume 1 controller
df['COUNT'] = df['COUNT'].fillna(1)
df.head()
df.columns

# Filter for only OOOOb facilities and pneumatic controllers
df = df[df['OOOOb Facility Flag'].isin(['Y', 'Compressor', 'Compressor ???'])]
#df = df[df['ACTUATING_METHOD'].isin(['Natural Gas', 'Propane'])]
#df['OOOOb Facility Flag'].unique()

# Create complete columns including corrected information
df['INACTIVE_DATE_NEW'] = np.where(df['Inactive Date Correction'].isna(), df['INACTIVE_DATE'], df['Inactive Date Correction'])
df['MANUFACTURER_NAME_NEW'] = np.where(df['Manufacturer Name Corrections'].isna(), df['MANUFACTURER_NAME'], df['Manufacturer Name Corrections'])
df['MODEL_NAME_NEW'] = np.where(df['Model Name Corrections'].isna(), df['MODEL_NAME'], df['Model Name Corrections'])
df['ACTUATING_METHOD_NEW'] = np.where(df['Actuatinng Method Correction'].isna(), df['ACTUATING_METHOD'], df['Actuatinng Method Correction'])
df['ACTUATING_TYPE_NEW'] = np.where(df['Actuating Type Corrections'].isna(), df['ACTUATING_TYPE'], df['Actuating Type Corrections'])
df['VENT_CONTROL_TYPE_NEW'] = np.where(df['Vent Control Corrections'].isna(), df['VENT_CONTROL_TYPE'], df['Vent Control Corrections'])

df1 = df.copy()

# Look for duplicate facility/source names, replace with new number so not same
# name appearing at facility multiple times

# Create a unique ID
df['Dup_Review'] = df['FACILITY_NAME'] + df['SOURCE_NAME']
# Create new dataframe with only the duplicate values
y = df[df.duplicated(subset='Dup_Review')]
# Iterate through each row to create a new CTRL name
for index, i in y.iterrows():
    # Find out how many total controllers exist at the facility
    tot_df = df[df['FACILITY_NAME'] == i['FACILITY_NAME']]
    tot_count = tot_df['FACILITY_NAME'].count()
    #print(tot_count)
    
    # Find out how many duplicate controllers exist at the facility
    dup_df = y[y['FACILITY_NAME'] == i['FACILITY_NAME']]
    dup_count = int(dup_df['FACILITY_NAME'].count())
    #print(dup_count)
    
    # Create a new counter to use in new name.  This starts at 1.
    dup_df['Count'] = range(1, len(dup_df)+1)
    # Get the value that will influence the new name
    new_val = dup_df[dup_df.index == index]['Count'].values[0]
    #print(new_val)
    
    # Create the new CTRL name by adding the influencer value (new counter) to
    # the total controller accounting, assuming the original total controller
    # Count starts at 1 and is increased by 1 int for each new controller.  This
    # helps to ensure the new name is unique and not a duplicate of an existing
    # controller name.
    new_source_name = 'CTRL-R-'+str(tot_count+new_val)
    # Assign the new source name to the SOURCE_NAME
    df.loc[index,'NEW_SOURCE_NAME'] = new_source_name
    #print('CTRL-R-'+str(tot_count+new_val))
    #print('####', index, i['FACILITY_NAME'], tot_count, dup_count, '$$$$')

# Check to make sure no duplicates exist after previous loop
df['Dup_Review'] = df['FACILITY_NAME'] + df['SOURCE_NAME']
df[df.duplicated(subset='Dup_Review')]
#df.head()

# Move existing source names where no duplicates exist to NEW_SOURCE_NAME column
df['NEW_SOURCE_NAME'] = np.where(df['NEW_SOURCE_NAME'].isna(), df['SOURCE_NAME'], df['NEW_SOURCE_NAME'])

# Create function to build new names for each controller where count >1
def multiply_and_suffix(string, x):
    result = [f"{string}{-i}" for i in range(1, x + 1)]
    return result

# Iterate through each row and apply the function to build out new controller
# names.  
output_list = []
for source in zip(df['NEW_SOURCE_NAME'], df['COUNT'].astype(int), 
                  df['FACILITY_NAME'], df['EQUIPMENT_ID'],
                  df['SOURCE_NAME'], 
                  df['MANUFACTURER_NAME'], df['Manufacturer Name Corrections'], df['MANUFACTURER_NAME_NEW'], 
                  df['MODEL_NAME'], df['Model Name Corrections'], df['MODEL_NAME_NEW'],
                  df['ACTUATING_METHOD'], df['Actuatinng Method Correction'], df['ACTUATING_METHOD_NEW'],
                  df['ACTUATING_TYPE'], df['Actuating Type Corrections'], df['ACTUATING_TYPE_NEW'],
                  df['VENT_CONTROL_TYPE'], df['Vent Control Corrections'], df['VENT_CONTROL_TYPE_NEW'],
                  df['ACTIVE_DATE'],
                  df['INACTIVE_DATE'], df['Inactive Date Correction'], df['INACTIVE_DATE_NEW'],
                  ):
    #print(source[1])
    result = multiply_and_suffix(source[0], source[1])
    #print(result)
    # For each new controller name, build out a sub list that includes
    # other important info
    for i in result:
        result = [source[2], source[3], source[4], source[1], source[5], source[6], 
                  source[7], source[8], source[9], source[10], source[11], 
                  source[12], source[13], source[14], source[15], source[16],
                  source[17], source[18], source[19], source[20],
                  source[21], source[22], source[23],i]
        output_list.append(result)

# Convert to DataFrame
df_new = pd.DataFrame(output_list, columns=['FACILITY_NAME', 'EQUIPMENT_ID', 'ORIGINAL_SOURCE_NAME', 'ORIGINAL_COUNT',
                                            'MANUFACTURER_NAME', 'Manufacturer Name Corrections', 'MANUFACTURER_NAME_NEW',
                                            'MODEL_NAME', 'Model Name Corrections', 'MODEL_NAME_NEW',
                                            'ACTUATING_METHOD', 'Actuatinng Method Correction', 'ACTUATING_METHOD_NEW',
                                            'ACTUATING_TYPE', 'Actuating Type Corrections', 'ACTUATING_TYPE_NEW',
                                            'VENT_CONTROL_TYPE','Vent Control Corrections', 'VENT_CONTROL_TYPE_NEW',
                                            'ACTIVE_DATE',
                                            'INACTIVE_DATE', 'Inactive Date Correction', 'INACTIVE_DATE_NEW',
                                            'OOOOb_NAME'])

# Drop any instances where the facility name doesn't exist, indicating bad data
df_cleaned = df_new.dropna(subset=['FACILITY_NAME'])
#df_cleaned.tail(17)

# Validate the number of records are as expected
df['COUNT'].sum()
len(df_cleaned)

df_cleaned.tail(20)


# df_cleaned['Dup_Review'] = df_cleaned['FACILITY_NAME'] + df_cleaned['OOOOb_NAME']
# df_cleaned[df_cleaned.duplicated(subset='Dup_Review')]
# len(df_cleaned[df_cleaned.duplicated(subset='Dup_Review')])

# df_cleaned[df_cleaned['Dup_Review'] == 'ZALESKY 34-8PHCTRL-05C-1']

df_cleaned.to_csv(file_path+"OOOOb_Pneumatic_Controllers1.csv")
