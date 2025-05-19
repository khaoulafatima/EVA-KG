from qwikidata.sparql import return_sparql_query_results
import time


def get_country_identifier(country_name: str) -> str or None:
    """
    Cerca su Wikidata l'identificatore di un paese dato il suo nome
    :param country_name: il nome del paese da cercare, in inglese
    :return: una stringa contenente l'identificatore Wikidata del paese o None se non trovato

    Search Wikidata for the identifier of a country given its name.
    :param country_name: the name of the country to search for, in English
    :return: a string containing the Wikidata identifier of the country, or None if not found
    """
    query_label = f"""
        SELECT ?item
        WHERE
        {{
            ?item wdt:P31 wd:Q3624078.    #P31 = instance of, Q3624078 = sovereign state
            ?item rdfs:label "{country_name}"@en.
        }}
        """
    query_alt_label = f"""
        SELECT ?item
        WHERE
        {{
            ?item wdt:P31 wd:Q3624078.
            ?item skos:altLabel "{country_name}"@en
        }}
        """
    try:
        results = return_sparql_query_results(query_label)
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["item"]["value"]
        results = return_sparql_query_results(query_alt_label)
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["item"]["value"]
    except Exception as e:
        if str(e) == "Expecting value: line 1 column 1 (char 0)":
            print(f"\033[91m{get_country_identifier.__name__}({country_name}):"
                  f" Too many requests, waiting 2 seconds...\033[0m")
        time.sleep(2)
        return get_country_identifier(country_name)
    return None


if __name__ == "__main__":
    """
    example of use
    """
    import json

    file = "utils/case_detail_frequency.json"
    file = json.load(open(file, encoding="UTF-8"))
    countries = list(file["Respondent State(s)"])
    for country in countries:
        identifier = get_country_identifier(country)
        if identifier:
            print(f"{country}: {identifier}")
        else:
            print(f"{country}: No data found")
