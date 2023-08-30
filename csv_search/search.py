from csv_search import openai, davinci1, davinci05, davinci01
from utils import get_csv_header, get_file_names, get_metadata

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

file_names = ["82_20230706_eg_incarichi",
              "82_20230801_an_cittadini",
              "82_20230801_at_atti_amministrativi",
              "4701_20230508_eg_concorsi"]


def prepare_prompt(file_names: list):
    data = ""
    for i, file_name in enumerate(file_names):
        csv_header = get_csv_header(file_name)
        metadata = get_metadata(file_name)

        data += data_prompt.format(i=i, metadata=metadata, csv_header=csv_header)

    return base.format(data=data)


if __name__ == '__main__':
    N = 40

    file_names = get_file_names(N)

    question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"

    prompt = prepare_prompt(file_names)
    correct_response = file_names.index("4701_20230508_eg_concorsi")

    print(question)

    print("Risposta corretta: ", correct_response)
    print("*" * 100)
    # get answer on openai
    print("openai")
    answer = openai(prompt + question)
    print(answer)

    # get answer on davinci1
    print("davinci1")
    answer = davinci1(prompt + question)
    print(answer)

    # get answer on davinci05
    print("davinci05")
    answer = davinci05(prompt + question)
    print(answer)

    # get answer on davinci01
    print("davinci01")
    answer = davinci01(prompt + question)
    print(answer)
