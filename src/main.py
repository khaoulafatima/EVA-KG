import os
from ECHRDocument import ECHRDocument
import rdflib
from http_requests import rdf_grapher_request
from pyvis_utils import graph_to_pyvis_net
from neo4j_utils import graph_to_neo4j

if __name__ == "__main__":
    html_path = "../data/corpus_html"
    pdf_path = "../data/corpus_pdf"
    json_path = "../data/case_detail_json"
    body_path = "../data/document_body"
    triple_path = "../data/triples"
    while True:
        print("\033[92m")
        choice = input("1. Dall'inizio\n2. Grafo da triple salvate\n3. Esci\n> ")
        print("\033[0m")
        if choice == "1":
            save = True
            corpus = []
            for file in os.listdir(html_path):
                if not os.path.isdir(html_path + file):
                    file = file.replace(".html", "")
                    echr_document = ECHRDocument(html_path=html_path, pdf_path=pdf_path, file_name=file)
                    print(f"Processing: {echr_document}")
                    echr_document.extract_case_detail_from_html()
                    echr_document.extract_body_from_html()
                    echr_document.extract_triples_from_case_detail()
                    if save:
                        echr_document.case_detail_to_json(json_path)
                        echr_document.body_to_txt(body_path)
                        echr_document.save_triples(triple_path)
                    corpus.append(echr_document)
        elif choice == "2":
            while True:
                print("\033[92m")
                choice = input("1. RDF GRAPHER\n2. PYVIS\n3. NEO4J\n4. Indietro\n> ")
                print("\033[0m")
                if choice == "4":
                    break
                complete_graph = rdflib.Graph()
                print("Caricamento grafo...")
                for file in os.listdir(triple_path):
                    g = rdflib.Graph()
                    g.parse(triple_path + "/" + file, format="turtle")
                    complete_graph += g
                file_path = "../"
                file_name = "KG"
                save = input("Salvare il grafo in formato turtle? (y/n) ")
                if save == "y":
                    complete_graph.serialize(file_path + file_name + ".ttl", format="turtle")
                    print(f"Grafo salvato in {os.path.abspath(file_path)}\\{file_name}.ttl")
                print("Generazione immagine...")
                if choice == "1":
                    out_format = "svg"
                    status = rdf_grapher_request(complete_graph, file_path, file_name, "ttl", out_format)
                    if status == 200:
                        print(f"Immagine salvata in {os.path.abspath(file_path)}\\{file_name}.{out_format}")
                    os.startfile(os.path.abspath(file_path) + "/" + file_name + "." + out_format)
                elif choice == "2":
                    graph_to_pyvis_net(complete_graph, file_path, file_name, display=True)
                    print(f"Immagine salvata in {os.path.abspath(file_path)}\\{file_name}.html")
                elif choice == "3":
                    try:
                        graph_to_neo4j(complete_graph, "neo4j://localhost:7687", "neo4j")
                        print("Esegui la query MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN * su Neo4j Browser")
                    except:
                        print("\033[91mAssicurarsi che il server neo4j sia attivo\033[0m")
        elif choice == "3":
            break
