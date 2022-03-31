import httpx
from rdflib import Graph
from pprint import pprint
from pathlib import Path

TEST_DATA = Path(__file__).parent / "test_data"

tests = [
    {
        "name": "Single Sampling",
        "desc": "Simplest form of a valid Sampling",
        "file": TEST_DATA / "t001.ttl",
        "valid": True
    }
]


def post_rdf_to_gateway(g: Graph):
    return httpx.post(
        "http://bdrgateway.surroundaustralia.com/validate",
        data=g.serialize(),
        headers={"Accept": "application/json"}
    )


if __name__ == "__main__":
    test_rdf = """
    <a:> <b:> <c:> .
    """
    test_graph = Graph().parse("test_data/messages/Concept_create_i2.ttl")
    r = post_rdf_to_gateway(test_graph)
    if r.status_code == 200:
        print("OK!")
    else:
        msgs = r.json()
        errors = [x["message"] for x in msgs if x["severity"] == "violation"]
        print("Errors:")
        for err in errors:
            print(f"* {err}")

        print()

        errors = [x["message"] for x in msgs if x["severity"] == "warning"]
        print("Warnings:")
        for err in errors:
            print(f"* {err}")
