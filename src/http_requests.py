import requests
import os
from rdflib import Graph
from urllib.parse import quote


def rdf_grapher_request(graph: Graph, save_path: str, file_name: str, in_format: str, out_format: str) -> int:
    """
    Effettua una richiesta POST al servizio rdf-grapher per generare un'immagine del grafo
    :param graph: grafo da visualizzare del tipo rdflib.Graph
    :param save_path: percorso in cui salvare l'immagine
    :param file_name: nome del file
    :param in_format: formato del grafo
    :param out_format: formato dell'immagine
    :return: lo status code della richiesta (200 se va a buon fine, altrimenti un codice di errore)


    Sends a POST request to the rdf-grapher service to generate an image of the graph
    :param graph: graph to be visualized, of type rdflib.Graph
    :param save_path: path where the image will be saved
    :param file_name: name of the file
    :param in_format: format of the input graph
    :param out_format: format of the output image
    :return: the status code of the request (200 if successful, otherwise an error code)
    """
    supported_formats = ["ttl", "xml", "json", "nt", "trig", "nq"]
    supported_outputs = ["png", "svg", "pdf", "ps", "eps", "gif", "jpg"]
    if in_format not in supported_formats:
        raise Exception("Formato di input non supportato")
    if out_format not in supported_outputs:
        raise Exception("Formato di output non supportato")
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    fmt = ""
    if in_format == "ttl":
        fmt = "turtle"
    elif in_format == "xml":
        fmt = "xml"
    elif in_format == "json":
        fmt = "json-ld"
    elif in_format == "nt":
        fmt = "nt"
    elif in_format == "trig":
        fmt = "trig"
    elif in_format == "nq":
        fmt = "nquads"
    g_encoded = quote(graph.serialize(format=fmt))
    url = "https://www.ldf.fi/service/rdf-grapher"
    response = requests.post(url, data=f"rdf={g_encoded}&from={in_format}&to={out_format}")
    if response.status_code == 200:
        with open(save_path + "/" + file_name + "." + out_format, "wb") as f:
            f.write(response.content)
    return response.status_code

