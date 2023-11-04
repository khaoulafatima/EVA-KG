from pandas import read_excel
import os.path
import re


def extract_document_url(title: str) -> str | None:
    """
    :return: stringa contenente il link del documento se presente, None altrimenti
    """
    path = "../../data/mapping_doc_link.xlsx"
    hudoc = "https://hudoc.echr.coe.int/eng?i="
    if not os.path.isfile(path):
        path = "../data/mapping_doc_link.xlsx"
    df = read_excel(path)
    for row in df.iterrows():
        if row[1][0] == title:
            match = re.search(r'"itemid"\s*:\s*\["([^"]+)"]', row[1][2])
            if match:
                itemid = match.group(1)
                return f"{hudoc}{itemid}"
            else:
                return None
    return None
