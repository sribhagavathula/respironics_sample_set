from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


'''
take as input a dict with csv file for subject and another csv for bedpartner
including how many lines must be skipped for each csv file (it differs slightly)
note to self, be mindful that pandas counts from 0 but libreoffice counts from 1 instead!
read_csv also has header=, but no need to specify it for the actiwatch files if skiprows= is chosen correctly
'''
def read_csv(pair):
  new_colnames = {
    "Line":"line",
    "Date":"date", "Time":"time",
    "Off-Wrist Status":"on_off_wrist", "Activity":"act", "Marker":"marker",
    "Red Light":"r", "Green Light":"g", "Blue Light":"b", "White Light":"w",
    "Sleep/Wake":"sleep_wake", "Interval Status":"status",
    "Unnamed: 12":"unused"}

  csv, skip = pair['subject']
  print(f"reading {csv} from line {skip}")
  sdata = pd.read_csv(csv, skiprows = skip)
  sdata = sdata.rename(columns = new_colnames)
  sdata["datetime"] = pd.to_datetime(sdata['date'] + ' ' + sdata['time'])

  csv, skip = pair['partner']
  print(f"reading {csv} from line {skip}")
  pdata = pd.read_csv(csv, skiprows = skip)
  pdata = pdata.rename(columns = new_colnames)
  pdata["datetime"] = pd.to_datetime(pdata['date'] + ' ' + pdata['time'])

  return [sdata, pdata]


'''
it seems the plotting features of Pandas DataFrame are really made
to be used with _one_ DataFrame or at least i was not able to figure
out how to do the things i wanted to do with multiple DataFrames, so
making one DataFrame containing all the data I need from the original
CSV files.
as for why making it into time series data? because that makes it much
easier to slice, https://stackoverflow.com/a/49668702 also for this.
docs for .concat: https://pandas.pydata.org/docs/reference/api/pandas.concat.html
'''
def join_data(sdata, pdata):
  print('joining subject and bedpartner data')

  selected_cols = [
    sdata['datetime'], # hopefully the watches were synchronous enough?!
    sdata['w'], sdata['r'], sdata['g'], sdata['b'],
    sdata['act'],
    pdata['w'], pdata['r'], pdata['g'], pdata['b'],
    pdata['act']]

  new_names = [
    'datetime', 
    's_light', 's_r', 's_g', 's_b',
    's_act',
    'p_light', 'p_r', 'p_g', 'p_b',
    'p_act']

  data = pd.concat(selected_cols, axis = 1, keys = new_names)
  data = data.set_index(['datetime'])

  return data


'''
does what it says in the name
i thought this would be more work
'''
def resample_data(data, binstring):
  print(f"resampling data for {binstring} bins")

  data = data.resample(binstring).mean()
  return data


'''
the data is not really about "a week", it's more about nights (not really "days" either)
so i want to be able to compare them
so i need to separate them from one another
'''
def slice_data(data, first_hour = 21, last_hour = 6, first_day = 22, last_day = 30):
  print(f"slicing data into regular intervals from {first_hour}:00 to {last_hour}:00")

  slices = []

  for day in range(first_day, last_day):
    t0 = f"2016-11-{day} {first_hour}:00"
    t1 = f"2016-11-{day+1} {last_hour}:00"
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
    slices.append(data.loc[ t0 : t1 ])

  return slices
