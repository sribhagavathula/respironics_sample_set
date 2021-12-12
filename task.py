'''
the full dataset is available at https://zenodo.org/record/4961281 
(just need to google one of the CSV file names, that's it!!!)
---
Note to self: to debug through separate files in VSCode, go to the debugger(Ctrl+Shft+D) and click on "create launch .json file" and in the last line 
enter "justMyCode":false".Save and close. Set a breakpoint in your concerned file and debug!
'''

from datetime import datetime
import common
import plot1
import plot2
import plot3

subjectAndBedpartner_pairs = [
  {
    'subject': ['data/C1045_Acti_1_Week_1_22_11_2016_5_03_00_PM_New_Analysis.csv', 174],
    'partner': ['data/P1045_Acti1_Week_1_22_11_2016_5_10_00_PM_New_Analysis.csv', 173]  
  }
]

for pair in subjectAndBedpartner_pairs:
  sdata, pdata = common.read_csv(pair)
  data = common.join_data(sdata, pdata)

  #print(data) 

  # both persons' activity in one plot for each period
  plot1.make_plot(data) # original sampling time is 1Min

  # pie charts for r/g/b light percentages for each person and each period
  plot2.make_plot(data, sampling_time = '30Min', first_hour = 21, last_hour = 6) # each night 
  plot2.make_plot(data, sampling_time = '30Min', first_hour = 10, last_hour = 18) # each day 

  # activity vs. light for each period, once for subject and once for bed partner
  plot3.make_plot(data, sampling_time = '30Min', first_hour = 16, last_hour = 12, act_max = 250, light_max = 1200) 
