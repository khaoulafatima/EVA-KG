import rdflib
import requests
import urllib.parse


def save_graph(rdf, in_format: str, to: str, name: str) -> bool:
    """
    :param rdf: stringa o grafo rdflib
    :param in_format: formato di rdf (ttl, xml, json, nt, trig, nq)
    :param to: formato di output (png, svg, pdf, ps, eps, gif, jpg)
    :param name: nome del file di output
    :return: True se il salvataggio è andato a buon fine, False altrimenti
    Effettua una richiesta al sito https://www.ldf.fi/service/rdf-grapher per salvare il grafo in un file
    Nota: utile per grafi piccoli dato il limite della lunghezza dell'url
    """
    try:
        rdf_string = ""
        if rdf is str:
            rdf_string = urllib.parse.quote_plus(rdf)
        elif rdf is rdflib.graph.Graph:
            rdf_string = urllib.parse.quote_plus(rdf.serialize())
        url = "http://www.ldf.fi/service/rdf-grapher?rdf=" + rdf_string + "&from=" + in_format + "&to=" + to
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Error: " + response.text)
        with open(f"{name}.{to}", "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(e)
        return False
