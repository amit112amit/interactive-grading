import base64
import numpy as np
import pandas as pd


def prepare_histogram_data_source(excelfilecontents, maxmarks=100):
    """
    Collect histogram details in a dictionary.
    """
    excelfile = base64.b64decode(excelfilecontents)
    df = pd.read_excel(excelfile, engine='openpyxl')
    marks = np.round(df['Total'].to_numpy(), 0)
    hist, bin_edges = np.histogram(marks, np.arange(-0.5, maxmarks + 1.5, 1))
    hist_data = {'top': hist, 'left': bin_edges[:-1], 'right': bin_edges[1:],
                 'bin_value': bin_edges[:-1] + 0.5}
    return hist_data


def get_marks_stats(excelfilecontents):
    """
    Return the total number of students, the average marks and unique marks.
    """
    excelfile = base64.b64decode(excelfilecontents)
    df = pd.read_excel(excelfile, engine='openpyxl')
    return df.shape[0], df.Total.mean()
