import common

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


'''
this was the first attempt of looking at the data before writing functions
just to get a feeling for what's in there
'''
def make_plot(data, sampling_time = False, first_hour = 14, last_hour = 14, act_max = False):

  if sampling_time: data = common.resample_data(data, sampling_time)
  if not act_max: act_max = max([data.p_act.max(), data.s_act.max()]) 
  
  #print(common.resample_data(data, '5Min'))

  data = data.drop(columns = ['s_r','s_g','s_b', 'p_r','p_g','p_b', 's_light','p_light'])
  time_slices = common.slice_data(data, first_hour = first_hour, last_hour = last_hour)

  # 8 rows, 1 col, 12 wide, 18 tall
  # https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html
  fig, axs = plt.subplots(8,1, figsize=[12,18], constrained_layout=True)
  # https://stackoverflow.com/a/64230180/5354137
  ax = axs.ravel() 
  fig.suptitle(f'Activity of Subject and Bedpartner')
  fig.supxlabel('Time')
  # https://matplotlib.org/stable/_images/sphx_glr_named_colors_003.png
  s_p_colors = ['darkred', 'darkslateblue']

  i = 0
  for slice in time_slices:
    if i == 0: next # the first day is lacking some data
    slicename = f"slice {i+1}"
    print(f"plotting {slicename}")
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#other-plots
    # the less "alpha", the more transparent the areas (it's more because of plot3)
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#area-plot
    time_slices[i].plot(ax = ax[i], kind = 'line', color = s_p_colors, alpha = 0.6)
    ax[i].set_title(slicename)
    # always free here because it's the middle of the night
    ax[i].legend(['subject', 'bed partner'], loc = 'upper center')
    ax[i].set_xlabel('')
    ax[i].set_ylabel('counts/min')
    ax[i].set_ylim(0, act_max)
    i += 1

  if not sampling_time: sampling_time = '1Min'
  png = f'plots/plot1_{sampling_time}Bin_{first_hour}-{last_hour}.png'
  print(f"writing {png}")
  # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
  plt.savefig(png, bbox_inches = 'tight', dpi = 500) # for viewing plots use plt.show()
  plt.close()
