from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SH
from pyshacl import validate
import sys


def print_validity(r):
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

if len(sys.argv) > 1:
    f = Path(TEST_DATA / "messages" / sys.argv[1])
    print(f)
    r = validate(str(f), shacl_graph=g_sh, ont_graph=Graph().parse(TEST_DATA / "bdr-msgs.ttl"))
    print_validity(r)

    exit()

g = Graph()
for f in sorted(list(Path(TEST_DATA / "messages").glob("*.ttl"))):
    print(f)
    v = True
    try:
        g = Graph().parse(f)
    except Exception as e:
        print(f"INVALID RDF: {e}")
        print()
        continue

    r = validate(str(f), shacl_graph=g_sh, ont_graph=Graph().parse(TEST_DATA / "bdr-msgs.ttl"))
    print_validity(r)
