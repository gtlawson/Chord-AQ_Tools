# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 07:11:23 2025

@author: Gary.Lawson

This script uses raw 5-min flare data and chains events that are sequential.
This data is grouped by the SCADA_ID and reports all other data available on
the existing rows.

To use, update Load data section with location of data, and verify columns are
the same.
"""


# Load Packages
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
pd.set_option('display.max_columns', 25)

# Load data
df = pd.read_csv(r"Downloads/Raw 5 minute Data - Cold Flares.csv")
df.index[df.isna().all(axis=1)].tolist() #No blank rows

df.head()
df.info()
df.columns

# OOOOb Facility List = remove any SCADA Tags that are not OOOOb related - list provided by Andres
oooob_tag_list = ['Watford City.WC03.Allen 44-36 CTB.Allen 44-36 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Dickinson.DX01-A.Warriors.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX01-A.Warriors.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX01-A.Warriors.Zone.DSU 01.Flares.HP Flare Temperature 03.Temperature','Dickinson.DX01-A.Warriors.Zone.DSU 01.Flares.HP Flare Temperature 04.Temperature','Dickinson.DX01-A.Warriors.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX01-A.Warriors.Zone.DSU 01.Flares.LP Flare Temperature 02.Temperature','Dickinson.DX01-C.Bradfield Gemstones.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX01-C.Bradfield Gemstones.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX01-C.Bradfield Gemstones.Zone.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX01-C.Ungulates.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX01-C.Ungulates.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX01-C.Ungulates.Zone.Pad 01.Gas Meters.LP Flare 01 Gas Meter 01.Temperature','Dickinson.DX02.Fox Ridge East.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX02.Fox Ridge East.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX02.Fox Ridge East.Zone.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX02.Pitch Tennis W CTB.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX02.Pitch Tennis W CTB.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX03.Fish South-AF Animals Central.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX03.Fish South-AF Animals Central.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX03.Fish South-AF Animals Central.Zone.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX03.Metals East.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX03.Metals East.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX03.Metals East.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX03.Racing.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX03.Racing.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX03.Racing.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX03.Whales East.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX03.Whales East.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX03.Whales East.Zone.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.Blanca 1 CTB.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.Blanca 1 CTB.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.Blanca 2 CTB.Flares.Flare Temperature 01.Flare Temperature','Dickinson.DX04.Hay Draw.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature'
,'Dickinson.DX04.Hay Draw.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.Hay Draw.Zone.DSU 02.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.Hay Draw.Zone.DSU 02.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Bice 1201 Pad 2.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Bice 1201 Pad 2.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX04.LK-Bice 1201 Pad 2.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Bice 1201 Pad 2.Pad 01.Flares.LP Flare Temperature 02.Temperature','Dickinson.DX04.LK-Bice 6-31.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Bice 6-31.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX04.LK-Bice 6-31.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Devils Canyon.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Devils Canyon.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX04.LK-Devils Canyon.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Erickson 11-2.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.LK-Erickson 11-2.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX04.LK-Erickson 11-2.Zone.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.LK-M Elisabeth 2-3-4.Pad 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.LK-M Elisabeth 2-3-4.Pad 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.Shavano-Clinton.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX04.Shavano-Clinton.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX04.Shavano-Clinton.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX04.Shavano-Clinton.Zone.DSU 01.Flares.LP Flare Temperature 02.Temperature','Dickinson.DX05.LK-Danielle CTB.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX05.LK-Danielle CTB.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX05.LK-Danielle CTB.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX05.LK-Olson.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX05.LK-Olson.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX05.LK-Olson.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Dickinson.DX05.MC Kudrna.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Dickinson.DX05.MC Kudrna.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Dickinson.DX05.MC Kudrna.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Lake.RL07.Locken Federal 12-11H.Flares.Flare Temperature 02.PV','Robinson Lake.RL01.Blanchette Fed 14-21 CTB.Blanchette Fed 14-21 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Evans 12-22 CTB.Evans 12-22 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Hagen Fed 43-31 CTB.Hagen Fed 43-31 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Heron 43-32 CTB.Heron 43-32 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Jammer 43-32 CTB.Jammer 43-32 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Nordby 13-12 CTB.Nordby 13-12 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Ongstad 13-15 CTB.Ongstad 13-15 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Rystedt 31-28 CTB.Rystedt 31-28 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL01.Sorkness 34X Pad.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL01.Sorkness 34X Pad.Flares.Flare Temperature 02.Temperature','Robinson Lake.RL04.Bronson 31X Pad.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL04.Bronson 31X Pad.Flares.HP Flare Temperature 01.Temperature','Robinson Lake.RL04.Bronson 31X Pad.Flares.HP Flare Temperature 02.Temperature','Robinson Lake.RL05.Marsupials West.Zone.Pad 01.Flares.HP Flare Temperature 01.Temperature','Robinson Lake.RL05.Marsupials West.Zone.Pad 01.Flares.HP Flare Temperature 02.Temperature','Robinson Lake.RL05.Marsupials West.Zone.Pad 01.Flares.LP Flare Temperature 01.Temperature','Robinson Lake.RL06.Sanish Bay E 22-7 CPB.Sanish Bay E 22-7 CTB.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL06.Sanish Bay E Fed 11-3 CPB.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL06.Sanish Bay W 34-1 CTB.Sanish Bay W 34-1 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL06.Sanish Bay W Fed 12-3 CPB.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL07.Braaflat 11-11H CTB.Flares.Flare Temperature 03.Temperature','Robinson Lake.RL07.DE Bud 44-32 CTB.DE Bud 44-32 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL07.DE YK 12-33 CTB.DE YK 12-33 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL07.Joanna TTT Ranch 11-6H.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL07.Joanna TTT Ranch 11-6H.Flares.Flare Temperature 02.Temperature','Robinson Lake.RL07.Locken Federal 12-11H.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL07.S Bar 34-1 CTB.S Bar 34-1 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL08.Bigfoot 42-26 CTB.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL08.Bigfoot 42-26 CTB.Flares.Flare Temperature 02.Temperature','Robinson Lake.RL08.Bigfoot 42-26 CTB.Flares.Flare Temperature 02.Temperature'
,'Robinson Lake.RL08.Bigfoot 42-26 CTB.Flares.Flare Temperature 03.Temperature','Robinson Lake.RL08.Littlefield 11-21-2 CTB.Flares.Flare Temperature 01.Temperature','Robinson Lake.RL08.Littlefield 11-21-2 CTB.Flares.Flare Temperature 02.Temperature','Robinson Lake.RL-NR.DISCO8-28A.CLX.Flares.Flare Temperature 01.Flare Temperature','Robinson Lake.RL-NR.DISCO8-28A.CLX.Flares.Flare Temperature 02.Flare Temperature','Robinson Lake.RL-NR.MHA Moose 43-7 CTB.MHA Moose 43-7 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC06.Bergem 43-33 CTB.Bergem 43-33 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC08.Dahl W Fed 13-15 CTB.Dahl W Fed 13-15 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC08.Fossum 43-35 CTB.Fossum 43-35 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC08.Lee N 21-5 CTB.Lee N 21-5 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC08.Lindvig Beck 12-2 CTB.Lindvig Beck 12-2 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC09.Barnes 43-11 CTB.Barnes 43-11 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC09.Behan 42-29 CTB.Behan 42-29 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC09.Dahl E Fed 13-14 CTB.Dahl E Fed 13-14 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC10.Slagle 42-12 CTB.Slagle 42-12 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC12.Ranger Fed 42-16 CTB.Ranger Fed 42-16 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC12.Safely Fed 32-7 CTB.Flares.Flare Temperature 01.PV','Watford City.WC12.Safely Fed 32-7 CTB.Flares.Flare Temperature 02.PV','Watford City.WC12.Snowshoe Fed 30-31.Flares.Flare Temperature 01.PV','Watford City.WC12.Snowshoe Fed 30-31.Flares.Flare Temperature 02.PV','Watford City.WC12.Van Buren Fed 42-36 CTB.Van Buren Fed 42-36 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC-WF-2.Bitterroot 21-30 CTB.Bitterroot 21-30 PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC-WF-2.Granli 34X-20 CTB.Granli 34X-20 CTB PLC.Flare Gas Data.LP Gas Yesterday','Watford City.WC-WF-2.Granli 34X-20 CTB.Granli 34X-20 CTB PLC.Flares.Flare Temperature 01.Flare Temperature'
,'Watford City.WC-WF-2.Granli 34X-20 CTB.Granli 34X-20 CTB PLC.Flares.Flare Temperature 02.Flare Temperature','Watford City.WC-WF-2.Sapphire 21-31 CTB.Sapphire 21-31 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Watford City.WC-WF-3.Borseth 31-15 CTB.Flares.Flare Temperature 01.Temperature','Watford City.WC-WF-3.Borseth 31-15 CTB.Flares.Flare Temperature 02.Temperature','Watford City.WC-WF-3.Borseth 31-15 CTB.Flares.Flare Temperature 03.Temperature','Watford City.WC-WF-3.State Federal 21-16 CTB.State Federal 21-16 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL02.Brown Bear.Zone.DSU 01.Flares.HP Flare Temperature 01.Temperature','Williston.WL02.Brown Bear.Zone.DSU 01.Flares.HP Flare Temperature 02.Temperature','Williston.WL02.Brown Bear.Zone.DSU 01.Flares.LP Flare Temperature 01.Temperature','Williston.WL03.Andrews Fed 12-24 CTB.Andrews Fed 12-24 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL03.George Fed 12-24 CTB.George Fed 12-24 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL03.Lake Trenton Fed 21-31 CTB.Lake Trenton Fed 21-31 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL05.K2 Holdings 11-31 CTB.K2 Holdings 11-31 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL05.Ledahl 42-33 CTB.Ledahl 42-33 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL05.Peters Road Fed 41-30 CTB.Peters Road Fed 41-30 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL05.Pocono 33-4 CTB.Pocono 33-4 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL05.Thunderhill Federal 33-3 CTB.Thunderhill Federal 33-3 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL06.Hendricks 36-25 CTB.Hendricks 36-25 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL06.Maridoe Streamsong 11-17 CTB.Maridoe Streamsong 11-17 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL08.Archerfield 43-16 CTB.Archerfield 43-16 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL08.Iceman Fed 34-5 CTB.Iceman Fed 34-5 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL08.Maverick Fed 13-12 CTB.Maverick Fed 13-12 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL08.Merlin 43-15 CTB.Merlin 43-15 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL13.Harrier 26-35 CTB.Harrier 26-35 CTB PLC.Combustor.Temperature','Williston.WL13.Kestrel Fed 43-22H CTB.Kestrel Fed 43-22H CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL13.Kestrel Fed 43-22H CTB.Kestrel Fed 43-22H CTB PLC.Flares.Flare Temperature 03.Flare Temperature','Williston.WL13.Osprey 44-23 CTB.Osprey 44-23 CTB PLC.Combustor2.Temperature','Williston.WL13.Peregrine 42-24H CTB.Peregrine 42-24H CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL14.Olson State Fed 41-9 CTB.Olson State Fed 41-9 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL15.Truax State Fed 43-9 CTB.Truax State Fed 43-9 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL17.Wood Federal 12-25 CPB.Wood Federal 12-25 CTB PLC.Flares.Flare Temperature 01.Flare Temperature','Williston.WL19.Olson 31-31 CTB.Flares.Flare Temperature 01.PV','Williston.WL19.Olson 31-31 CTB.Flares.Flare Temperature 02.PV','Williston.WL19.Olson 31-31 CTB.Flares.Flare Temperature 03.PV','Williston.WL19.Tri D Ranch 13-18 CTB.Tri D Ranch 13-18 CTB PLC.Flares.Flare Temperature 01.Flare Temperature'
    ]

df = df[df['FLARE_TEMP_FULL_TAG_NAME'].isin(oooob_tag_list)]
len(df)

# Convert cell data types
df['FLARE_TEMP_RECORDTIME_CTZ'] = pd.to_datetime(df['FLARE_TEMP_RECORDTIME_CTZ'], format='mixed')

# Group rows if datetime is within 5 minutes for each facility
def group_rows(group):
    group = group.sort_values('FLARE_TEMP_RECORDTIME_CTZ')
    group['group'] = (group['FLARE_TEMP_RECORDTIME_CTZ'].diff() > timedelta(minutes=5)).cumsum()
    return group

df = df.groupby('SCADA_ID', group_keys=False).apply(group_rows)

# Aggregate the grouped rows
result = df.groupby(['SCADA_ID', 'group']).agg({
    # Start and end time of the group
    'FLARE_TEMP_RECORDTIME_CTZ': ['min', 'max'],
    'group': 'count',              # Count of chained events in the group
    'SCADASITE': 'first',
    'FLARE_TEMP_ID': 'first',
    # 'SCADA_ID': 'first',
    'FLARE_TEMP_FULL_TAG_NAME': 'first',
    # 'FLARE_TEMP_RECORDTIME_CTZ': 'first',
    'AMBIENT_TEMP_AREA': 'first',
    'AMBIENT_TEMP_TAG_NAME': 'first',
    'COLD_DEVIATION_STATUS': 'first',
    'GROUPING_SET': 'first',
    'SITE_NAME': 'first',
    'PRIORNUMBEROFDAYS': 'first'
}).reset_index()

# Clean up column names
result.columns = ['SCADA_ID', 'group',
                  'start_time', 'end_time',  # Start and end time of the group
                  'Chained_events',
                  'SCADASITE',
                  'FLARE_TEMP_ID',
                  # 'SCADA_ID': 'first',
                  'FLARE_TEMP_FULL_TAG_NAME',
                  # 'FLARE_TEMP_RECORDTIME_CTZ': 'first',
                  'AMBIENT_TEMP_AREA',
                  'AMBIENT_TEMP_TAG_NAME',
                  'COLD_DEVIATION_STATUS',
                  'GROUPING_SET',
                  'SITE_NAME',
                  'PRIORNUMBEROFDAYS'
                  ]
result = result.drop(columns='group')  # Drop the group column

# Add 5 min to end_time due to reading being at start of 5-min increment
result['end_time'] = result['end_time'] + timedelta(minutes=5)

# Add duration information
result['Duration'] = (result['end_time'] - result['start_time'])
result['Duration_hrs'] = (result['Duration'].dt.components['minutes'] +
                          result['Duration'].dt.components['hours']*60 +
                          result['Duration'].dt.components['days']*60*24)/60

# Reorder columns
result = result[['SCADASITE',
                'FLARE_TEMP_ID',
                 'SCADA_ID',
                 'FLARE_TEMP_FULL_TAG_NAME',
                 'start_time', 'end_time',  # Start and end time of the group
                 #'Duration',
                 'Chained_events',
                 'Duration_hrs',
                 'AMBIENT_TEMP_AREA',
                 'AMBIENT_TEMP_TAG_NAME',
                 'COLD_DEVIATION_STATUS',
                 'GROUPING_SET',
                 'SITE_NAME',
                 'PRIORNUMBEROFDAYS'
                 ]]


# Group rows of chained events if separated by 15 minutes or less 
gap_time = 120 #define time between chained cold events that acceptable to group

def group_of_groups(group):
    group = group.sort_values(by=['SCADA_ID', 'start_time'])
    group['time_diff'] = group['start_time'] - group.groupby('SCADA_ID')['end_time'].shift()
    time_threshold = pd.Timedelta(minutes=gap_time)
    group['group_of_groups'] = (group['time_diff'] > time_threshold).cumsum()
    return group

df2 = result.groupby('SCADA_ID', group_keys=False).apply(group_of_groups)

# Aggregate the grouped rows
result2 = df2.groupby(['SCADA_ID', 'group_of_groups'], as_index=False).agg({
    'SCADA_ID': 'first',
    'start_time': 'min',
    'end_time': 'max',  # Start and end time of the group
    'group_of_groups': 'count',
    'SCADASITE': 'first',
    'FLARE_TEMP_ID': 'first',
    'FLARE_TEMP_FULL_TAG_NAME': 'first',
    'Chained_events': 'sum',
    'Duration_hrs': 'sum',
    'AMBIENT_TEMP_AREA': 'first',
    'AMBIENT_TEMP_TAG_NAME': 'first',
    'COLD_DEVIATION_STATUS': 'first',
    'GROUPING_SET': 'first',
    'SITE_NAME': 'first',
    'PRIORNUMBEROFDAYS': 'first',
    'time_diff': 'first'
})

# Clean up column names
result2.columns = ['SCADA_ID',
                   'start_time',
                   'end_time',  # Start and end time of the group
                   'Chained_groups',
                   'SCADASITE',
                   'FLARE_TEMP_ID',
                   'FLARE_TEMP_FULL_TAG_NAME',
                   'Chained_events',
                   'Duration_hrs',
                   'AMBIENT_TEMP_AREA',
                   'AMBIENT_TEMP_TAG_NAME',
                   'COLD_DEVIATION_STATUS',
                   'GROUPING_SET',
                   'SITE_NAME',
                   'PRIORNUMBEROFDAYS',
                   'time_diff'
                   ]


# Reorder columns
result2 = result2[['SCADASITE',
                   'FLARE_TEMP_ID',
                   'SCADA_ID',
                   'FLARE_TEMP_FULL_TAG_NAME',
                   'start_time', 'end_time',  # Start and end time of the group
                   #'Duration',
                   'Chained_events',
                   'Chained_groups',
                   'Duration_hrs',
                   'AMBIENT_TEMP_AREA',
                   'AMBIENT_TEMP_TAG_NAME',
                   'COLD_DEVIATION_STATUS',
                   'GROUPING_SET',
                   'SITE_NAME',
                   'PRIORNUMBEROFDAYS'
                   ]]


#Pull in additional information to help make this sheet more usable

# bobo_old = pd.read_csv(r"Downloads/2025 0723 Thermocouple Deviations.csv") - commented out because we found a more complete data sheet
bobo_old = pd.read_csv(r"Downloads/2025 0723 Thermocouple Deviations_V2.csv")
flr_ref = pd.read_csv(r"Downloads/Flare Temp Cross Reference to ACTS Flare.csv")

# Convert cell data types
bobo_old['Date Deviation Began'] = pd.to_datetime(bobo_old['Date Deviation Began'], format='mixed').dt.date
flr_ref['OOOOb Scope Date'] = pd.to_datetime(flr_ref['OOOOb Scope Date'], format='mixed').dt.date
flr_ref.at[207,'Flare Pilot GSID'] = np.nan # get rid of string
flr_ref['Flare Pilot GSID'] = flr_ref['Flare Pilot GSID'].fillna(0).astype(np.int64)

# Drop duplicate flare records to prevent reporting two deviations for a combo
# flare.  Preferencing the storage vessel record.
flr_ref = flr_ref.sort_values(by=['Flare Pilot GSID', 'FLARE NAME', 'OOOOb Scope Date'], ascending=[True, True, True])
flr_ref = flr_ref.drop_duplicates(subset=['Flare Pilot GSID', 'FLARE NAME', 'OOOOb Scope Date'], keep='first')

# Merge in site no, flare name, and type of affected facility
result3 = pd.merge(result2, flr_ref[['Flare Pilot GSID',
                                     'Site No.', 
                                     'FLARE NAME', 
                                     'Type of Affected faciity', 
                                     'OOOOb Scope Date']], 
                     left_on='SCADA_ID', right_on='Flare Pilot GSID', how='left')
result3 = result3.drop(columns=['Flare Pilot GSID'])

result3['start_date'] = result3['start_time'].dt.date

# Drop duplicate flare records since Bobo's list had several more rows
bobo_old = bobo_old.rename(columns={'Equipment Name on FlareTempCrossReferenceToACTSFlare spreadsheet': 'FLARE NAME'})
bobo_old = bobo_old.sort_values(by=['SCADA_ID', 
                                    'FLARE NAME', 
                                    'Date Deviation Began'], 
                                ascending=[True, True, True])

bobo_old = bobo_old.drop_duplicates(subset=['SCADA_ID', 
                                            'FLARE NAME', 
                                            'Date Deviation Began'], 
                                    keep='first')

# Merge in Bobo's work
result4 = pd.merge(result3, bobo_old[['SCADA_ID', 
                                      'Date Deviation Began',
                                      'Bobo_Reason']], 
                     left_on=['SCADA_ID','start_date'], right_on=['SCADA_ID', 'Date Deviation Began'], how='left')

# Remove any records that exist prior to the OOOOb Scope Date
result4 = result4[result4['start_date'] >= result4['OOOOb Scope Date']]

# Drop unwanted columns
result4 = result4.drop(columns=['start_date', 'Date Deviation Began'])

# Print results
result4.to_csv(r"Downloads/OOOOb Cold Deviations_2hr gap group_python2.csv")


##############################################################################
# Stats and figures
##############################################################################

result_final = result4[result4['Cause of the Deviation (Marsworx)'].notna()]
tot_rows = len(result_final)
tot_hrs = result_final['Duration_hrs'].sum()
print('Total number of rows after removing "Cause of Deviation (Marsworx)" rows: ', tot_rows)
print('Total hours cold flares after removing "Cause of Deviation (Marsworx)" rows: ', round(tot_hrs,1))

result_final.groupby(['SCADA_ID'], as_index=False).agg({
    'SITE_NAME': 'first',
    'Duration_hrs': 'sum'
    }).sort_values(by='Duration_hrs', ascending=False)

counts = result3['start_date'].value_counts().sort_index()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
fig, ax = plt.subplots()
plt.figure(figsize=(10,6))
ax.bar(counts.index, counts)
#plt.rcParams['figure.dpi'] = 300
#fig.autofmt_xdate()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) # Format as YYYY-MM
# Rotate x-axis labels for better readability if needed
#plt.xticks(rotation=90, ha='right')
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title('Distribution of Cold Flare Events by Day for all OOOOb Facilities')
ax.set_xlabel('Day Cold Event Started')
ax.set_ylabel('Number of Cold Events')

#sns.barplot(x=counts.index, y=counts.values, ax=ax)
#counts.plot(kind='bar', color='skyblue', width=0.5)
plt.show()

# Generate a figure for each SCADA ID
for scadaid in result_final['SCADA_ID'].unique():
    # scadaid = 1499214
    # print(scadaid)
    data =  result[result['SCADA_ID']==scadaid].reset_index()
    sitename = data['SITE_NAME'].values[0]
    # print(sitename)
    OOOOb_date = result3[result3['SCADA_ID']==scadaid]['OOOOb Scope Date'].values[0]
    compliance_start = datetime(2024,5,7)
    if  OOOOb_date >=  compliance_start.date():
        start = OOOOb_date
    else:
        start = compliance_start.date()

    end = datetime(2025,5,6,23,59,59)

    # Prepare data for plotting
    plot_data = []
    for i in range(len(data)):
        # Connect start_time to stop_time with y=1
        plot_data.append({'time': data.loc[i, 'start_time'], 'value': 0})
        plot_data.append({'time': data.loc[i, 'end_time'], 'value': 0})

        # Connect stop_time to next start_time with y=0 (if not the last event)
        if i < len(data) - 1:
            plot_data.append({'time': data.loc[i, 'end_time'], 'value': 1})
            plot_data.append({'time': data.loc[i+1, 'start_time'], 'value': 1})
        
        # Add an initial point if the first interval doesn't start at the very beginning of your desired plot range
        # This ensures the '1' state is shown before the first '0' state
        if data['start_time'].iloc[0] >= pd.to_datetime(start):
            plot_data.append({'time': pd.to_datetime(start), 'value': 1})
            plot_data.append({'time': data['start_time'].iloc[0], 'value': 1})
        
        # Add a final point if needed to show '1' after the last interval
        if data['end_time'].iloc[-1] <= pd.to_datetime(end):
            plot_data.append({'time': pd.to_datetime(end), 'value': 1})
            plot_data.append({'time': data['end_time'].iloc[-1], 'value': 1})

    plot_df = pd.DataFrame(plot_data).sort_values(by='time').reset_index(drop=True)

    #Plot the data
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(plot_df['time'], plot_df['value'], drawstyle='steps-post', linewidth=2, color='orange') # Use steps-post for clear segments

    ax.set_xlim(start, end)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) # Format as YYYY-MM
    # Rotate x-axis labels for better readability if needed
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Flare Cold (0)', 'Flare Lit (1)'])
    ax.set_title(f'Cold Flare Events by Day for {sitename}', )
    ax.set_xlabel('Activity Timeline')
    ax.set_ylabel('Status')
    plt.text(1, 1, f'OOOOb Effective Date: {OOOOb_date}', transform=ax.transAxes,
            ha='right', va='top', fontsize=12, color='blue')
    plt.grid(True)

    plt.show()
    filename = sitename+'_graphic.png'
    fig.savefig('Downloads/FlareFigs/'+filename)
  
