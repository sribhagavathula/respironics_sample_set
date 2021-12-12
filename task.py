'''
the full dataset is available at https://zenodo.org/record/4961281 
(just need to google one of the CSV file names, that's it!!!)
'''

import common
import plot1
import plot2
import plot3

subjectAndBedpartner_pairs = [
  {
    'subject': ['C1045_Acti_1_Week_1_22_11_2016_5_03_00_PM_New_Analysis.csv', 174],
    'partner': ['P1045_Acti1_Week_1_22_11_2016_5_10_00_PM_New_Analysis.csv', 173]
  }
]

sdata, pdata = common.read_csv(subjectAndBedpartner_pairs[0])
data = common.join_data(sdata, pdata)

# both persons' activity in one plot for each period
#plot1.make_plot(data) # original sampling time is 1Min

# pie charts for r/g/b light percentages for each person and each period
#plot2.make_plot(data, sampling_time = '60Min', first_hour = 21, last_hour = 6) # each night
#plot2.make_plot(data, sampling_time = '60Min', first_hour = 10, last_hour = 18) # each day

# activity vs. light for each period, once for subject and once for bed partner
#plot3.make_plot(data, sampling_time = '5Min', first_hour = 20, last_hour = 8, act_max = 50, light_max = 350)
