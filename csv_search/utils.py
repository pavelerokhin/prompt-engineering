import json
import os
import random
import re

GREEN = '\033[92m'
GREY = '\033[90m'
LIGHT_BLUE = '\033[94m'
RED = '\033[91m'
WHITE = '\033[0m'

file_names_default = ["82_20230706_eg_incarichi",
                      "82_20230801_an_cittadini",
                      "82_20230801_at_atti_amministrativi",
                      "4701_20230508_eg_concorsi"]


def estimate_batch_answer(answer, correct_response, lower, upper):
    print(f"{lower} - {upper}", end=" ")
    if answer == "-1":
        if lower <= correct_response <= upper:
            print(f"{RED}false negative{WHITE}")
            return
        else:
            print(f"{GREEN}true negative{WHITE}")
            return

    response = lower + int(answer)
    print(f"{LIGHT_BLUE}{response}, {correct_response}{WHITE}")
    if response == correct_response:
        print(f"{GREEN}true positive{WHITE}")
        return
    print(f"{RED}false positive{WHITE}")


def estimate_one_answer(answer, correct_response):
    if answer.isnumeric():
        x = int(answer)
        if x == correct_response:
            if x:
                print(f"{GREEN}true positive{WHITE}")
            else:
                print(f"{RED}false negative{WHITE}")
        if x != correct_response:
            if x:
                print(f"{RED}false positive{WHITE}")
            else:
                print(f"{GREEN}true negative{WHITE}")
        return True
    return False


def get_answer(llm, prompt, question):
    answer = ""
    while not (answer.isnumeric() or answer == "-1"):
        print(llm.model_name)
        answer = llm(prompt + question)
        answer = answer.replace("\n", "").replace("\t", "").replace(" ", "")

        if len(answer) > 3:
            print(f"{GREY}{answer}{WHITE}")
            # if there is -1 somewhere in the answer, answer = -1
            answer = parse_long_answer(answer)
    return answer


def parse_long_answer(answer):
    answer = answer.replace("\n", "").replace("\t", "").replace(" ", "").lower()

    # find the first number in answer text
    r = re.compile("(\\d+)")
    m = r.search(answer)
    if m:
        return m.group(1)

    if "non" in answer or "nessun" in answer:
        return "-1"

    return answer


def get_csv_header(file_name):
    file = './output/' + file_name + '.csv'
    with open(file, 'r') as f:
        return f.readline()


def get_file_names(N):
    all_files = os.listdir('./output')
    # delete all extensions and duplicates
    all_files = list(set([file.split('.')[0] for file in all_files]))
    random.shuffle(all_files)

    file_names = all_files[:N]
    if "4701_20230508_eg_concorsi" not in file_names:
        file_names.remove(file_names[0])
        file_names = file_names + ["4701_20230508_eg_concorsi"]
        random.shuffle(file_names)

    return file_names


def get_metadata(file_name):
    file = './output/' + file_name + '.json'
    with open(file, 'r') as f:
        j = json.loads(f.read())
    topics = j.get("metadata").get("Temi del dataset")
    geo = j.get("metadata").get("Copertura geografica")
    auth = j.get("metadata").get("Titolare")
    return f"Tematiche: {topics}\nCopertura geografica: {geo}\nTitolare: {auth}"
