import json
import os
import random

from csv_search import openai, davinci1, davinci05, davinci01
from search import prepare_prompt_context

# prepare prompt, we inject a list of metadata into the prompt as context
# we inject headers of the corresponding csv files (with same name)
# we inject the first line of the corresponding csv files (with same name)


def get_file_header(file):
    with open(file, 'r') as f:
        return f.readline()


base = """Questi sono le informazioni che abbiamo sul dataset:
{data}
***
Fine dataset.

Devi rispondere con il numero del dataset o -1 se non lo sai.
Qual è numero di dataset relativo alla domanda:
"""

data_prompt = """
Dataset {i}
Le metadata sono:
{metadata}
Le categorie sono:
{csv_header}
"""

N = 4

file_names = os.listdir('./output')
file_names = list(set([file.split('.')[0] for file in file_names]))
random.shuffle(file_names)
file_names = file_names[:N]
if "4701_20230508_eg_concorsi" not in file_names:
    file_names.remove(file_names[0])
    file_names = file_names + ["4701_20230508_eg_concorsi"]
    random.shuffle(file_names)


if __name__ == '__main__':
    correct_response = file_names.index("4701_20230508_eg_concorsi")
    # prepare prompt
    prompt = prepare_prompt_context(file_names)

    # ask question
    question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"

    print("*" * 100)
    # get answer on openai
    print("Risposta corretta: ", correct_response)
    print("openai")
    answer = openai(prompt + question)
    print(answer)

    # get answer on davinci1
    print("Risposta corretta: ", correct_response)
    print("davinci1")
    answer = davinci1(prompt + question)
    print(answer)

    # get answer on davinci05
    print("Risposta corretta: ", correct_response)
    print("davinci05")
    answer = davinci05(prompt + question)
    print(answer)

    # get answer on davinci01
    print("Risposta corretta: ", correct_response)
    print("davinci01")
    answer = davinci01(prompt + question)
    print(answer)
