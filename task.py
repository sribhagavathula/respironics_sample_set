from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

patient_csv = 'P1045_Acti1_Week_1_22_11_2016_5_10_00_PM_New_Analysis.csv'
control_csv = 'C1045_Acti_1_Week_1_22_11_2016_5_03_00_PM_New_Analysis.csv'

pdata = pd.read_csv(patient_csv, skiprows=173)
cdata = pd.read_csv(control_csv, skiprows=174)

pdata["datetime"] = pd.to_datetime(pdata['Date'] + ' ' + pdata['Time'])
cdata["datetime"] = pd.to_datetime(cdata['Date'] + ' ' + cdata['Time'])

pdata = pdata.rename(columns={"Line":"line", "Date":"date", "Time":"time", "Off-Wrist Status":"on_off_wrist", "Activity":"act", "Marker":"marker", "Red Light":"r", "Green Light":"g", "Blue Light":"b", "White Light":"w", "Sleep/Wake":"sleep_wake", "Interval Status":"status", "Unnamed: 12":"unused"})
cdata = cdata.rename(columns={"Line":"line", "Date":"date", "Time":"time", "Off-Wrist Status":"on_off_wrist", "Activity":"act", "Marker":"marker", "Red Light":"r", "Green Light":"g", "Blue Light":"b", "White Light":"w", "Sleep/Wake":"sleep_wake", "Interval Status":"status", "Unnamed: 12":"unused"})

#print(pdata)
#print(cdata)

fig, axs = plt.subplots(figsize=(12, 4))
p_by_day = pdata.groupby(pdata['datetime'].dt.day)
p_by_day['w'].plot(kind='line')
plt.show()
