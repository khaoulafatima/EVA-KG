from flask import Flask, request
from rdflib import Graph
from threading import Thread
import os
import time
import requests
import pprint

app = Flask(__name__)


@app.route("/sparql", methods=["GET", "POST"])
def sparql_endpoint():
    query = request.args.get("query", "")
    result = execute_sparql_query(query)
    return result


def execute_sparql_query(query):
    g = Graph()
    g.parse("../KG.ttl", format="turtle")
    results = g.query(query)
    formatted_results = format_query_results(results)
    return formatted_results


def format_query_results(results):
    return results.serialize(format="json").decode("utf-8")


def endpoint_request():
    endpoint_url = 'http://localhost:5000/sparql'
    time.sleep(5)
    while True:
        sparql_query_string = input("\033[92mInserisci una query oppure \"exit\" per chiudere: \033[0m")
        if sparql_query_string == "exit":
            os.system("taskkill /F /IM python.exe")
        else:
            # sparql_query_string = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
            # sparql_query_string = "SELECT ?s ?p ?o WHERE { BIND(<http://eva.org/entity/40020/03> AS ?s) ?s ?p ?o }"
            print(f"Query posta: {sparql_query_string}")
            response = requests.get(endpoint_url, params={"query": sparql_query_string, "format": "json"})

            if response.status_code == 200:
                results = response.json()
                pprint.pprint(results['results']['bindings'], sort_dicts=False)
                print(f"\nOttenuti {len(results['results']['bindings'])} risultati\n")
                time.sleep(2)
            else:
                print(f"Errore nella richiesta SPARQL: {response.status_code} - {response.text}")


if __name__ == "__main__":
    er = Thread(target=endpoint_request)
    er.start()
    app.run(host="localhost", port=5000, debug=True)
