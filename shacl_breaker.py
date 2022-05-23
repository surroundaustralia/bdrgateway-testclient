"""Removes triples from a valid TestClient dataset to deliberately force TERN Ontology shapes errors

Use: on the command line:

~$ python shacl_breaker.py {input_rdf_file_path}

Adds ".broken" to the input_rdf_file_path to create a file path for the output

e.g.:

~$ python shacl_breaker.py test_client_conservation_01.ttl
-->
test_client_conservation_01.broken.ttl

"""
import sys
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import VOID


def main(input_rdf_file_path: Path):
    g = Graph().parse(input_rdf_file_path)
    g.remove((None, VOID.inDataset, None))
    out_file_path = str(input_rdf_file_path).replace(input_rdf_file_path.suffix, ".broken" + input_rdf_file_path.suffix)
    g.serialize(destination=out_file_path)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
