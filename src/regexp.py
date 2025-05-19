import os
import json
import re
from datetime import datetime


def strasbourg_case_law_re(scl: str) -> list:
    """
    Cerca le informazioni di interesse in una stringa che rappresenta una sentenza della Corte di Strasburgo.
    :param scl: stringa che rappresenta una sentenza della Corte di Strasburgo
    :return: lista con tre valori: titolo, numero, data (in formato yyyy-mm-dd)


    Search for relevant information in a string representing a judgment of the Strasbourg Court.
    :param scl: string representing a judgment of the Strasbourg Court
    :return: list with three values: title, number, date (in yyyy-mm-dd format)
    """
    content = [None, None, None]
    pattern_title = r"^(.*?), "
    pattern_app_no = r"\d+\/\d+"
    pattern_date = r"\d+ [A-Z][a-z]+ \d+"
    match_title = re.match(pattern_title, scl)
    match_app = re.search(pattern_app_no, scl)
    match_date = re.search(pattern_date, scl)
    if match_title:
        content[0] = match_title.group()[0:-2]
    if match_app:
        content[1] = match_app.group()
    if match_date:
        input_date_str = match_date.group()
        try:
            input_date = datetime.strptime(input_date_str, '%d %B %Y')
            output_date_str = input_date.strftime('%Y-%m-%d')
            content[2] = output_date_str
        except ValueError:
            pass
    return content


if __name__ == "__main__":
    path = "../data/case_detail_json"
    target = "Strasbourg Case-Law"
    for file in os.listdir(path):
        dct = json.load(open(path + "/" + file, encoding="UTF-8"))
        if target in dct.keys() and isinstance(dct[target], list):
            for value in dct[target]:
                match = strasbourg_case_law_re(value)
                if match[0] or match[1] or match[2]:
                    print(f"{value}")
                    print("\033[92m")
                    if match[0]:
                        print(f"\t{match[0]}")
                    if match[1]:
                        print(f"\t{match[1]}")
                    if match[2]:
                        print(f"\t{match[2]}")
                    print("\033[0m")
                else:
                    print(f"{value}")
                    print("\033[91m")
                    print("\tNo match found.")
                    print("\033[0m")
