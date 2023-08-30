import pandas as pd
from pandasai import SmartDataframe

from csv_search import openai, davinci1, davinci05, davinci01
from utils import *

# You can instantiate a SmartDataframe with a path to a CSV file
# df = SmartDataframe("4701_20230508_eg_concorsi.csv")
# df.llm = openai

# response = df.chat("Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?")
# print(response)


if __name__ == '__main__':
    N = 40

    file_names = get_file_names(N)
    metadata = []
    additional_info = []
    for file_name in file_names:
        m = pd.read_json("./output/"+file_name+".json")
        mm = pd.DataFrame(m["metadata"])
        mm.name = file_name
        aa = pd.DataFrame(m["additional_info"])
        aa.name = file_name
        metadata.append(mm)
        additional_info.append(aa)

    # Merge dataframes by index
    df = pd.concat(metadata, axis=0)

    sdf = SmartDataframe(df)
    sdf.llm = openai
    response = sdf.chat("Quale dataset potrebbe rispondere alla domanda: Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?")

    print(response)
