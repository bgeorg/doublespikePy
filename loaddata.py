
"""Load data from csv file,
and perform some operations to bring dataframe into shape.
Dataframe is used to feed elemental info to elemental objects later on.
@author: bastian

"""



import pandas as pd
import numpy as np

def read_data():
    
    header_cols = ['element', 'isotope', 'mass', 'standard', 
                   'spike1', 'spike2', 'spike3', 'spike4', 
                   'spike5', 'spike6', 'spike7', 'spike8',
                   'spike9', 'spike10']
    
    df = pd.read_csv('maininput.csv', index_col=None, header=0, names=header_cols, sep=',').replace('"','', regex=True)
    df['element'].fillna(value='tbf', inplace=True)
    
    labels = []
    length = len(df)
    
    for i in range(length):
        if df.iloc[i]['element'] != 'tbf':
            label = df.iloc[i]['element']
            labels.append(label)
        else:
            labels.append(label)
            
    df.drop(columns='element', axis=1, inplace=True)
    df.insert(0, 'element', labels)
    
    
    return df


def load_isodata_per_element(data, element):
    
    el_data = data[data['element'] == element]
    el_data = el_data.copy()
    el_data.dropna(axis='columns', inplace=True)
    
    #get isotope data 
    isotope = el_data['isotope'].values
    mass = el_data['mass'].values
    standard = np.transpose((el_data['standard'].values))
    spikes = np.transpose((el_data.iloc[: , 4 :]).values)
    
    
    return (element, isotope, mass, standard, spikes)








