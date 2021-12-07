from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

subject_csv = 'C1045_Acti_1_Week_1_22_11_2016_5_03_00_PM_New_Analysis.csv'
bedpartner_csv = 'P1045_Acti1_Week_1_22_11_2016_5_10_00_PM_New_Analysis.csv'

print("reading csv")

# note to self, be mindful that pandas counts from 0 but libreoffice counts from 1 instead!
# read_csv also has header=, but no need to specify it for the actiwatch files if skiprows= is chosen correctly
sdata = pd.read_csv(subject_csv, skiprows=174)
bpdata = pd.read_csv(bedpartner_csv, skiprows=173)

new_colnames = {
        "Line":"line",
        "Date":"date", "Time":"time",
        "Off-Wrist Status":"on_off_wrist", "Activity":"act", "Marker":"marker",
        "Red Light":"r", "Green Light":"g", "Blue Light":"b", "White Light":"w",
        "Sleep/Wake":"sleep_wake", "Interval Status":"status",
        "Unnamed: 12":"unused"}
sdata = sdata.rename(columns = new_colnames)
bpdata = bpdata.rename(columns = new_colnames)

# https://stackoverflow.com/a/49668702
sdata["datetime"] = pd.to_datetime(sdata['date'] + ' ' + sdata['time'])
bpdata["datetime"] = pd.to_datetime(bpdata['date'] + ' ' + bpdata['time'])

###############################################################################

print("writing plots")

# making a new dataframe which has exactly the data that should go
# into the plot makes it so much easier to make the plot look the
# way it should!
# axis=0 is 'index', axis=1 is 'columns'
# (https://pandas.pydata.org/docs/reference/api/pandas.concat.html)
plot_data = pd.concat(
        [ sdata['datetime'], bpdata['w'], bpdata['act'], sdata['w'], sdata['act'] ], axis=1,
        keys=['datetime', 'bp_light', 'bp_act', 's_light', 's_act'])

# using the 2nd method explained at https://stackoverflow.com/a/29370182/5354137
plot_data = plot_data.set_index(['datetime'])
act_max = max([plot_data.bp_act.max(), plot_data.s_act.max()])
light_max = max([plot_data.bp_light.max(), plot_data.s_light.max()])

binspec = '60Min'
plot_data = plot_data.resample(binspec).mean()

# watches were first worn on the 22nd of november 2016 (slice 1 with incomplete bedpartner in the beginning)
# and then for one week until 30th of november 2016 (slice 8 with incomplete bedpartner in the end)
first_day = 22
last_day = 30

# 8 rows, 1 col, 12 wide, 18 tall ... constrained_layout makes it less crammed, funny enough
# docs: https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html
fig, axs = plt.subplots(8,1, figsize=[12,18], constrained_layout=True)
ax = axs.ravel() # (results in list of length 8;
                 #  see https://stackoverflow.com/a/64230180/5354137 for what's going on here)

# had no idea what Photopic light (the "White Light" column according to the
# User Manual, is Photopic light) ... according to Wikipedia, it means light
# as perceived by the eye
fig.suptitle(f'Activity and Photopic Light of Subject/Bedpartner ({binspec} bin)')
fig.supylabel('Activity (counts/min)')
fig.supxlabel('Time')

# note: i know that pandas has .groupby() but it didn't work the way i thought
# it would and i felt i'm loosing too much time trying to figure it out, so
# solved this with a loop instead, sorry if it's not much elegant...
time_slices = []
i = 0
for day in range(first_day, last_day):

    t0 = f"2016-11-{day} 14:00"
    t1 = f"2016-11-{day+1} 14:00"

    # https://stackoverflow.com/questions/29370057
    time_slices.append(plot_data.loc[ t0 : t1 ])

    light_columns = ['s_light','bp_light']
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    nice_colors = ['mistyrose','tomato','powderblue','steelblue']
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#other-plots
    time_slices[i].plot(ax=ax[i], kind='area', secondary_y=light_columns, color=nice_colors, legend=False)

    ax[i].legend(loc = 'upper center')
    ax[i].set_ylim(0, act_max)
    ax[i].right_ax.set_ylim(0, light_max)
    ax[i].right_ax.set_ylabel('lux')
    ax[i].set_xlabel('')
    ax[i].set_ylabel('')

    slicename = f"slice {i+1}"
    ax[i].set_title(slicename)
    print(slicename)

    i += 1

png = f'time_slices-{binspec}Bin.png'
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
# plt.savefig(png, bbox_inches='tight', dpi=600)
plt.show()
plt.close()
