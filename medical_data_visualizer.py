import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['overweight'] = df['weight'] / ((df['height'] / 100) ** 2) > 25
df['overweight'] = df['overweight'].apply(lambda x : 1 if x == True else 0)

# 3 Normalize
for col in ('gluc', 'cholesterol'):
    df[col] = df[col].apply(lambda x : 0 if x == 1 else 1)

# 4
def draw_cat_plot():
    # 5
    values = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    values.sort()
    
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=values)

    # 6
    totals_0 = []
    totals_1 = []

    for var in values:
        var_totals_0 = df_cat[(df_cat['variable'] == var) & (df_cat['cardio'] == 0)]['value'].value_counts().values
        var_totals_1 = df_cat[(df_cat['variable'] ==  var) & (df_cat['cardio'] == 1)]['value'].value_counts().values
        totals_0 = np.concatenate((totals_0, var_totals_0))
        totals_1 = np.concatenate((totals_1, var_totals_1))

    totals = np.concatenate((totals_0, totals_1))
    
    df_cat = df_cat.drop_duplicates().sort_values(by=['cardio', 'variable'])
    df_cat['total'] = totals
    
    # 7 TODO convert to long

    # 8
    fig, ax = plt.subplots(figsize=(8,8))
    fig = sns.catplot(data=df_cat, x='variable', y='total', hue='value', col='cardio', kind='bar')

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[df['ap_lo'] <= df['ap_hi']]

    for col in ('height', 'weight'):
        df_heat = df_heat[df_heat[col] >= df_heat[col].quantile(0.025)]
        df_heat = df_heat[df_heat[col] <= df_heat[col].quantile(0.975)]

    # 12
    corr = df_heat.corr()

    # 13
    size = corr.index.size
    m = np.ones((size,size), dtype=bool)
    for i in range(size):
        m[i][:i] = False
    mask = m

    # 14
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_title("Correlation")

    # 15
    ax = sns.heatmap(corr, mask=mask, annot=True, linewidth=.5, center=0.0, vmax=0.3, square=True, fmt='.1f')

    # 16
    fig.savefig('heatmap.png')
    return fig
