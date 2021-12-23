from pathlib import Path
from rdflib import Graph


TEST_DATA = Path(__file__).parent / "test_data" / "messages"

g = Graph()
for f in TEST_DATA.glob("*.ttl"):
    print(f)
    g.parse(f)
