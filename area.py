#%%
import matplotlib.pyplot as plt
import numpy as np

from util import *

plt.rcParams['xtick.labeltop'] = True
plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.facecolor'] = 'none' #'#E4E9E9'
plt.rcParams['figure.facecolor'] = 'none' #'#E4E9E9'
plt.rcParams['legend.facecolor'] = 'whitesmoke'


month2num = {'Jan':1, 'Fev':2, 'Mar':3, 'Abr':4, 'Mai':5, 'Jun':6,
             'Jul':7, 'Ago':8, 'Set':9, 'Out':10, 'Nov':11, 'Dez':12,
             'Janeiro':1, 'Fevereiro':2, 'Março':3, 'Abril':4, 'Maio':5,
             'Junho':6, 'Julho':7, 'Agosto':8, 'Setembro':9, 'Outubro':10,
             'Novembr':11, 'Dezembro':12}

def plotEvolution(dates, massa_gorda, massa_magra, dpi=500):
    datesNum = [month2num[date] for date in dates]
    fig, ax = plt.subplots(1,1, dpi=dpi)
    ax.fill_between(datesNum, massa_gorda, label="Massa Gorda", color='#CBE0E9', linestyle='-', linewidth=1.0)
    ax.fill_between(datesNum, massa_magra, label="Massa Magra", color='#A3E7D6', linestyle='-', linewidth=1.0)
    ax.set_xticks(datesNum)
    ax.set_xticklabels(dates)
    ax.grid(linestyle='dashed', color='grey', alpha=.2, linewidth=.5)
    ax.set_ylabel('Percentual')
    ax.legend(loc='lower center', ncol=1, borderaxespad=4)
    return fig, ax

def runPlotExample(dpi=100):
    ypad=5
    massa_gorda = [33-ypad, 30-ypad, 31-ypad, 28-ypad]
    massa_magra = [18-ypad, 22-ypad, 21-ypad, 23-ypad]

    dates = ['17 Jan 21', '18 Jul 21', '19 Ago 21', '20 Set 21']
    dates = [date.split()[1] for date in dates]

    fig, _ = plotEvolution(dates, massa_gorda, massa_magra, dpi=dpi)
    return image2array(fig, dpi=dpi)

# %%
