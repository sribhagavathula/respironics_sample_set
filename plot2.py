import common

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


'''
after seeing the data with the white light as compared to activity of both people,
then i got interested how much the colour of the light may be different between them?
'''
def make_plot(data, sampling_time = False, first_hour = 14, last_hour = 14):

  if sampling_time: data = common.resample_data(data, sampling_time)
  
  data = data.drop(columns = ['s_act','s_light', 'p_act','p_light'])
  time_slices = common.slice_data(data, first_hour = first_hour, last_hour = last_hour)

  # rows, cols, width, height
  fig, axs = plt.subplots(8,2, figsize = [6,18], constrained_layout = True)
  ax = axs.ravel()

  fig.suptitle(f'Percentages of R/G/B Colour of Subject/Bedpartner ({sampling_time} bin)')
  nice_colors = ['red', 'green', 'blue'] # because these colours are intuitive :)

  i = 0 # which slice
  j = 0 # which axis
  for slice in time_slices:
    if i == 0: next # the first day is lacking some data
    
    slicename = f"slice {i+1}"

    # add them up
    s_r_sum = time_slices[i].s_r.sum()
    s_g_sum = time_slices[i].s_g.sum()
    s_b_sum = time_slices[i].s_b.sum()
    s_total = s_r_sum + s_g_sum + s_b_sum
    p_r_sum = time_slices[i].p_r.sum()
    p_g_sum = time_slices[i].p_g.sum()
    p_b_sum = time_slices[i].p_b.sum()
    p_total = p_r_sum + p_g_sum + p_b_sum

    # create percentages
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.pie.html
    new_df = pd.DataFrame(
      {
        'subject': [(s_r_sum/s_total)*100, (s_g_sum/s_total)*100, (s_b_sum/s_total)*100],
        'partner': [(p_r_sum/p_total)*100, (p_g_sum/p_total)*100, (p_b_sum/p_total)*100]
      },
      index = ['red', 'green', 'blue']
    )

    # plot the exposure every night!
    # left side should be subject
    print(f"plotting subject onto axis {j}")
    s_ax = ax[j]
    new_df.plot(ax = s_ax, kind = 'pie', y = 'subject', colors = nice_colors, legend = False, labels=['','',''])
    s_ax.set_title('')
    s_ax.set_xlabel('')
    s_ax.set_ylabel(slicename)

    # right side should be bedpartner
    print(f"plotting partner onto axis {j+1}")
    p_ax = ax[j+1]
    new_df.plot(ax = p_ax, kind = 'pie', y = 'partner', colors = nice_colors, legend = False, labels=['','',''])
    p_ax.set_title('')
    p_ax.set_xlabel('')
    p_ax.set_ylabel('')

    i += 1
    j += 2
  
  if not sampling_time: sampling_time = '1Min'
  png = f'plots/plot2_{sampling_time}Bin_{first_hour}-{last_hour}.png'
  print(f"writing {png}")
  # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
  plt.savefig(png, bbox_inches = 'tight', dpi = 500)
  #plt.show()
  plt.close()
