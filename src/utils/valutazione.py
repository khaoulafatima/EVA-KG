from rdflib import Graph, Namespace
import requests


def get_wikidata_label(uri):
    entity_id = uri.split('/')[-1]

    sparql_query = f"""
        SELECT ?itemLabel
        WHERE {{
          wd:{entity_id} rdfs:label ?itemLabel.
          FILTER(LANG(?itemLabel) = "en") 
        }}
    """

    params = {
        'format': 'json',
        'query': sparql_query
    }

    endpoint_url = 'https://query.wikidata.org/sparql'

    response = requests.get(endpoint_url, params=params, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

    try:
        data = response.json()
        label = data['results']['bindings'][0]['itemLabel']['value']
        return label
    except (IndexError, KeyError):
        return None


g = Graph()
g.parse("../../KG.ttl", format="turtle")
print(f"Numero di triple: {len(g)}")
print(f"Numero di nodi: {len(g.all_nodes())}")

predicates = set()
for s, p, o in g:
    predicates.add(p)
print(f"Numero di predicati: {len(predicates)}")

subjects = set()
for s, p, o in g:
    subjects.add(s)
print(f"Numero di soggetti: {len(subjects)}")

objects = set()
for s, p, o in g:
    objects.add(o)
print(f"Numero di oggetti: {len(objects)}")

wd = Namespace("http://www.wikidata.org/entity/")
wikidata = set()
for s, p, o in g:
    if o.startswith(wd):
        wikidata.add(o)
print(f"Numero di risorse di wikidata: {len(wikidata)}")
print("Risorse di wikidata:")
for resource in wikidata:
    print(f"\t{resource}: {get_wikidata_label(resource)}")
