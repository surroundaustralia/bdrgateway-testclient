from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SH
from pyshacl import validate

BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
TEST_DATA = Path(__file__).parent / "test_data"

print("Making validator...")
print()

# make the compound validator
g_sh = Graph()
for f in Path(TEST_DATA / "validators").glob("*.ttl"):
    g_sh.parse(f)
    print(f"adding {f}")

print()
print("Validating...")
print()

g = Graph()
for f in Path(TEST_DATA / "messages").glob("*.ttl"):
    v = True
    g = Graph().parse(f)
    # which messages are we checking?
    msgs_to_check = [
        (None, RDF.type, BDRM.CreateMessage),
        (None, RDF.type, BDRM.UpdateMessage),
        (None, RDF.type, BDRM.DeleteMessage),
        (None, RDF.type, BDRM.ExistsMessage)
    ]
    if any([x in g for x in msgs_to_check]):
        print(f.name)
        r = validate(str(f), shacl_graph=g_sh, ont_graph=Graph().parse(TEST_DATA / "bdr-msgs.ttl"))
        # ignore SHACL Warnings
        v = True
        for vr in r[1].objects(subject=None, predicate=SH.result):
            for sev in r[1].objects(subject=vr, predicate=SH.resultSeverity):
                if sev == SH.Violation:
                    v = False
                    fnodes = []
                    for fnode in r[1].objects(subject=vr, predicate=SH.focusNode):
                        fnodes.append(fnode)
                    msgs = []
                    for msg in r[1].objects(subject=vr, predicate=SH.resultMessage):
                        msgs.append(msg)
                    for i, fnode in enumerate(fnodes):
                        print(fnode, msgs[i])
        print(f"Valid: {v}")
        print()
