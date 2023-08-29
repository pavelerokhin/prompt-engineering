import json
import os
import random
import time

from csv_search import openai, davinci1, davinci05, davinci01


# prepare prompt, we inject a list of metadata into the prompt as context
# we inject headers of the corresponding csv files (with same name)
# we inject the first line of the corresponding csv files (with same name)


def get_file_header(file):
    with open(file, 'r') as f:
        return f.readline()


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


def prepare_prompt_context(file_names: list):
    data = ""

    for i, file_name in enumerate(file_names):
        file_name_csv = './output/' + file_name + '.csv'
        file_name_json = './output/' + file_name + '.json'

        # read json and make it a map
        with open(file_name_json, 'r') as f:
            j = json.loads(f.read())

        topics = j.get("metadata").get("Temi del dataset")
        geo = j.get("metadata").get("Copertura geografica")
        auth = j.get("metadata").get("Titolare")
        metadata = f"Tematiche: {topics}\nCopertura geografica: {geo}\nTitolare: {auth}"

        # read csv headers
        csv_header = get_file_header(file_name_csv)

        data += data_prompt.format(i=i, metadata=metadata, csv_header=csv_header)

    return base.format(data=data)


GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[0m'

if __name__ == '__main__':
    N = 30
    n = 3

    # number of files in dir ./output
    all_files = os.listdir('./output')
    # delete all extensions and duplicates
    all_files = list(set([file.split('.')[0] for file in all_files]))
    random.shuffle(all_files)
    file_names = all_files[:N]
    if "4701_20230508_eg_concorsi" not in file_names:
        file_names.remove(file_names[0])
        file_names = file_names + ["4701_20230508_eg_concorsi"]
        random.shuffle(file_names)

    correct_response = file_names.index("4701_20230508_eg_concorsi")

    part_of_files = []
    prompts = []
    for i, file in enumerate(file_names):
        if i and i % n == 0:
            prompt = prepare_prompt_context(part_of_files)
            prompts.append(prompt)
            part_of_files = []

        full_name = file.split('.')
        name = full_name[0]
        if name not in part_of_files:
            part_of_files.append(name)

    prompt = prepare_prompt_context(part_of_files)
    prompts.append(prompt)

    answers = []
    i = 0
    while i < len(prompts):
        print("*" * 10, "from", i * n, "to", (i + 1) * n - 1, "*" * 10)
        print("Risposta corretta: ", correct_response)
        print(file_names[i * n:(i + 1) * n])

        question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"
        answerOpenAI = "*"
        while not (answerOpenAI.isnumeric() or answerOpenAI == "-1"):
            answerOpenAI = openai(prompt + question)
            answerOpenAI = answerOpenAI.replace("\n", "").replace("\t", "").replace(" ", "")
            if answerOpenAI.isnumeric():
                x = int(answerOpenAI) + i * n
                print("openai")
                if x == correct_response:
                    print(f"{GREEN}{part_of_files[x]}{WHITE}")
                else:
                    print(f"{RED}{part_of_files[x]}{WHITE}")

        answerDaVinci1 = "*"
        while not (answerDaVinci1.isnumeric() or answerDaVinci1 == "-1"):
            answerDaVinci1 = davinci1(prompt + question)
            answerDaVinci1 = answerDaVinci1.replace("\n", "").replace("\t", "").replace(" ", "")
            if answerDaVinci1.isnumeric():
                x = int(answerDaVinci1) + i * n
                print("openai")
                if x == correct_response:
                    print(f"{GREEN}{part_of_files[x]}{WHITE}")
                else:
                    print(f"{RED}{part_of_files[x]}{WHITE}")

        answerDaVinci05 = "*"
        while not (answerDaVinci05.isnumeric() or answerDaVinci05 == "-1"):
            answerDaVinci05 = davinci05(prompt + question)
            answerDaVinci05 = answerDaVinci05.replace("\n", "").replace("\t", "").replace(" ", "")
            if answerDaVinci05.isnumeric():
                x = int(answerDaVinci05) + i * n
                print("openai")
                if x == correct_response:
                    print(f"{GREEN}{part_of_files[x]}{WHITE}")
                else:
                    print(f"{RED}{part_of_files[x]}{WHITE}")

        answerDaVinci01 = "*"
        while not (answerDaVinci01.isnumeric() or answerDaVinci01 == "-1"):
            answerDaVinci01 = davinci01(prompt + question)
            answerDaVinci01 = answerDaVinci01.replace("\n", "").replace("\t", "").replace(" ", "")
            if answerDaVinci01.isnumeric():
                x = int(answerDaVinci01) + i * n
                print("openai")
                if x == correct_response:
                    print(f"{GREEN}{part_of_files[x]}{WHITE}")
                else:
                    print(f"{RED}{part_of_files[x]}{WHITE}")

        answers.append([answerOpenAI, answerDaVinci1, answerDaVinci05, answerDaVinci01, str(correct_response)])
        i += 1

    # save answers in csv file, format time in human-readable format
    with open(f"{time.time()}_answers.csv", 'w') as f:
        for answer in answers:
            f.write(','.join(answer) + '\n')
