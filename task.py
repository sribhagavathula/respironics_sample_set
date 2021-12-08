import common
import plot1
import plot2

subjectAndBedpartner_pairs = [
  {
    'subject': ['C1045_Acti_1_Week_1_22_11_2016_5_03_00_PM_New_Analysis.csv', 174],
    'partner': ['P1045_Acti1_Week_1_22_11_2016_5_10_00_PM_New_Analysis.csv', 173]
  }
]

sdata, pdata = common.read_csv(subjectAndBedpartner_pairs[0])
data = common.join_data(sdata, pdata)

plot1.make_plot(data, sampling_time = '30Min', first_hour = 22, last_hour = 6, act_max = 200, light_max = 2000)

plot2.make_plot(data, sampling_time = '60Min', first_hour = 21, last_hour = 6) # each night
plot2.make_plot(data, sampling_time = '60Min', first_hour = 10, last_hour = 18) # each day
