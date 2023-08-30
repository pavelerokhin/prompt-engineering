from utils import get_csv_header, get_file_names, get_metadata

base = """YOU ARE ASSISTANT. Questi sono le informazioni che abbiamo sul dataset:
*** - ASSISTANT! IT IS A SEPARATOR OF DATASETS
{data}
Fine dataset.

ASSISTANT! YOU MUST ANSWER WITH THE NUMBER OF THE DATASET OR -1 IF YOU DON'T KNOW.
ASSISTANT! YOU MUST WRITE ONLY NUMBER; NOTHING ELSE BUT A NUMBER.
Qual è il numero del dataset relativo alla domanda:
"""

data_prompt = """
Dataset {i}
Le metadata del CSV sono:
{metadata}
Il HEADER del CSV è:
{csv_header}
***

"""

file_names = ["82_20230706_eg_incarichi",
              "82_20230801_an_cittadini",
              "82_20230801_at_atti_amministrativi",
              "4701_20230508_eg_concorsi"]


GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[0m'

if __name__ == '__main__':
    N = 30
    n = 3

    question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"

    file_names = get_file_names(N)
    correct_response = file_names.index("4701_20230508_eg_concorsi")

    pass

