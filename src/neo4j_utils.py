from neo4j import GraphDatabase
from rdflib import Graph, term


def graph_to_neo4j(graph: Graph, neo4j_uri, neo4j_user):
    """
    :param graph: grafo di rdflib che si vuole caricare su neo4j
    :param neo4j_uri: uri del server neo4j
    :param neo4j_user: nome utente per accedere al server neo4j
    :return:
    la password deve essere salvata in un file neo4j_password.txt nella cartella principale


    :param graph: rdflib graph to be uploaded to Neo4j
    :param neo4j_uri: URI of the Neo4j server
    :param neo4j_user: username for accessing the Neo4j server
    :return:
    The password must be saved in a file named neo4j_password.txt in the main folder

    """
    neo4j_password = ""
    try:
        with open("../neo4j_password.txt", "r") as f:
            neo4j_password = f.read()
    except FileNotFoundError:
        print("File neo4j_password.txt non trovato")
    try:
        neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    except Exception as e:
        print(e)
        return
    with neo4j_driver.session() as session:
        # TODO vedere limite nodi
        session.run("MATCH (n) DETACH DELETE n")
        blank_nodes_mapping = {}
        for subj, pred, obj in graph:
            if isinstance(subj, term.BNode):
                if subj not in blank_nodes_mapping:
                    blank_nodes_mapping[subj] = f"blank_node_{len(blank_nodes_mapping)}"
                subj = blank_nodes_mapping[subj]
            else:
                subj = str(subj)
            if isinstance(obj, term.BNode):
                if obj not in blank_nodes_mapping:
                    blank_nodes_mapping[obj] = f"blank_node_{len(blank_nodes_mapping)}"
                obj = blank_nodes_mapping[obj]
            else:
                obj = str(obj)

            pred_str = str(pred)
            try:
                # TODO rivedere etichette
                # TODO rivedere errori per alcuni simboli
                session.run(f"""
                    MERGE (s {{name: "{subj}"}})
                    MERGE (o {{name: "{obj}"}})
                    MERGE (s)-[p:Predicate {{name: "{pred_str}"}}]->(o)
                    """)
            except Exception as e:
                print(e)

    # query: MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN *
