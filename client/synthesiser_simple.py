import random
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
try:
    from client.model._TERN import TERN
    from client.model import *
except:
    import sys
    from pathlib import Path

    p = Path(__file__).parent.parent.resolve()
    sys.path.append(str(p))
    from client.model._TERN import TERN
    from client.model import *

BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")

MESSAGE_TYPES = ["create", "update", "delete", "exists"]
ANIMAL_CONCEPT = Concept(
    "http://linked.data.gov.au/def/tern-cv/2361dea8-598c-4b6f-a641-2b98ff199e9e"
)
ANIMAL_POPULATION_CONCEPT = Concept(
    "http://linked.data.gov.au/def/tern-cv/cd5cbdbb-07d9-4a5b-9b11-5ab9d6015be6"
)

SCIENTIFIC_NAME_IDS = [
    URIRef("https://fake-scientific-name-id.com/name/afd/001"),
    URIRef("https://fake-scientific-name-id.com/name/afd/002"),
    URIRef("https://fake-scientific-name-id.com/name/afd/003"),
    URIRef("https://fake-scientific-name-id.com/name/afd/004"),
    URIRef("https://fake-scientific-name-id.com/name/afd/005"),
    URIRef("https://fake-scientific-name-id.com/name/afd/006"),
    URIRef("https://fake-scientific-name-id.com/name/afd/007"),
    URIRef("https://fake-scientific-name-id.com/name/afd/008"),
    URIRef("https://fake-scientific-name-id.com/name/afd/009"),
    URIRef("https://fake-scientific-name-id.com/name/afd/010"),
]

NSL_REAL_VALUES = [
    URIRef("https://id.biodiversity.org.au/tree/aal"),
    URIRef("https://id.biodiversity.org.au/tree/abl"),
    URIRef("https://id.biodiversity.org.au/tree/afd"),
    URIRef("https://id.biodiversity.org.au/tree/afl"),
    URIRef("https://id.biodiversity.org.au/tree/all"),
    URIRef("https://id.biodiversity.org.au/tree/apc"),
]


class BasicSynthesizer:
    def __init__(self, n: int):
        assert n > 0, f"n, the number of Samples " \
                      f"must be greater than 0. " \
                      f"You provided: {n}"

    def different_types_graph(n: int):
        assert n > 0, "n needs to be greater than 0"
        g = Graph()
        for i in range(n):
            g.add((URIRef(f"https://example.com/{i}"), RDF.type, URIRef(f"https://example.com/type/{i}")))
            g.add((URIRef(f"https://example.com/{i}"), RDFS.label, Literal(f"example_label_{i}")))
        return g

    # picking from 1-3 different types
    def repeated_types_graph(n: int):
        assert n > 0, "n needs to be greater than 0"
        types = [URIRef(f"https://example.com/type/1"),
                 URIRef(f"https://example.com/type/2"), URIRef(f"https://example.com/type/3")]
        g = Graph()
        for i in range(n):
            g.add((URIRef(f"https://example.com/{i}"), RDF.type, random.choice(types)))
            g.add((URIRef(f"https://example.com/{i}"), RDFS.label, Literal(f"example_label_{i}")))
        return g
    def simple_example(self):
        pass
