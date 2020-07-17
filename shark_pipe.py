# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 02:15:44 2020

@author: lukas
"""

# Problem Definition:
## Deduce TOP-10 Manufacturers by Fuel Efficiency for given year
import pandas as pd


# take CSV file from folder
def acquisition():
    df = pd.read_csv('GSAF5.csv', encoding= 'cp1252')
    return df

# clean the columns and reomve inconsistancy
def wrangle(df):
    cols = ['Year','Type','Area','Location' , 'Activity','Species ', 'Fatal (Y/N)']
    df_EC = df[cols].loc[(df['Country'] == 'AUSTRALIA')  & ((df['Area'] == 'New South Wales')|(df['Area'] == 'Queensland')) & (df['Year'] > 1989)]
    df_EC_noNA = df_EC.dropna(subset=['Species ','Fatal (Y/N)'])
    df_EC_s = df_EC_noNA.loc[(df_EC_noNA['Fatal (Y/N)'] == 'N') | (df_EC_noNA['Fatal (Y/N)'] == 'Y')].rename(columns={"Species ": "Species", "Fatal (Y/N)": "Fatal"})
    filtered = df_EC_s
    return filtered

# perform basic analytics
def analyze(df):
    compare = df.groupby(['Area','Fatal']).count().Year
    final=compare.reset_index()
    return final

# perform basic visualisation
def viz(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    fig,ax=plt.subplots(figsize=(15,8))
    barchart=sns.barplot(data=df, x='Area',y='Count', hue='Fatal')
    plt.title("Comparison between the Queensland and New South Wales policy on mitigation")
    return barchart

# save vizualisation
def save_viz(plot):
    fig=plot.get_figure()
    fig.savefig("Comparison QLD and NSW.png")
    
#initialise file
if __name__=='__main__':
    data=acquisition()
    filtered=wrangle(data)
    results=analyze(filtered)
    barchart=viz(results)
    save_viz(barchart)
