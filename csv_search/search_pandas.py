import pandas
import pandas as pd
from pandasai import SmartDataframe

from csv_search import openai, davinci1, davinci05, davinci0
from utils import *

# # You can instantiate a SmartDataframe with a path to a CSV file
# df = SmartDataframe("4701_20230508_eg_concorsi.csv")
# df.llm = openai
#
# response = df.chat("Ci sono i concorsi per operaio mautentore di macchine operatrici complesse?")
# print(response)

# FASE 1

if __name__ == '__main__':
    N = 4

    file_names = get_file_names(N)
    correct_response = file_names.index("4701_20230508_eg_concorsi")

    metadata = []
    additional_info = []
    for file_name in file_names:
        m = get_metadata(file_name)
        metadata.append(pandas.DataFrame(m["metadata"], index=[file_name]))
        additional_info.append(m["additional_info"])

    # Merge dataframes by index
    df = pd.concat(metadata, axis=0)

    sdf = SmartDataframe(df)
    sdf.llm = openai
    response = sdf.chat("Quale file probabilmente risponderà alla domanda: Ci sono ancora i concorsi per operaio mautentore di macchine operatrici complesse?")

    print(response)
