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
        "http://ndesgateway.surroundaustralia.com/validate",
        data=g.serialize(),
        headers={"Accept": "application/json"}
    )


if __name__ == "__main__":
    test_rdf = """
    <a:> <b:> <c:> .
    """
    test_graph = Graph().parse(data=test_rdf)
    r = post_rdf_to_gateway(test_graph)
    if r.status_code == 200:
        print("OK!")
    else:
        pprint(r.json()[0]["message"])
