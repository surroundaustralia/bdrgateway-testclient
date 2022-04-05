import argparse
from tern_synthesizer import TernSynthesizer

import httpx
from rdflib import Graph

MESSAGE_TYPES = ["create", "update", "delete", "exists"]


def post_rdf_to_gateway(g: Graph):
    return httpx.post(
        "http://bdrgateway.surroundaustralia.com/validate",
        data=g.serialize(),
        headers={"Accept": "application/json"},
    )


parser = argparse.ArgumentParser()


def validate_number(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 10000:
        raise argparse.ArgumentTypeError(
            f"Samplings number must be >= 1 and <= 10000, you gave {value}"
        )
    return ivalue


parser.add_argument(
    "num",
    help="The number of Samplings you want to synthesise data for",
    type=validate_number,
)

parser.add_argument(
    "msg_type",
    help="The type of message to wrap the data in",
    choices=MESSAGE_TYPES,
)

args = parser.parse_args()

tern_rdf_graph = TernSynthesizer(args.num).to_graph()
