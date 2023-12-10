from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
import os
import json

if __name__ == "__main__":
    path = "./"
    github_url = "https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl"
    wd = Namespace("http://www.wikidata.org/entity/")
    ont_ns = Namespace(github_url + "#")
    g = Graph()
    g.namespace_manager.bind("ont", ont_ns)

    # TIPI
    g.add((ont_ns.DomesticLaw, RDF.type, OWL.Class))
    g.add((ont_ns.DomesticLaw, RDFS.subClassOf, wd.Q7748))

    g.add((ont_ns.InternationalLaw, RDF.type, OWL.Class))
    g.add((ont_ns.InternationalLaw, RDFS.subClassOf, wd.Q7748))

    g.add((ont_ns.StrasbourgCaseLaw, RDF.type, OWL.Class))
    g.add((ont_ns.StrasbourgCaseLaw, RDFS.subClassOf, wd.Q11022655))

    # PROPRIETA'
    g.add((ont_ns.hasApplicationNumber, RDF.type, OWL.DatatypeProperty))
    g.add((ont_ns.hasApplicationNumber, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((ont_ns.hasApplicationNumber, RDFS.range, XSD.string))

    g.add((ont_ns.importanceLevel, RDF.type, OWL.DatatypeProperty))
    g.add((ont_ns.importanceLevel, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((ont_ns.importanceLevel, RDFS.range, XSD.integer))
    g.add((ont_ns.importanceLevel, XSD.minInclusive, Literal(1, datatype=XSD.integer)))
    g.add((ont_ns.importanceLevel, XSD.maxInclusive, Literal(4, datatype=XSD.integer)))

    g.add((ont_ns.respondentState, RDF.type, OWL.DatatypeProperty))
    g.add((ont_ns.respondentState, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((ont_ns.respondentState, RDFS.range, wd.Q3624078))

    g.add((ont_ns.involveConventionArticle, RDF.type, OWL.DatatypeProperty))
    g.add((ont_ns.involveConventionArticle, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((ont_ns.involveConventionArticle, RDFS.range, XSD.string))

    g.add((ont_ns.unanimousDecision, RDF.type, OWL.DatatypeProperty))
    g.add((ont_ns.unanimousDecision, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((ont_ns.unanimousDecision, RDFS.range, XSD.boolean))

    # DOMINIO e RANGE PROPRIETA' dcterm
    dcterms = Namespace("http://purl.org/dc/terms/")
    g.namespace_manager.bind("dcterms", dcterms)

    g.add((dcterms.type, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.type, RDFS.range, wd.Q327000))

    g.add((dcterms.contributor, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.contributor, RDFS.range, wd.Q40348))

    g.add((dcterms.date, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.date, RDFS.range, XSD.date))

    g.add((dcterms.isVersionOf, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.isVersionOf, RDFS.range, XSD.string))

    g.add((dcterms.abstract, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.abstract, RDFS.range, XSD.string))

    g.add((dcterms.references, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.references, RDFS.range, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.references, RDFS.range, ont_ns.DomesticLaw))
    g.add((dcterms.references, RDFS.range, ont_ns.InternationalLaw))

    g.add((dcterms.identifier, RDFS.domain, ont_ns.StrasbourgCaseLaw))
    g.add((dcterms.identifier, RDFS.range, XSD.string))

    g.add((dcterms.accessRights, RDFS.domain, XSD.string))
    g.add((dcterms.accessRights, RDFS.range, XSD.string))
    g.add((dcterms.accessRights, XSD.minInclusive, Literal("public", datatype=XSD.string)))
    g.add((dcterms.accessRights, XSD.maxInclusive, Literal("private", datatype=XSD.string)))

    # ENTITA'
    for file in os.listdir("../data/case_detail_json"):
        with open("../data/case_detail_json/" + file, "r", encoding="UTF-8") as f:
            cd_json = json.load(f)
            app_nos = cd_json["App. No(s)."]
            if isinstance(app_nos, str):
                g.add((ont_ns[app_nos], RDF.type, ont_ns.StrasbourgCaseLaw))
            elif isinstance(app_nos, list):
                for app_no in app_nos:
                    g.add((ont_ns[app_no], RDF.type, ont_ns.StrasbourgCaseLaw))

    print(g.serialize(format="turtle"))
    g.serialize(destination=path + "ontology.owl", format="xml")
