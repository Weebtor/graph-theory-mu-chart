from os import read
import numpy as np

import pandas as pd
from pandas.io.parsers.readers import validate_integer


def csv_to_numpy_matrix_list(file_path):
    mu_chart = pd.read_csv(file_path)
    char_list = list(mu_chart.columns[1:])
    matrix_list = []

    # print(char_list)
    for i in range(0,len(char_list)):
        char_name = char_list[i]
        
        index_char = mu_chart.columns.get_loc(char_name)
        mu_list = []
        for col in mu_chart.columns[1:]:
            value = mu_chart[col][index_char-1]
            if value != "-" and float(value) > 5:
                mu_list.append(float(value))
            else:
                mu_list.append(0.0)
        # print(index_char, char_name)
        matrix_list.append(mu_list) 
    #     print(char_name, mu_list)
    # print(len(char_list))

    return matrix_list
    # for col in mu_chart.columns[1:]:
        
