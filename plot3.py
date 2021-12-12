import common

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def make_plot(data, sampling_time = False, first_hour = 14, last_hour = 14, act_max = False, light_max = False):

  if sampling_time: data = common.resample_data(data, sampling_time)
  if not act_max: act_max = max([data.p_act.max(), data.s_act.max()])
  if not light_max: light_max = max([data.p_light.max(), data.s_light.max()])
  
  print(f"act_max: {int(act_max)}")
  print(f"light_max: {int(light_max)}")

  sdata = data.drop(columns = ['s_r','s_g','s_b', 'p_r','p_g','p_b', 'p_act','p_light'])
  pdata = data.drop(columns = ['s_r','s_g','s_b', 'p_r','p_g','p_b', 's_act','s_light'])

  sslices = common.slice_data(sdata, first_hour = first_hour, last_hour = last_hour)
  pslices = common.slice_data(pdata, first_hour = first_hour, last_hour = last_hour)

  ###

  fig, axs = plt.subplots(8,1, figsize=[12,18], constrained_layout=True)
  ax = axs.ravel()
  fig.suptitle(f'Activity (strong) and White Light (faint) of SUBJECT')
  fig.supxlabel('Time')
  scolors = ['brown', 'darkred']

  i = 0
  for slice in sslices:
    if i == 0: next # the first day is lacking some data
    slicename = f"slice {i+1}"
    print(f"plotting subject {slicename}")
    sslices[i].plot(ax = ax[i], kind = 'area', secondary_y = 's_act', color = scolors, legend = False, alpha = 0.5)
    ax[i].set_title(slicename)
    ax[i].set_xlabel('')
    ax[i].set_ylabel('lux')
    ax[i].right_ax.set_ylabel('counts/min')
    ax[i].set_ylim(0, light_max)
    ax[i].right_ax.set_ylim(0, act_max)
    i += 1

  if not sampling_time: sampling_time = '1Min'
  png = f'plots/plot3-subject_{sampling_time}Bin_{first_hour}-{last_hour}.png'
  print(f"writing {png}")
  plt.savefig(png, bbox_inches = 'tight', dpi = 500)
  plt.close()
  
  ###

  fig, axs = plt.subplots(8,1, figsize=[12,18], constrained_layout=True)
  ax = axs.ravel() # functions the same way as .reshape()
  fig.suptitle(f'Activity (strong) and White Light (faint) of BED PARTNER')
  fig.supxlabel('Time')
  pcolors = ['darkslateblue', 'slateblue']

  i = 0
  for slice in pslices:
    if i == 0: next # the first day is lacking some data
    slicename = f"slice {i+1}"
    print(f"plotting partner {slicename}")
    pslices[i].plot(ax = ax[i], kind = 'area', secondary_y = 'p_act', color = pcolors, legend = False, alpha = 0.5)
    ax[i].set_title(slicename)
    ax[i].set_xlabel('')
    ax[i].set_ylabel('lux')
    ax[i].right_ax.set_ylabel('counts/min')
    ax[i].set_ylim(0, light_max)
    ax[i].right_ax.set_ylim(0, act_max)
    i += 1

  if not sampling_time: sampling_time = '1Min'
  png = f'plots/plot3-partner_{sampling_time}Bin_{first_hour}-{last_hour}.png'
  print(f"writing {png}")
  plt.savefig(png, bbox_inches = 'tight', dpi = 600)
  plt.close()
