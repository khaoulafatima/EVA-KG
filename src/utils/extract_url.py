from pandas import read_excel
import os.path


def extract_document_url(title: str, alt: bool = True) -> str | None:
    """
    Estrarre il link di un documento a partire dal titolo, controllando nel file excel
    :param title: stringa contenente il titolo del documento di cui si vuole estrarre il link
    :param alt: se true si estrae il link senza encoding URL, altrimenti quello con encoding
        print(extract_document_url("CASE OF A AND B v. GEORGIA", alt=False)) -> https://hudoc.echr.coe.int/eng#{%22itemid%22:[%22001-215716%22]}
        print(extract_document_url("CASE OF A AND B v. GEORGIA", alt=True)) -> https://hudoc.echr.coe.int/eng#{"itemid":["001-215716"]}
    :return: stringa contenente il link del documento se presente, None altrimenti
    """
    path = "../../data/mapping_doc_link.xlsx"
    if not os.path.isfile(path):
        path = "../data/mapping_doc_link.xlsx"
    df = read_excel(path)
    for row in df.iterrows():
        if row[1][0] == title:
            if alt:
                return row[1][2]
            return row[1][1]
    return None
