from csv_search import openai, davinci1, davinci05, davinci01
from search import prepare_prompt
from utils import get_file_names

# prepare prompt, we inject a list of metadata into the prompt as context
# we inject headers of the corresponding csv files (with same name)
# we inject the first line of the corresponding csv files (with same name)
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

N = 40
n = 4


if __name__ == '__main__':
    file_names = get_file_names(N)

    # prepare prompt
    prompt = prepare_prompt(file_names)
    correct_response = file_names.index("4701_20230508_eg_concorsi")

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
