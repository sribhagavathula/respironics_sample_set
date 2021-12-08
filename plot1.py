import common

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def make_plot(data, sampling_time = False, first_hour = 14, last_hour = 14, act_max = False, light_max = False):

  if sampling_time: data = common.resample_data(data, sampling_time)
  data = data.drop(columns = ['s_r','s_g','s_b', 'p_r','p_g','p_b'])
  time_slices = common.slice_data(data, first_hour = first_hour, last_hour = last_hour)

  # 8 rows, 1 col, 12 wide, 18 tall
  # https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html
  fig, axs = plt.subplots(8,1, figsize=[12,18], constrained_layout=True)
  # https://stackoverflow.com/a/64230180/5354137
  ax = axs.ravel()

  fig.suptitle(f'Activity and Photopic Light of Subject/Bedpartner ({sampling_time} bin)')
  fig.supylabel('Activity (counts/min)')
  fig.supxlabel('Time')

  if not act_max: act_max = max([data.p_act.max(), data.s_act.max()])
  if not light_max: light_max = max([data.p_light.max(), data.s_light.max()])
  light_columns = ['s_light', 'p_light']
  # list: https://matplotlib.org/stable/gallery/color/named_colors.html
  nice_colors = ['powderblue','steelblue', 'mistyrose','tomato']

  i = 0
  for slice in time_slices:
    slicename = f"slice {i+1}"
    print(f"plotting {slicename}")

    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#other-plots
    time_slices[i].plot(ax = ax[i], kind = 'area', secondary_y = light_columns, color = nice_colors, legend = False)

    ax[i].set_title(slicename)
    ax[i].legend(loc = 'upper center')
    ax[i].set_ylim(0, act_max)
    ax[i].right_ax.set_ylim(0, light_max)
    ax[i].right_ax.set_ylabel('lux')
    ax[i].set_xlabel('')
    ax[i].set_ylabel('')

    i += 1

  png = f'time_slices-{sampling_time}Bin_{first_hour}-{last_hour}.png'
  print(f"writing {png}")
  # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
  plt.savefig(png, bbox_inches = 'tight', dpi = 600) # for viewing plots use plt.show()
  plt.close()
