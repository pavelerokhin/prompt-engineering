import time

from csv_search import openai, davinci1, davinci05, davinci01
from utils import *

# prepare prompt, we inject a list of metadata into the prompt as context
# we inject headers of the corresponding csv files (with same name)
# we inject the first line of the corresponding csv files (with same name)
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


if __name__ == '__main__':
    N = 10
    n = 1

    question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"

    file_names = get_file_names(N)
    prompts = []
    for i, file in enumerate(file_names):
        prompt = prepare_prompt([file])
        prompts.append(prompt)

    correct_response = file_names.index("4701_20230508_eg_concorsi")

    answers = []
    i = 0
    print("Risposta corretta: ", correct_response)

    while i < len(prompts):
        print("*" * 10, i, "*" * 10)
        prompt_ = prompts[i]
        answerOpenAI = "*"
        while not (answerOpenAI.isnumeric()):
            print("openai")
            answerOpenAI = openai(prompt_ + question)
            answerOpenAI = answerOpenAI.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_one_answer(answerOpenAI)

        answerDaVinci1 = "*"
        while not (answerDaVinci1.isnumeric() or answerDaVinci1 == "-1"):
            print("DaVinci1")
            answerDaVinci1 = davinci1(prompt_ + question)
            answerDaVinci1 = answerDaVinci1.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_one_answer(answerDaVinci1)

        answerDaVinci05 = "*"
        while not (answerDaVinci05.isnumeric()):
            print("DaVinci05")
            answerDaVinci05 = davinci05(prompt_ + question)
            answerDaVinci05 = answerDaVinci05.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_one_answer(answerDaVinci05)

        answerDaVinci01 = "*"
        while not (answerDaVinci01.isnumeric()):
            print("DaVinci01")
            answerDaVinci01 = davinci01(prompt_ + question)
            answerDaVinci01 = answerDaVinci01.replace("\n", "").replace("\t", "").replace(" ", "")
            estimate_one_answer(answerDaVinci01)

        answers.append([file_names[i], answerOpenAI, answerDaVinci1, answerDaVinci05, answerDaVinci01, '*' if i == correct_response else ''])
        i += 1


    # save answers in csv file, format time in human-readable format
    with open(f"{time.time()}_answers_tree.csv", 'w') as f:
        for answer in answers:
            f.write(','.join(answer) + '\n')