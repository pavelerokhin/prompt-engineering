import time

from csv_search import openai, davinci1, davinci05, davinci0
from utils import *

# prepare prompt, we inject a list of metadata into the prompt as context
# we inject headers of the corresponding csv files (with same name)
# we inject the first line of the corresponding csv files (with same name)

base = """Rispondi solo con i numeri. Questi sono le informazioni che abbiamo sul dataset:
{data}
***
Fine dataset.

Devi rispondere con il numero del dataset.
Qual è il numero del dataset più relativo alla domanda:
"""

base1 = """Here are the information we have about the datasets:
{data}
*** separator
End of datasets.


What is the dataset number related and helps with the following question (Italian)?
You must answer with the most relevant dataset number.
Question:
"""

data_prompt = """
Dataset {i}
Metadata:
{metadata}
Tags:
{csv_header}
*** separator
"""


def prepare_prompt_context(file_names: list):
    data = ""
    for i, file_name in enumerate(file_names):
        csv_header = get_csv_header(file_name)
        metadata = get_metadata_str(file_name)

        data += data_prompt.format(i=i, metadata=metadata, csv_header=csv_header)

    return base.format(data=data)


if __name__ == '__main__':
    N = 40
    n = 4
    question = "Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"

    file_names = get_file_names(N)
    correct_response = file_names.index("4701_20230508_eg_concorsi")
    print("Risposta corretta: ", correct_response)

    answers = []
    i = 0
    lower = 0
    while True:
        lower = i * n
        if lower >= len(file_names):
            break
        upper = lower + n

        # take i-est n files and prepare prompt
        fns = file_names[lower:upper]
        prompt = prepare_prompt_context(fns)

        answerOpenAI = get_answer(openai, prompt, question)
        estimate_batch_answer(answerOpenAI, correct_response, lower, upper)
        # answerDaVinci05 = get_answer(davinci05, prompt, question)
        # estimate_batch_answer(answerDaVinci05, correct_response, lower, upper)

        i += 1

        # answerDaVinci1 = "*"
        # while not (answerDaVinci1.isnumeric() or answerDaVinci1 == "-1"):
        #     answerDaVinci1 = davinci1(prompt + question)
        #     answerDaVinci1 = answerDaVinci1.replace("\n", "").replace("\t", "").replace(" ", "")
        #     if answerDaVinci1.isnumeric():
        #         x = int(answerDaVinci1) + i * n
        #         print("openai")
        #         if x == correct_response:
        #             print(f"{GREEN}{file_names[x]}{WHITE}")
        #         else:
        #             print(f"{RED}{file_names[x]}{WHITE}")
        #
        # answerDaVinci05 = "*"
        # while not (answerDaVinci05.isnumeric() or answerDaVinci05 == "-1"):
        #     answerDaVinci05 = davinci05(prompt + question)
        #     answerDaVinci05 = answerDaVinci05.replace("\n", "").replace("\t", "").replace(" ", "")
        #     if answerDaVinci05.isnumeric():
        #         x = int(answerDaVinci05) + i * n
        #         print("openai")
        #         if x == correct_response:
        #             print(f"{GREEN}{file_names[x]}{WHITE}")
        #         else:
        #             print(f"{RED}{file_names[x]}{WHITE}")
        #
        # answerDaVinci01 = "*"
        # while not (answerDaVinci01.isnumeric() or answerDaVinci01 == "-1"):
        #     answerDaVinci01 = davinci0(prompt + question)
        #     answerDaVinci01 = answerDaVinci01.replace("\n", "").replace("\t", "").replace(" ", "")
        #     if answerDaVinci01.isnumeric():
        #         x = int(answerDaVinci01) + i * n
        #         print("openai")
        #         if x == correct_response:
        #             print(f"{GREEN}{file_names[x]}{WHITE}")
        #         else:
        #             print(f"{RED}{file_names[x]}{WHITE}")
        #
        # answers.append([answerOpenAI, answerDaVinci1, answerDaVinci05, answerDaVinci01, str(correct_response)])

    # # save answers in csv file, format time in human-readable format
    # with open(f"{time.time()}_answers.csv", 'w') as f:
    #     for answer in answers:
    #         f.write(','.join(answer) + '\n')
