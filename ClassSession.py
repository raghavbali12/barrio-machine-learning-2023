import pandas as pd

class ClassSessionWrapper:
  def __init__(self, df):
        self.df = df

  def get_columns(self):
      return self.df.columns.tolist()

  def get_row(self, index):
      return self.df.iloc[index]

  def get_shape(self):
      return self.df.shape