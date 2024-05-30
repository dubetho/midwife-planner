import pandas as pd
from datetime import datetime


month_mapping = {
     1: 'Janvier',
     2: 'Février',
     3: 'Mars',
     4: 'Avril',
     5: 'Mai',
     6: 'Juin',
     7: 'Juillet',
     8: 'Août',
     9: 'Septembre',
     10: 'Octobre',
     11: 'Novembre',
     12: 'Décembre'
}

list_not_names = ['J', 'JU', 'JU inf', 'JP', 'C1', 'J1', 'JBB', 'C2', 'J2', 'N', 'NU', 'N1', 'N2 infirmière',
                  'N2 sage-femme', 'EF', 'CSG', 'A reprendre ']

def get_month(dataset):
    """ Extract the month from the first column of the dataset"""
    first_row_without_na= dataset.head(1).T.dropna(how='all')
    month_integer = pd.to_datetime(first_row_without_na.iloc[0, 0]).month
    return month_mapping[month_integer]

def get_year(dataset):
    """ Extract the year from the first column of the dataset"""
    first_row_without_na= dataset.head(1).T.dropna(how='all')
    year = pd.to_datetime(first_row_without_na.iloc[0, 0]).year
    return year

def get_midwifes_name(dataset):
    """ Extract the names of the midwifes from the first column of the dataset"""
    # Extract the first column, drop NaN values, get unique values, and convert to a list
    names = dataset.iloc[:, 0].dropna().unique().tolist()
    # Remove unwanted names
    for item in list_not_names:
        if item in names:
            names.remove(item)
    return names



