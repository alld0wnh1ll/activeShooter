import pandas as pd
import pip
import matplotlib.pyplot as plt
pip.main(["install", "pandas"])
pip.main(["install", "openpyxl"])
pip.main(["install", "researchpy"])
input_file = r'CCW_SRO-11-30-22-(2-60) - used with paper.xlsx'
import numpy as np



desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',10)

df = pd.read_excel(input_file)
df = df[df['sro delay'] < 50]


def remove_outlier(df_in, col_name, baseline):
    q1 = df_in[col_name].quantile(0.00001)
    q3 = df_in[col_name].quantile(0.99999)
    iqr = baseline[col_name].std()
    fence_low  = q1 + 6
    fence_high = q3 - 6
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out


## 30/10  Baseline NO_FF

df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')
df_hide30_b = df_hide30
df_hide30 = remove_outlier(df_hide30, 'ui rhf casualty', df_hide30_b)

no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide30['sro delay'].unique()


xb = no_sro_ccw_response
yb = no_sro_ccw1
stdb = no_sro_ccw['ui rhf casualty'].std()

## 30/10  CCW ONLY NO_FF


df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')

no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide30['sro delay'].unique()


x0 = no_sro_ccw_response
y0 = no_sro_ccw1
std0 = no_sro_ccw['ui rhf casualty'].std()



## 30/10 SRO Only No_FF


df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')




df_hide30 = remove_outlier(df_hide30, 'ui rhf casualty', df_hide30_b)
print('mean ',df_hide30.groupby(['fight range']).mean()['ui rhf casualty'])
no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide30['sro delay'].unique()
x1 = no_sro_ccw_response
y1 = no_sro_ccw1
std1 = no_sro_ccw['ui rhf casualty'].std()



## 30/10 Both No_FF


df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 1"
                    "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')
no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide30['sro delay'].unique()
x2 = no_sro_ccw_response
y2 = no_sro_ccw1
std2 = no_sro_ccw['ui rhf casualty'].std()



### Line Chart Createion
x_base = np.linspace(0,50,50) 
y_base = np.repeat(yb,50)  
y0b = np.repeat(y0,50)



### SRO Only line
plt.plot(x1, y1, 'bo-', label='SRO/NO CCW  std={0:2.2f}'.format(std1))
for x,y in zip(x1,y1):
    plt.annotate(xy=(x,y+.25), text='{0:2.2f}'.format(y) ,ha='center')


### Both Only line
plt.plot(x2, y2, 'ro-', label='SRO/CCW  std={0:2.2f}'.format(std2))
for x,y in zip(x2,y2):
    plt.annotate(xy=(x,y+.25), text='{0:2.2f}'.format(y) ,ha='center' )


### Baseline
plt.plot(x_base, y_base, '--', label='NO CCW/NO SRO  std={0:2.2f}'.format(stdb))
plt.annotate(xy=(x_base[0], y_base[0]-.4), text='Baseline with no support {0:2.2f}'.format(y_base[0]))


### CCW Only
plt.plot(x_base, y0b, '--', label='CCW/NO SRO   std={0:2.2f}'.format(std0))




plt.xlabel('SRO Response Time (seconds)')
plt.ylabel('Total Casualties (AVG/100 Iterations)')
plt.title('30 Hide/10 Fight Scenario -- No Friendly Fire')
plt.legend(loc='upper right')
plt.show()


###  Analysis on SRO, CCW, and Shooter's survivability


labels = ['No SRO', '<=10', '<=30', '<=60']
df_hide30 = df.query("`fight range` == 10 & `hide range` >= 30 & `friendly fire percent` == 0").sort_values('sro delay')
ccw_perc = [round(df_hide30['ccw casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['ccw casualty'].loc[df['sro number'] == 0].count() * 100 ,
               round(df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]

sro_perc = [round(df_hide30['sro casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['sro casualty'].loc[df['sro number'] == 0].count() * 100,
               round(df_hide30['sro casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['sro casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]
shooter_death =  [df_hide30['as dead'].loc[df['sro number'] == 0].sum()/df_hide30['as dead'].loc[df['sro number'] == 0].count()*50,
                  df_hide30['as dead'].loc[df['sro delay'] <= 10].sum()/df_hide30['as dead'].loc[df['sro delay'] <= 10].count()*50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 50]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()


rects1 = ax.bar(x - width,  ccw_perc, width, label='CCW Deaths', align='center')
rects2 = ax.bar(x , sro_perc, width, label='SRO Deaths', align='center')
rects3 = ax.bar(x + width, shooter_death, width, label='Shooter Deaths', align='center')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('CCW, SRO, Shooter Deaths (Percentage %)')
ax.set_xlabel('SRO Response Time (seconds)')
ax.set_title('CCW, SRO, and Shooter Death Percentages / Total Iterations / SRO Delay')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f"{height/100:.0%}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.show()







## 100 Hide Baseline No_FF



df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')
df_hide100_b = df_hide100

no_sro_ccw = df_hide100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide100['sro delay'].unique()

xb = no_sro_ccw_response
yb = no_sro_ccw1
stdb = no_sro_ccw['ui rhf casualty'].std()




## 30/10 CCW Only No_FF


df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')
df_hide100 = remove_outlier(df_hide100, 'ui rhf casualty', df_hide100_b)
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()

no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide100['sro delay'].unique()


x0 = no_sro_ccw_response
y0 = no_sro_ccw1
std0 = no_sro_ccw['ui rhf casualty'].std()



## 30/10 SRO Only No_FF




df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')
df_hide100  = remove_outlier(df_hide100 , 'ui rhf casualty', df_hide100_b)
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()

no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide100['sro delay'].unique()

x1 = no_sro_ccw_response
y1 = no_sro_ccw1
std1 = no_sro_ccw['ui rhf casualty'].std()






## 30/10 Both No_FF

f_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 1"
                    "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')
df_hide100 = df.query("`fight range` == 10 & `hide range` == 30").sort_values('sro delay')
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide100['sro delay'].unique()


x2 = no_sro_ccw_response
y2 = no_sro_ccw1
std2 = no_sro_ccw['ui rhf casualty'].std()


x_base = np.linspace(0,50,50)
y_base = np.repeat(yb,50)
y0b = np.repeat(y0,50)

plt.plot(x1, y1, 'bo-', label='SRO/NO CCW  std={0:2.2f}'.format(std1))
for x,y in zip(x1,y1):
    plt.annotate(xy=(x,y+2), text='{0:2.2f}'.format(y) ,ha='center')
plt.plot(x2, y2, 'ro-', label='SRO/CCW  std={0:2.2f}'.format(std2))
for x,y in zip(x2,y2):
    plt.annotate(xy=(x,y+2), text='{0:2.2f}'.format(y) ,ha='center' )


plt.plot(x_base, y_base, '--', label='NO CCW/NO SRO  std={0:2.2f}'.format(stdb))
plt.annotate(xy=(x_base[0], y_base[0]-1.5), text='Baseline with no support {0:2.2f}'.format(y_base[0]))
plt.plot(x_base, y0b, '--', label='CCW/NO SRO   std={0:2.2f}'.format(std0))




plt.xlabel('SRO Response Time (seconds)')
plt.ylabel('Total Casualties (AVG/100 Iterations)')
plt.title('All Hide Scenario -- No Friendly Fire')
plt.legend(loc='upper right')
plt.show()



### Analysis on CCW|SRO|Shooter Survivability


df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `friendly fire percent` == 0").sort_values('sro delay')
ccw_perc = [round(df_hide100['ccw casualty'].loc[df['sro number'] == 0].sum())/
               df_hide100['ccw casualty'].loc[df['sro number'] == 0].count() * 100 ,
               round(df_hide100['ccw casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide100['ccw casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide100['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide100['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide100['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide100['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]

sro_perc = [round(df_hide100['sro casualty'].loc[df['sro number'] == 0].sum())/
               df_hide100['sro casualty'].loc[df['sro number'] == 0].count() * 100,
               round(df_hide100['sro casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide100['sro casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide100['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide100['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide100['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide100['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]
shooter_death =  [df_hide100['as dead'].loc[df['sro number'] == 0].sum()/df_hide100['as dead'].loc[df['sro number'] == 0].count()*50,
                  df_hide100['as dead'].loc[df['sro delay'] <= 10].sum()/df_hide100['as dead'].loc[df['sro delay'] <= 10].count()*50,
                  df_hide100['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum()/
                  df_hide100['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 50,
                  df_hide100['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum()/
                  df_hide100['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 50]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()


rects1 = ax.bar(x - width,  ccw_perc, width, label='CCW Deaths', align='center')
rects2 = ax.bar(x , sro_perc, width, label='SRO Deaths', align='center')
rects3 = ax.bar(x + width, shooter_death, width, label='Shooter Deaths', align='center')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('CCW, SRO, Shooter Deaths (Percentage %)')
ax.set_xlabel('SRO Response Time (seconds)')
ax.set_title('CCW, SRO, and Shooter Death Percentages / Total Iterations / SRO Delay')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f"{height/100:.0%}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.show()




## 100 Run Baseline No_FF



df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')
df_run100_b = df_run100

no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_run100['sro delay'].unique()


xb = no_sro_ccw_response
yb = no_sro_ccw1
stdb = no_sro_ccw['ui rhf casualty'].std()



## 100 CCW Only No_FF


df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_run100['sro delay'].unique()

x0 = no_sro_ccw_response
y0 = no_sro_ccw1
std0 = no_sro_ccw['ui rhf casualty'].std()



## 100 SRO Only No_FF




df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_run100['sro delay'].unique()
x1 = no_sro_ccw_response
y1 = no_sro_ccw1
std1 = no_sro_ccw['ui rhf casualty'].std()






## 100 Run Both No_FF

df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 1"
                    "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')

no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_run100['sro delay'].unique()


x2 = no_sro_ccw_response
y2 = no_sro_ccw1
std2 = no_sro_ccw['ui rhf casualty'].std()


x_base = np.linspace(0,50,50)
y_base = np.repeat(yb,50)
y0b = np.repeat(y0,50)

plt.plot(x1, y1, 'bo-', label='SRO/NO CCW  std={0:2.2f}'.format(std1))
for x,y in zip(x1,y1):
    plt.annotate(xy=(x,y+.15), text='{0:2.2f}'.format(y) ,ha='center')
plt.plot(x2, y2, 'ro-', label='SRO/CCW  std={0:2.2f}'.format(std2))
for x,y in zip(x2,y2):
    plt.annotate(xy=(x,y+.15), text='{0:2.2f}'.format(y) ,ha='center' )


plt.plot(x_base, y_base, '--', label='NO CCW/NO SRO  std={0:2.2f}'.format(stdb))
plt.annotate(xy=(x_base[0], y_base[0]-.55), text='Baseline with no support {0:2.2f}'.format(y_base[0]))
plt.plot(x_base, y0b, '--', label='CCW/NO SRO   std={0:2.2f}'.format(std0))




plt.xlabel('SRO Response Time (seconds)')
plt.ylabel('Total Casualties (AVG/100 Iterations)')
plt.title('All Run Scenario -- No Friendly Fire')
plt.legend(loc='upper right')
plt.show()


labels = ['No SRO', '<=10', '<=30', '<=60']


## 100 Run CCW | SRO | Shooter Analysis


df_run100 = df.query("`fight range` == 0 & `hide range` >= 0 & `friendly fire percent` == 0").sort_values('sro delay')
ccw_perc = [round(df_run100['ccw casualty'].loc[df['sro number'] == 0].sum())/
               df_run100['ccw casualty'].loc[df['sro number'] == 0].count() * 100 ,
               round(df_run100['ccw casualty'].loc[df['sro delay'] <= 10].sum())/
               df_run100['ccw casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_run100['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_run100['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_run100['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_run100['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]

sro_perc = [round(df_run100['sro casualty'].loc[df['sro number'] == 0].sum())/
               df_run100['sro casualty'].loc[df['sro number'] == 0].count() * 100,
               round(df_run100['sro casualty'].loc[df['sro delay'] <= 10].sum())/
               df_run100['sro casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_run100['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_run100['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_run100['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_run100['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]
shooter_death =  [df_run100['as dead'].loc[df['sro number'] == 0].sum()/df_run100['as dead'].loc[df['sro number'] == 0].count()*50,
                  df_run100['as dead'].loc[df['sro delay'] <= 10].sum()/df_run100['as dead'].loc[df['sro delay'] <= 10].count()*50,
                  df_run100['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum()/
                  df_run100['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 50,
                  df_run100['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum()/
                  df_run100['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 50]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()


rects1 = ax.bar(x - width,  ccw_perc, width, label='CCW Deaths', align='center')
rects2 = ax.bar(x , sro_perc, width, label='SRO Deaths', align='center')
rects3 = ax.bar(x + width, shooter_death, width, label='Shooter Deaths', align='center')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('CCW, SRO, Shooter Deaths (Percentage %)')
ax.set_xlabel('SRO Response Time (seconds)')
ax.set_title('CCW, SRO, and Shooter Death Percentages / Total Iterations / SRO Delay')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f"{height/100:.0%}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.show()





#FRIENDLY FIRE STARTS HERE  -- Outliers not removed


## 30/10 Baseline FF



df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide30['sro delay'].unique()

xb = no_sro_ccw_response
yb = no_sro_ccw1
stdb = no_sro_ccw['ui rhf casualty'].std()


## 30/10 CCW Only FF


df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide30['sro delay'].unique()

x0 = no_sro_ccw_response
y0 = no_sro_ccw1
std0 = no_sro_ccw['ui rhf casualty'].std()





## 30/10 SRO Only FF


df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide30['sro delay'].unique()
x1 = no_sro_ccw_response
y1 = no_sro_ccw1
std1 = no_sro_ccw['ui rhf casualty'].std()






## 30/10 Both FF

f_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 1"
                    "& `ccw number` == 1 & `friendly fire percent` > 0").sort_values('sro delay')
df_hide30 = df.query("`fight range` == 10 & `hide range` == 30").sort_values('sro delay')
no_sro_ccw = df_hide30.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide30['sro delay'].unique()
x2 = no_sro_ccw_response
y2 = no_sro_ccw1
std2 = no_sro_ccw['ui rhf casualty'].std()

x_base = np.linspace(0,50,50)
y_base = np.repeat(yb,50)
y0b = np.repeat(y0,50)

plt.plot(x1, y1, 'bo-', label='SRO/NO CCW  std={0:2.2f}'.format(std1))
for x,y in zip(x1,y1):
    plt.annotate(xy=(x,y+.25), text='{0:2.2f}'.format(y) ,ha='center')
plt.plot(x2, y2, 'ro-', label='SRO/CCW  std={0:2.2f}'.format(std2))
for x,y in zip(x2,y2):
    plt.annotate(xy=(x,y+.25), text='{0:2.2f}'.format(y) ,ha='center' )


plt.plot(x_base, y_base, '--', label='NO CCW/NO SRO  std={0:2.2f}'.format(stdb))
plt.annotate(xy=(x_base[0], y_base[0]-.4), text='Baseline with no support {0:2.2f}'.format(y_base[0]))
plt.plot(x_base, y0b, '--', label='CCW/NO SRO   std={0:2.2f}'.format(std0))




plt.xlabel('SRO Response Time (seconds)')
plt.ylabel('Total Casualties (AVG/100 Iterations)')
plt.title('30 Hide/10 Fight Scenario - Friendly Fire')
plt.legend(loc='upper right')
plt.show()




### Friendly Fire Assessment on 30/10


labels = x1
df_hide30 = df.query("`fight range` == 10 & `hide range` >= 30 & `friendly fire percent` > 0").sort_values('sro delay')
ccw_perc = [round(df_hide30['ccw casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['ccw casualty'].loc[df['sro number'] == 0].count() * 100 ,
               round(df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]

sro_perc = [round(df_hide30['sro casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['sro casualty'].loc[df['sro number'] == 0].count() * 100,
               round(df_hide30['sro casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['sro casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]
shooter_death =  [df_hide30['as dead'].loc[df['sro number'] == 0].sum()/df_hide30['as dead'].loc[df['sro number'] == 0].count()*50,
                  df_hide30['as dead'].loc[df['sro delay'] <= 10].sum()/df_hide30['as dead'].loc[df['sro delay'] <= 10].count()*50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 50]
friendly_death =  df_hide30.groupby('sro delay').sum()['friendly fire']/df_hide30.groupby('sro delay').count()['friendly fire'] * 100


x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()



rects4 = ax.bar(x , friendly_death, width, label='Friendly Fire Incident Likelihood', align='center', color='red')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percentage of Samples that had a Friendly Fire Incident (Percentage %)')
ax.set_xlabel('SRO Response Time (seconds)')
ax.set_title('Percentage of Samples with Friendly Fire Incident 30-Hide/10-Fight')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(text="{0:2.2f}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



autolabel(rects4)

fig.tight_layout()

plt.show()







## 100 Hide Baseline FF



df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide100['sro delay'].unique()


xb = no_sro_ccw_response
yb = no_sro_ccw1
stdb = no_sro_ccw['ui rhf casualty'].std()


## 100 Hide CCW Only FF


df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_hide100['sro delay'].unique()
x0 = no_sro_ccw_response
y0 = no_sro_ccw1
std0 = no_sro_ccw['ui rhf casualty'].std()

## 100 Hide SRO Only FF

df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide100['sro delay'].unique()
x1 = no_sro_ccw_response
y1 = no_sro_ccw1
std1 = no_sro_ccw['ui rhf casualty'].std()



## 100 Hide CCW Only FF

df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 1"
                    "& `ccw number` == 1 & `friendly fire percent` > 0").sort_values('sro delay')
df_hide100 = df.query("`fight range` == 10 & `hide range` == 30").sort_values('sro delay')
no_sro_ccw = df_hide100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_hide100['sro delay'].unique()
x2 = no_sro_ccw_response
y2 = no_sro_ccw1
std2 = no_sro_ccw['ui rhf casualty'].std()

x_base = np.linspace(0,50,50)
y_base = np.repeat(yb,50)
y0b = np.repeat(y0,50)

plt.plot(x1, y1, 'bo-', label='SRO/NO CCW  std={0:2.2f}'.format(std1))
for x,y in zip(x1,y1):
    plt.annotate(xy=(x,y+2), text='{0:2.2f}'.format(y) ,ha='center')
plt.plot(x2, y2, 'ro-', label='SRO/CCW  std={0:2.2f}'.format(std2))
for x,y in zip(x2,y2):
    plt.annotate(xy=(x,y+2), text='{0:2.2f}'.format(y) ,ha='center' )


plt.plot(x_base, y_base, '--', label='NO CCW/NO SRO  std={0:2.2f}'.format(stdb))
plt.annotate(xy=(x_base[0], y_base[0]-1.5), text='Baseline with no support {0:2.2f}'.format(y_base[0]))
plt.plot(x_base, y0b, '--', label='CCW/NO SRO   std={0:2.2f}'.format(std0))




plt.xlabel('SRO Response Time (seconds)')
plt.ylabel('Total Casualties (AVG/100 Iterations)')
plt.title('All Hide Scenario - Friendly Fire')
plt.legend(loc='upper right')
plt.show()

### CCW | SRO | SHOOTER SURVIVABILITY Analysis FF

labels = ['No SRO', '<=10', '<=30', '<=60']
df_hide30 = df.query("`fight range` == 0 & `hide range` >= 90 & `friendly fire percent` > 0").sort_values('sro delay')
ccw_perc = [round(df_hide30['ccw casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['ccw casualty'].loc[df['sro number'] == 0].count() * 100 ,
               round(df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]

sro_perc = [round(df_hide30['sro casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['sro casualty'].loc[df['sro number'] == 0].count() * 100,
               round(df_hide30['sro casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['sro casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]
shooter_death =  [df_hide30['as dead'].loc[df['sro number'] == 0].sum()/df_hide30['as dead'].loc[df['sro number'] == 0].count()*50,
                  df_hide30['as dead'].loc[df['sro delay'] <= 10].sum()/df_hide30['as dead'].loc[df['sro delay'] <= 10].count()*50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 50]
friendly_death =  [df_hide30['friendly fire'].loc[df['sro number'] == 0].mean()/5600,
                  df_hide30['friendly fire'].loc[df['sro delay'] <= 10].mean()/5600,
                  df_hide30['friendly fire'].loc[(df['sro delay'] > 10).sum() & (df['sro delay'] <= 30)].mean()/
                  56*100,
                  df_hide30['friendly fire'].loc[(df['sro delay'] > 30).sum() & (df['sro delay'] <= 60)].mean()/
                  56*100]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()


rects1 = ax.bar(x - width,  ccw_perc, width, label='CCW Deaths', align='center')
rects2 = ax.bar(x , sro_perc, width, label='SRO Deaths', align='center')
rects3 = ax.bar(x + width, shooter_death, width, label='Shooter Deaths', align='center')
rects4 = ax.bar(x + width*2, friendly_death, width, label='Friendly Deaths', align='center')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('CCW, SRO, Shooter Deaths (Percentage %)')
ax.set_xlabel('SRO Response Time (seconds)')
ax.set_title('CCW, SRO, and Shooter Death Percentages / Total Iterations / SRO Delay')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(text="{0:2.2%}".format(height/100),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)

fig.tight_layout()

plt.show()




## 100 run Baseline FF



df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_run100['sro delay'].unique()

xb = no_sro_ccw_response
yb = no_sro_ccw1
stdb = no_sro_ccw['ui rhf casualty'].std()


df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty'].mean()
no_sro_ccw_response = df_run100['sro delay'].unique()
x0 = no_sro_ccw_response
y0 = no_sro_ccw1
std0 = no_sro_ccw['ui rhf casualty'].std()

## 100 Run SRO Only FF


df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_run100['sro delay'].unique()
x1 = no_sro_ccw_response
y1 = no_sro_ccw1
std1 = no_sro_ccw['ui rhf casualty'].std()



## 100 Run Both FF

df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 1"
                    "& `ccw number` == 1 & `friendly fire percent` > 0").sort_values('sro delay')
no_sro_ccw = df_run100.groupby(['sro delay']).mean()
no_sro_ccw1 = no_sro_ccw['ui rhf casualty']
no_sro_ccw_response = df_run100['sro delay'].unique()

x2 = no_sro_ccw_response
y2 = no_sro_ccw1
std2 = no_sro_ccw['ui rhf casualty'].std()

x_base = np.linspace(0,50,50)
y_base = np.repeat(yb,50)
y0b = np.repeat(y0,50)

plt.plot(x1, y1, 'bo-', label='SRO/NO CCW  std={0:2.2f}'.format(std1))
for x,y in zip(x1,y1):
    plt.annotate(xy=(x,y+1), text='{0:2.2f}'.format(y) ,ha='center')
plt.plot(x2, y2, 'ro-', label='SRO/CCW  std={0:2.2f}'.format(std2))
for x,y in zip(x2,y2):
    plt.annotate(xy=(x,y+1), text='{0:2.2f}'.format(y) ,ha='center' )


plt.plot(x_base, y_base, '--', label='NO CCW/NO SRO  std={0:2.2f}'.format(stdb))
plt.annotate(xy=(x_base[0], y_base[0]-.75), text='Baseline with no support {0:2.2f}'.format(y_base[0]))
plt.plot(x_base, y0b, '--', label='CCW/NO SRO   std={0:2.2f}'.format(std0))




plt.xlabel('SRO Response Time (seconds)')
plt.ylabel('Total Casualties (AVG/100 Iterations)')
plt.title('All Run Scenario -- Friendly Fire')
plt.legend(loc='upper right')
plt.show()



## CCW | SRO | Shooters Surviability Analysis FF


labels = ['No SRO', '<=10', '<=30', '<=60']
df_hide30 = df.query("`fight range` == 0 & `hide range` >= 0 & `friendly fire percent` > 0").sort_values('sro delay')
ccw_perc = [round(df_hide30['ccw casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['ccw casualty'].loc[df['sro number'] == 0].count() * 100 ,
               round(df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['ccw casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['ccw casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]

sro_perc = [round(df_hide30['sro casualty'].loc[df['sro number'] == 0].sum())/
               df_hide30['sro casualty'].loc[df['sro number'] == 0].count() * 100,
               round(df_hide30['sro casualty'].loc[df['sro delay'] <= 10].sum())/
               df_hide30['sro casualty'].loc[df['sro delay'] <= 10].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 100,
               round(df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum())/
               df_hide30['sro casualty'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 100]
shooter_death =  [df_hide30['as dead'].loc[df['sro number'] == 0].sum()/df_hide30['as dead'].loc[df['sro number'] == 0].count()*50,
                  df_hide30['as dead'].loc[df['sro delay'] <= 10].sum()/df_hide30['as dead'].loc[df['sro delay'] <= 10].count()*50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 10) & (df['sro delay'] <= 30)].count() * 50,
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].sum()/
                  df_hide30['as dead'].loc[(df['sro delay'] > 30) & (df['sro delay'] <= 60)].count() * 50]
friendly_death =  [df_hide30['friendly fire'].loc[df['sro number'] == 0].mean()/5600,
                  df_hide30['friendly fire'].loc[df['sro delay'] <= 10].mean()/5600,
                  df_hide30['friendly fire'].loc[(df['sro delay'] > 10).sum() & (df['sro delay'] <= 30)].mean()/
                  56*100,
                  df_hide30['friendly fire'].loc[(df['sro delay'] > 30).sum() & (df['sro delay'] <= 60)].mean()/
                  56*100]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()


rects1 = ax.bar(x - width,  ccw_perc, width, label='CCW Deaths', align='center')
rects2 = ax.bar(x , sro_perc, width, label='SRO Deaths', align='center')
rects3 = ax.bar(x + width, shooter_death, width, label='Shooter Deaths', align='center')
rects4 = ax.bar(x + width*2, friendly_death, width, label='Friendly Deaths', align='center')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('CCW, SRO, Shooter Deaths (Percentage %)')
ax.set_xlabel('SRO Response Time (seconds)')
ax.set_title('CCW, SRO, and Shooter Death Percentages / Total Iterations / SRO Delay')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(text="{0:2.2%}".format(height/100),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)

fig.tight_layout()

plt.show()




#### Overall Macro Bar Graph for All Scenarios No FF




### aggregation bar
#30/10
df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


fh_cas_0c0s = df_hide30['ui rhf casualty'].mean()
fh_cas_0c0s_std = df_hide30['ui rhf casualty'].std()

df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


fh_cas_1c0s = df_hide30['ui rhf casualty'].mean()
fh_cas_1c0s_std = df_hide30['ui rhf casualty'].std()

df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 1"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


fh_cas_1c1s = df_hide30['ui rhf casualty'].mean()
fh_cas_1c1s_std = df_hide30['ui rhf casualty'].std()

df_hide30 = df.query("`fight range` == 10 & `hide range` == 30 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


fh_cas_0c1s = df_hide30['ui rhf casualty'].mean()
fh_cas_0c1s_std = df_hide30['ui rhf casualty'].std()

#all hide
df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


h_cas_0c0s = df_hide100['ui rhf casualty'].mean()
h_cas_0c0s_std = df_hide100['ui rhf casualty'].std()

df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


h_cas_1c0s = df_hide100['ui rhf casualty'].mean()
h_cas_1c0s_std = df_hide100['ui rhf casualty'].std()

df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 1"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


h_cas_1c1s = df_hide100['ui rhf casualty'].mean()
h_cas_1c1s_std = df_hide100['ui rhf casualty'].std()

df_hide100 = df.query("`fight range` == 0 & `hide range` >= 90 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


h_cas_0c1s = df_hide100['ui rhf casualty'].mean()
h_cas_0c1s_std = df_hide100['ui rhf casualty'].std()


#all run
df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 0"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


r_cas_0c0s = df_run100['ui rhf casualty'].mean()
r_cas_0c0s_std = df_run100['ui rhf casualty'].std()

df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 0"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


r_cas_1c0s = df_run100['ui rhf casualty'].mean()
r_cas_1c0s_std = df_run100['ui rhf casualty'].std()

df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 1"
                     "& `ccw number` == 1 & `friendly fire percent` == 0").sort_values('sro delay')


r_cas_1c1s = df_run100['ui rhf casualty'].mean()
r_cas_1c1s_std = df_run100['ui rhf casualty'].std()

df_run100 = df.query("`fight range` == 0 & `hide range` == 0 & `sro number` == 1"
                     "& `ccw number` == 0 & `friendly fire percent` == 0").sort_values('sro delay')


r_cas_0c1s = df_run100['ui rhf casualty'].mean()
r_cas_0c1s_std = df_run100['ui rhf casualty'].std()


labels = ['No CCW | No SRO', 'CCW | No SRO', 'No CCW | SRO', 'CCW | SRO' ]


x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
hide30 = [fh_cas_0c0s, fh_cas_1c0s,fh_cas_0c1s,fh_cas_1c1s ]
allhide = [h_cas_0c0s, h_cas_1c0s,h_cas_0c1s,h_cas_1c1s ]
allrun = [r_cas_0c0s, r_cas_1c0s,r_cas_0c1s,r_cas_1c1s ]



rects1 = ax.bar(x ,  hide30, width, label='30Hide-10Fight Cas', align='center')
rects2 = ax.bar(x - width , allhide, width, label='All Hide Cas', align='center')
rects3 = ax.bar(x + width, allrun, width, label='All Run Cas', align='center')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Amount of Casualties (1 per count)')
ax.set_xlabel('Variations')
ax.set_title('Casualty Comparison by Scenario and Variation')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(title='Scenarios')



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(text="{0:2.2f}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)


fig.tight_layout()

plt.show()
