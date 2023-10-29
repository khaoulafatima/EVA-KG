import os
import PyPDF2
import json
import re


def extract_titles_frequency(path: str):
    title_dict = {}

    for file in os.listdir(path):
        pdf_file = open(path + file, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page in pdf_reader.pages:
            text = page.extract_text()

            # i titoli delle sezioni principali sono in maiuscolo
            for token in text.split('\n'):
                if token.isupper():
                    if token not in title_dict.keys():
                        title_dict[token] = 1
                    else:
                        title_dict[token] += 1

    title_dict = dict(sorted(title_dict.items(), key=lambda item: item[1], reverse=True))

    with open("title_dict.json", "w", encoding="UTF-8") as f:
        json.dump(title_dict, f, ensure_ascii=False, indent=4)


def get_num_token_gpt3_5_turbo(text: str):
    import tiktoken
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def get_num_token_for_titles(path: str):
    CAP_1 = ["PROCEDURE", "INTRODUCTION", "FACTS AND PROCEDURE", "PROCÉDURE", "FAITS ET PROCÉDURE"]
    CAP_2 = ["THE FACTS", "AS TO THE FACTS", "EN FAIT"]
    CAP_3 = ["THE LAW", "AS TO THE LAW", "EN DROIT"]
    CAP_4 = ["FOR THESE REASONS, THE COURT, UNANIMOUSLY,", "FOR THESE REASONS, THE COURT UNANIMOUSLY",
             "PAR CES MOTIFS, LA COUR, À L’UNANIMITÉ,", "FOR THESE REASONS, THE COURT", "FOR THESE REASONS, THE COURT,",
             "PAR CES MOTIFS, LA COUR"]

    # regexp_1 = "PROCÉDURE|EN FAIT|EN DROIT|PAR CES MOTIFS, LA COUR, À L’UNANIMITÉ,"
    regexp = ""
    for cap in CAP_1 + CAP_2 + CAP_3 + CAP_4:
        regexp += cap + "|"
    regexp = regexp[:-1]

    pattern = re.compile(regexp)

    for file in os.listdir(path):
        complete_text = ""
        pdf_file = open(path + "/" + file, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            complete_text += text

        matches = pattern.findall(complete_text)
        matches.insert(0, "HEADER")

        # print(len(matches), matches)
        parts = pattern.split(complete_text)

        for i in range(len(parts)):
            print(f"{file}\t{matches[i]}\t{get_num_token_gpt3_5_turbo(parts[i])}")


if __name__ == "__main__":
    pdf_path = "../../data/corpus_pdf/"
    extract_titles_frequency(pdf_path)
    # get_num_token_for_titles(pdf_path)
