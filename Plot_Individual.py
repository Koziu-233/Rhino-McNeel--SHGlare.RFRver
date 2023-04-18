import os
from datetime import date, datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

#----------///Public method definition///----------
def read_file(path):
    with open(path, 'r') as file:
        Lst_txt = file.readlines()
    dict = {}
    for txt in Lst_txt:
        Lst_data = txt.split('_')
        timestamp = Lst_data[0]
        grade = Lst_data[1].replace('\n', '')
        dict[timestamp] = grade
    return dict

def get_annual_day(year, month, day, date_start):
    try:
        date_now = date(year, month, day)
        delta = date_now - date_start
        num = delta.days
        return num
    except:
        return None

def get_daily_min(year, month, day, hour, min, sec, datetime_start):
    try:
        datetime_now = datetime(year, month, day, hour, min, sec)
        delta = datetime_now - datetime_start
        num = int(delta.seconds / 60)
        return num
    except:
        return None

def get_timestamp(month, day, hour, min):
    txt_mon = _treat_date(month)
    txt_day = _treat_date(day)
    txt_hr = _treat_date(hour)
    txt_min = _treat_date(min)
    txt_timestamp = txt_mon + '/' + txt_day + '/' + txt_hr + '/' + txt_min
    return txt_timestamp

def get_grade(key, dict):
    if key in dict.keys():
        txt = dict[key]
        if txt == 'A':
            return 1
        elif  txt == 'B':
            return 2
        else:
            return 3
    else:
        return 0

#----------///Methods for plot settings///----------
def get_x_labels(mon_start, mon_end, dom, date_start):
    Lst_num = []
    for mm in range(mon_start, mon_end):
        doy = get_annual_day(2022, mm, dom, date_start)
        Lst_num.append(doy)
    Lst_txt = ['JAN', 'FEB', 'MAR', 'APR',
               'MAY', 'JUN', 'JUL', 'AUG',
               'SEPT', 'OCT', 'NOV', 'DEC']
    return Lst_num, Lst_txt

def get_y_labels(hour_start, hour_end, min):
    Lst_num = []
    Lst_txt = []
    datetime_start = datetime(2022, 1, 1, hour_start, 0, 0)
    for hh in range(hour_start, hour_end):
        miod = get_daily_min(2022, 1, 1, hh, min, 0, datetime_start)
        txt = _treat_date(hh) + ':' + _treat_date(min)
        Lst_num.append(miod)
        Lst_txt.append(txt)
    return Lst_num, Lst_txt

def get_cmap(Lst_RGB):
    txt = 'custm_cmap'
    cmap = LinearSegmentedColormap.from_list(txt, Lst_RGB, N = len(Lst_RGB))
    return cmap


#----------///Private method definition///----------
def _treat_date(num):
    if num < 10:
        txt = '0' + str(num)
    else:
        txt = str(num)
    return txt

#----------///Main///----------
if __name__ == '__main__':
    #---///Get all file names in current folder///---
    path_current = os.getcwd()
    path_parent = path_current.replace('Images', '')
    path_result = path_parent + 'Results'
    File_Names = []
    for root, dirs, files in os.walk(path_result):
        for file_name in files:
            if file_name.find("Result") != -1 and file_name.find(".txt") != -1:
                File_Names.append(file_name)
    
    #---/General settings/---
    date_start = date(2022, 1, 1)
    dd_start = 1
    dd_end = 365
    hh_start = 4
    hh_end = 21
    Days = np.arange(0, dd_end - dd_start + 1, 1)
    Mins = np.arange(0, (hh_end - hh_start) * 60, 1)
    Xs, Ys = np.meshgrid(Days, Mins)

    #---/General plot settings/---
    #-/Extend the x and y axis to use a flat shading/-
    Xs_plot = np.arange(0, dd_end - dd_start + 2, 1)
    Ys_plot = np.arange(0, (hh_end - hh_start) * 60 + 1, 1)

    #-/Color settings/-
    cmap_l = get_cmap([(1, 1, 1), (1, 0.93, 0.62), (1, 0.47, 0.11), (0.76, 0, 0.13)])
    cmap_d = plt.colormaps['magma']
    #------------------------------------------------------------------------------------------------------
    cmap_choose = cmap_l # <<<<<<<<======================================<<<<<<<< CHANGE CMAP HERE <<<<<<<<
    #------------------------------------------------------------------------------------------------------
    Bounds_color = [0, 1, 2, 3, 4]
    norm = mpl.colors.BoundaryNorm(Bounds_color, cmap_choose.N, extend = 'neither')

    for file_name in File_Names:
        #---/Read the txt file/---
        path_file = path_result + "\\" + file_name
        dict_result = read_file(path_file)
        
        
        #---/Sub settings/---
        Grades = np.zeros_like(Xs)
        Lst_name = file_name.split('_')
        idx_window = int(Lst_name[-1].replace('.txt', ''))
        #--------------------------------------------------------------------------------------------------
        reflectance = '10%' # <<<<<<<<============================<<<<<<<< CHANGE REFLECTANCE HERE <<<<<<<<
        #--------------------------------------------------------------------------------------------------

        #---/Iterate the months/---
        for mm in range(1, 13):
            #---/Iterate the days/---
            for dd in range(1, 32):
                doy = get_annual_day(2022, mm, dd, date_start)
                if doy:
                    datetime_start = datetime(2022, mm, dd, hh_start, 0, 0)
                    #---/Iterate the hours/---
                    for hh in range(hh_start, hh_end):
                        #---/Iterate the minutes/---
                        for mimi in range(60):
                            miod = get_daily_min(2022, mm, dd, hh, mimi, 0, datetime_start)
                            timestamp = get_timestamp(mm, dd, hh, mimi)
                            Grades[miod, doy] = get_grade(timestamp, dict_result)
        
        #-/Initiate the figure/-
        fig, ax = plt.subplots(layout = 'compressed', figsize = (24, 30))
        font01 = {'color':'black', 'size':20}
        txt_title = 'Annual Glare Rates of Window NO.' + str(idx_window) + ' with Glass Reflectance = ' + reflectance
        plt.title(txt_title, fontdict = font01, y = 1.02)

        #-/Set the x labels/-
        [X_values, Txts_mon] = get_x_labels(1, 13, 15, date_start)
        ax.set_xticks(X_values, labels = Txts_mon, fontsize = 20)
        plt.xlabel('Days in each month', fontdict = font01)


        #-/Set the major y labels/-
        [Y_values1, Txts_hour1] = get_y_labels(hh_start, hh_end, 0)
        ax.set_yticks(Y_values1, labels = Txts_hour1, minor = False, fontsize = 20)
        plt.ylabel('Times in day', fontdict = font01)

        #-/Set the minor y labels/-
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        [Y_values2, Txts_hour2] = get_y_labels(hh_start, hh_end, 30)
        ax.set_yticks(Y_values2, labels = Txts_hour2, minor = True, fontsize = 15)

        #-/Draw Vertical lines/-
        [X_values, Txts_mon] = get_x_labels(1, 13, 1, date_start)
        for x_value in X_values[1:]:
            plt.axvline(x = x_value, color = '#66B2FF', linestyle = '-', linewidth = 0.5)

        #-/Draw horizontal lines/-
        for y_value in Y_values1:
            plt.axhline(y = y_value, color = '#66B2FF', linestyle = '-', linewidth = 0.5)
        for y_value in Y_values2:
            plt.axhline(y = y_value, color = '#66B2FF', linestyle = '--', linewidth = 0.5)

        #---/Plot the mesh/---
        img = ax.pcolormesh(Xs_plot, Ys_plot, Grades, shading='flat', cmap=cmap_choose, norm=norm)

        #---/Plot the color bar/---
        clb = fig.colorbar(img, shrink = 0.1, aspect = 4, anchor = (0.0, 0.0), drawedges = False)
        clb.set_ticks([0.5, 1.5, 2.5, 3.5], labels=['No Reflection', 'Acceptable', 'Minor impact', 'Major impact'])
        clb.ax.tick_params(labelsize=20)

        #---/Post plotting actions/---
        #plt.show()
        figure_name = 'Window_NO.' + str(idx_window) + '_R' + reflectance + '.png'
        plt.savefig(figure_name)