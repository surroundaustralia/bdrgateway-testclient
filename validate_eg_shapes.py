from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SH
from pyshacl import validate

ABISM = Namespace("https://linked.data.gov.au/def/abis-msg/")
TEST_DATA = Path(__file__).parent / "test_data"

g = Graph()
for f in Path(TEST_DATA / "messages").glob("*.ttl"):

    v = True
    g = Graph().parse(f)
    if (None, RDF.type, ABISM.CreateMessage) in g:
        print(f)
        r = validate(str(f), shacl_graph=str(Path(TEST_DATA) / "validators" / "vocpub-bdr.ttl"))
        # ignore SHACL Warnings
        for vr in r[1].objects(subject=None, predicate=SH.result):
            for sev in r[1].objects(subject=vr, predicate=SH.resultSeverity):
                if sev == SH.Violation:
                    v = False
                    print(r[1].serialize())

        print(f"Valid: {v}")

