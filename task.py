from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

patient_csv = 'C1045_Acti_1_Week_1_22_11_2016_5_03_00_PM_New_Analysis.csv'
control_csv = 'P1045_Acti1_Week_1_22_11_2016_5_10_00_PM_New_Analysis.csv'

print("reading csv")

# note to self, be mindful that pandas counts from 0 but libreoffice counts from 1 instead!
# read_csv also has header=, but no need to specify it for the actiwatch files if skiprows= is chosen correctly
pdata = pd.read_csv(patient_csv, skiprows=174)
cdata = pd.read_csv(control_csv, skiprows=173)

new_colnames = {
        "Line":"line",
        "Date":"date", "Time":"time",
        "Off-Wrist Status":"on_off_wrist", "Activity":"act", "Marker":"marker",
        "Red Light":"r", "Green Light":"g", "Blue Light":"b", "White Light":"w",
        "Sleep/Wake":"sleep_wake", "Interval Status":"status",
        "Unnamed: 12":"unused"}
pdata = pdata.rename(columns = new_colnames)
cdata = cdata.rename(columns = new_colnames)

# https://stackoverflow.com/a/49668702,
pdata["datetime"] = pd.to_datetime(pdata['date'] + ' ' + pdata['time'])
cdata["datetime"] = pd.to_datetime(cdata['date'] + ' ' + cdata['time'])

print("writing plots")

# https://pandas.pydata.org/docs/reference/api/pandas.concat.html
plot_data = pd.concat(
        [ pdata['datetime'], cdata['w'], cdata['act'], pdata['w'], pdata['act'] ], axis=1,
        keys=['datetime', 'c_light', 'c_act', 'p_light', 'p_act'])

# https://stackoverflow.com/a/29370182/5354137
act_max = max([plot_data.c_act.max(), plot_data.p_act.max()])
light_max = max([plot_data.c_light.max(), plot_data.p_light.max()])

# nov 22 to nov 30, 2016
first_day = 22
last_day = 30

nights = []
night = 0
for day in range(first_day, last_day):

    t0 = f"2016-11-{day} 14:00"
    t1 = f"2016-11-{day+1} 14:00"

    # https://stackoverflow.com/questions/29370057
    nights.append(plot_data.loc[ t0 : t1 ])
    
    light_columns = ['p_light','c_light']
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    nice_colors = ['mistyrose','tomato','powderblue','steelblue']
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#other-plots
    ax = nights[night].plot.area(secondary_y=light_columns, color=nice_colors)

    ax.legend(loc = 'upper center')
    ax.set_ylim(0, act_max)
    ax.right_ax.set_ylim(0, light_max)
    ax.set_ylabel('Activity (counts/min)')
    ax.right_ax.set_ylabel('Photopic light (lux)') # watch user manual says "white" is photopic light
    ax.set_xlabel('Time')

    plt.title('Patient vs. Control: Activity and Photopic Light')
    # plt.show()
    
    night += 1
    png = f"night{night}.png"
    print(png)
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
    # plt.savefig(png, bbox_inches='tight', dpi=600)
    plt.show()
    plt.close()
