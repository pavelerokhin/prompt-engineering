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

simple_phrases_prompt = """
Riformula la sequente domanda in frsi chiare e semplici:
{question}
"""

base = """
YOU ARE ASSISTANT. Questi sono le informazioni che abbiamo sul dataset:
{data}
Fine dataset.

ASSISTANT! YOU MUST ANSWER WITH 1 IF TRUE OR 0 IF FALSE OR IF YOU DON'T KNOW.
ASSISTANT! YOU MUST WRITE ONLY NUMBER; NOTHING ELSE BUT A NUMBER.

IL dataset è relativo alla domanda:
"""

base_tot = """
YOU ARE ASSISTANT. Questi sono le informazioni che abbiamo sul dataset:
{data}
Fine dataset.

ASSISTANT! 
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking,
then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.
You must answer with 1 if true or 0 if false or if you don't know.
You must write only number; nothing else but a number.
The question is: 
IL dataset è relativo alla domanda? 
"""

""""""

data_prompt = """
Le metadata del CSV sono:
{metadata}
Il HEADER del CSV è:
{csv_header}
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

    return base_tot.format(data=data)


def estimate_answer(answer):
    if answer.isnumeric():
        x = int(answer)
        if i == correct_response:
            if x:
                print(f"{GREEN}true positive{WHITE}")
            else:
                print(f"{RED}false negative{WHITE}")
        if i != correct_response:
            if x:
                print(f"{RED}false positive{WHITE}")
            else:
                print(f"{GREEN}true negative{WHITE}")
        return True
    return False


GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[0m'

if __name__ == '__main__':
    N = 10
    n = 1

    question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"
    # while True:
    #     question_ = openai(simple_phrases_prompt.format(question=question))
    #     if question_ == "":
    #         continue
    #     print("is the following correct question:", question_)
    #     # if press enter, then the question is correct, interrupt the loop
    #     if input() == "":
    #         break
    question_ = question


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
        prompt = prepare_prompt_context([file])
        prompts.append(prompt)

    answers = []
    i = 0
    print("Risposta corretta: ", correct_response)

    while i < len(prompts):
        print("*" * 10, i, "*" * 10)
        prompt_ = prompts[i]
        answerOpenAI = "*"
        while not (answerOpenAI.isnumeric()):
            print("openai")
            answerOpenAI = openai(prompt_ + question_)
            answerOpenAI = answerOpenAI.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_answer(answerOpenAI)

        answerDaVinci1 = "*"
        while not (answerDaVinci1.isnumeric() or answerDaVinci1 == "-1"):
            print("DaVinci1")
            answerDaVinci1 = davinci1(prompt_ + question_)
            answerDaVinci1 = answerDaVinci1.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_answer(answerDaVinci1)

        answerDaVinci05 = "*"
        while not (answerDaVinci05.isnumeric()):
            print("DaVinci05")
            answerDaVinci05 = davinci05(prompt_ + question_)
            answerDaVinci05 = answerDaVinci05.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_answer(answerDaVinci05)

        answerDaVinci01 = "*"
        while not (answerDaVinci01.isnumeric()):
            print("DaVinci01")
            answerDaVinci01 = davinci01(prompt_ + question_)
            answerDaVinci01 = answerDaVinci01.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_answer(answerDaVinci01)

        answers.append([file_names[i], answerOpenAI, answerDaVinci1, answerDaVinci05, answerDaVinci01, '*' if i == correct_response else ''])
        i += 1


    # save answers in csv file, format time in human-readable format
    with open(f"{time.time()}_answers_tree.csv", 'w') as f:
        for answer in answers:
            f.write(','.join(answer) + '\n')