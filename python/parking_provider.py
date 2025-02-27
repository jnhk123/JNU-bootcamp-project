import pandas as pd

class Parking() :
    def __init__(self):
        df = pd.read_csv('./processedParking.csv', encoding='cp949')
        _non_coord = df[df[['x', 'y']].isnull().all(axis=1)].reset_index(drop=True)
        _has_coord = df[df[['x', 'y']].notnull().all(axis=1)].reset_index(drop=True)

        self.origin = df
        self.has_coord = _has_coord
        self.non_coord = _non_coord







