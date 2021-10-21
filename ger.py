#%%
import numpy as np
import matplotlib.pyplot as plt

from util import *

#%%
Harris = {'male':lambda weight, height, age: 66.4730+13.7516*weight+5.0033*height-6.7550*age,
          'female':lambda weight, height, age: 655.0955+9.5624*weight+1.8496*height-4.6756*age}

Mifflin = {'male':lambda weight, height, age: (9.99*weight)+(6.25*height)-(4.92*age)+5,
            'female':lambda weight, height, age: (9.99*weight)+(6.25*height)-(4.92*age)-161}

Owen = {'male': lambda weight, height, age: 879+10.2*weight,
        'female': lambda weight, height, age: 795+7.18*weight}

Frankenfield1 = {'male': lambda weight, height, age: (10*weight+3*height-5*age+684,
                                                     10*weight+3*height-5*age+661),
                 'female': lambda weight, height, age:(10*weight+3*height-5*age+440,
                                                      10*weight+3*height-5*age+454)}

Frankenfield2 = {'male': lambda weight, height, age: (10*weight-5*age+1139,
                                                      11*weight-6*age+1068),
                 'female': lambda weight, height, age: (10*weight-5*age+865,
                                                        11*weight-6*age+838)}

Schofield = {'male': lambda weight, height, age: ((0.063*weight+2.896)*239,
                                                    (0.048*weight+3.653)*239),
             'female': lambda weight, height, age: ((0.062*weight+2.036)*239,
                                                    (0.034*weight+3.538)*239)}

Joint1 = {'male': lambda weight, height, age: (15.2*weight+679,
                                               11.6*weight+879),
        'female': lambda weight, height, age: (14.7*weight+496,
                                                8.7*weight+829)}

Joint2 = {'male': lambda weight, height, age: (15.4*weight+0.27*height+717,
                                               11.3*weight+0.16*height+901),
          'female': lambda weight, height, age: (13.3*weight+3.34*height+35,
                                                 8.7*weight+0.25*height+865),}

Henry = {'male': lambda weight, height, age: ((0.057*weight-0.00429*height+3.412)*239,
                                              (0.046*weight-0.00081*height+3.277)*239),
         'female': lambda weight, height, age: ((0.042*weight+0.01546*height+0.433)*239,
                                                0.047*weight+0.00145*height+2.256)*239}

Ireton = {'male': lambda weight, height, age: (629-11*age+25*weight,
                                               629-11*age+25*weight-609),
          'female': lambda weight, height, age: (629-11*age+25*weight,
                                                 629-11*age+25*weight-609)}

Livingston1 = {'male': lambda weight, height, age: 239*weight**0.4330-5.92*age,
               'female': lambda weight, height, age: 248*weight**0.4356-5.09*age}

Livingston2 = {'male': lambda weight, height, age: 246*weight**0.4473,
               'female': lambda weight, height, age: 196*weight**0.4613}

def methodsGER():
    return [Mifflin, Schofield, Owen, Henry, Harris, Frankenfield1, Frankenfield2]

# %%
def getGET(gender, weight, height, age):
    GERs = [each[gender](weight, height, age) for each in methodsGER()]
    GERs = np.array(list(flatten(GERs)))

    averageGET = np.array([GERs.mean()*ratio for ratio in [1.2, 1.4, 1.6, 1.8, 2.0]])
    dailyDeficit = averageGET - 1000
    monthlyDeficit = dailyDeficit * 7 * 4

    dailyLoose = dailyDeficit*0.143
    monthlyLoose = monthlyDeficit*0.143
    
    return dailyLoose, monthlyLoose

# %%
def plotTableGET(gender, weight, height, age, dpi=500, **kwargs):
    fig, ax = plt.subplots(1,1,dpi=dpi)
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    daily, monthly = getGET(gender, weight, height, age)
    tables = ax.table(cellText=[np.round(daily, 2), np.round(monthly, 2)], colLabels=[1.2,1.4,1.6,1.8,2.0], rowLabels=['Diário','Mensal'], loc='center')
    tables.auto_set_font_size(False)
    
    for cell in tables._cells:
        tables._cells[cell].set_facecolor('None')
        
        if cell[0] != 0:
            tables._cells[cell].set_height(0.2)
            if cell[0] % 2 == 0:
                tables._cells[cell].set_facecolor('#CBE0E9')
            else:
                tables._cells[cell].set_facecolor('#A3E7D6')
        
        if cell[-1] == -1:
            tables._cells[cell].get_text().set_rotation(90)
            tables._cells[cell].get_text().set_fontsize(12)
            tables._cells[cell].get_text().set_horizontalalignment('right')
            tables._cells[cell].visible_edges = 'horizontal'
        
        if cell[0] == 0:
            tables._cells[cell].get_text().set_fontsize(12)
            tables._cells[cell].visible_edges = 'vertical'

    fig.tight_layout()
    return image2array(fig, dpi=dpi)

# %%
