import json
import langchain

# prepare prompt, we inject a list of metadata into the prompt as context
# we inject headers of the corresponding csv files (with same name)
# we inject the first line of the corresponding csv files (with same name)


def get_file_header(file):
    with open(file, 'r') as f:
        return f.readline()


base = """Questi sono le informazioni che abbiamo sul dataset:
{data}
Fine dataset.
Puoi rispondere con il numero del dataset o con il nome del dataset.
Quale dataset potrebbe rispondere a questa domanda:
"""

data_prompt = """
Informazione {i}
Le metadata del CSV sono:
{metadata}
Il HEADER del CSV è:
{csv_header}
***

"""


def prepare_prompt_context(file_names: list):
    data = ""

    for i, file_name in enumerate(file_names):
        file_name_csv = './output/' + file_name + '.csv'
        file_name_json = './output/' + file_name + '.json'

        # read json and make it a map
        with open(file_name_json, 'r') as f:
            j = json.loads(f.read())

        topics = j.get("Temi del dataset")
        geo = j.get("Copertura geografica")
        auth = j.get("Titolare")
        metadata = f"Tematiche: {topics}\nCopertura geografica: {geo}\nTitolare: {auth}"

        # read csv headers
        csv_header = get_file_header(file_name_csv)

        data += data_prompt.format(i=i, metadata=metadata, csv_header=csv_header)

    return base.format(data=data)

