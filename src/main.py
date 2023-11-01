import os
from ECHRDocument import ECHRDocument
from pyvis.network import Network


def pyvis_net_options(n: Network):
    n.toggle_physics(False)
    n.show_buttons()
    # necessario prima configure, seguito da opzioni
    options = '''
        var options = {
            "configure": {
                "enabled": true,
                "filter": ["physics"]
            },
            "physics": {
                    "barnesHut": {
                    "gravitationalConstant": -30000,
                    "avoidOverlap": 1
                    }
            }
        }
    '''
    n.set_options(options)


def triples_to_pyvis(triples: list, n: Network):
    for triple in triples:
        s = triple["subject"]
        p = triple["predicate"]
        o = triple["object"]
        if s not in n.get_nodes():
            n.add_node(s, label=s)
        if o not in n.get_nodes():
            n.add_node(o, label=o)
        if p not in n.get_edges():
            n.add_edge(s, o, label=p)


if __name__ == "__main__":
    html_path = "../data/corpus_html"
    pdf_path = "../data/corpus_pdf"
    json_path = "../data/case_detail_json"
    body_path = "../data/document_body"
    triple_path = "../data/triples"
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

    net = Network()
    pyvis_net_options(net)
    for doc in corpus:
        triples_to_pyvis(doc.get_triples(), net)
    kg_name = os.path.abspath("../KG.html")
    print("Visualizzare knowledge graph? (y/n)")
    if input() == "y":
        print("Salvato in")
        net.show(kg_name, notebook=False)
    else:
        print("Salvato in\n" + kg_name)
        net.save_graph(kg_name)
