import json
import time

from csv_search import openai, davinci1, davinci05, davinci01
from utils import get_file_names, get_csv_header, get_metadata


annotation_prompt = """
Describe the dataset, given the following metadata and CSV header:
Metadata: {metadata}
CSV header: {csv_header}
"""

N = 40


def annotate(file_names):
    annotations = {}
    for file_name in file_names:
        print(file_name)
        header = get_csv_header(file_name)
        metadata = get_metadata(file_name)
        prompt = annotation_prompt.format(metadata=metadata, csv_header=header)

        annotation = openai(prompt)
        annotations[file_name] = annotation

    return annotations


def save_annotations(annotations):
    with open(f"{time.time()}_annotations_{N}_files.json", 'w') as f:
        json.dump(annotations, f)


p = """
Questi sono le informazioni che abbiamo sul dataset:
The dataset provides information on administration and remuneration of personnel in the municipality of Zenson di Piave. The dataset includes the following metadata:\n\n- Tematiche: Popolazione e società (Themes: Population and society)\n- Copertura geografica (Geographical coverage): No specific information is provided about the coverage. \n- Titolare (Holder): Name: Comune di Zenson di Piave (Municipality of Zenson di Piave)\n- Codice IPA/IVA (IPA/IVA code): c_m163\n\nThe CSV header contains three columns:\n\n1. ANNO (Year): Indicates the year of the data for administration and remuneration of personnel.\n2. VOCE_ACCESSORIA (Accessory item): Refers to the specific items or categories related to compensation.\n3. TOTALE_COMPENSI (Total compensation): Represents the total amount of compensation for the respective accessory item and year.\n\nThe dataset seems to provide detailed information on the administration and remuneration of personnel in the municipality of Zenson di Piave, including specific categories and their corresponding compensation amounts over multiple years. However, further details or context may be required to understand the complete scope and nature of the dataset.

Devi rispondere sì, no o non lo so.
Ci sono ancora dei concorsi aperti per operaio mautentore di macchine operatrici complesse?"""

if __name__ == "__main__":
    # file_names = get_file_names(N)
    #
    # annotations = annotate(file_names)
    # save_annotations(annotations)
    print(openai(p), "\n\n\n")
    print(davinci1(p), "\n\n\n")
    print(davinci05(p), "\n\n\n")
    print(davinci01(p))
