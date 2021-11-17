import pandas as pd
import os

class DataManager():

    def __init__(self, file_path: str) -> None:
        self.mu_chart = pd.read_csv(file_path)
        
    def get_vertex_list(self) -> list:

        return list(self.mu_chart.columns[1:])

    def get_character_winning_mu(self, char_name: str):
        index_char: int = self.mu_chart.columns.get_loc(char_name)

        mu_dict = {}

        
        for col in self.mu_chart.columns[1:]:
            value = self.mu_chart[col][index_char-1] 
            if value != "-" and float(value) > 5:
                # value_float = float(value.replace(",","."))
                mu_dict[col] = float(value)
            

        return mu_dict
