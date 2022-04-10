import argparse
from synthesizer_tern import TernSynthesizer
from synthesizer_abis import AbisSynthesizer

import httpx
from rdflib import Graph

from shapely.geometry import box

SCENARIOS = ["broad", "degree", "narrow", "embargoed", "conservation"]
MESSAGE_TYPES = ["create", "update", "delete", "exists"]


def post_rdf_to_gateway(g: Graph):
    return httpx.post(
        "http://bdrgateway.surroundaustralia.com/validate",
        data=g.serialize(),
        headers={"Accept": "application/json"},
    )


def validate_number(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 10000:
        raise argparse.ArgumentTypeError(
            f"Samplings number must be >= 1 and <= 10000, you gave {value}"
        )
    return ivalue


def process_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "scenario",
        help="The data generation scenario wanted. 'broad' is Esperance to Geralton, 'degree' is a 1 square degree "
             "area, 'narrow' is a 0.1 x 0.1 degree area",
        choices=SCENARIOS,
    )

    parser.add_argument(
        "-n",
        "--num",
        help="The number of Samplings you want to synthesise data for",
        type=validate_number,
        required=False
    )

    parser.add_argument(
        "-m",
        "--msgtype",
        help="The type of message to wrap the data in",
        choices=MESSAGE_TYPES,
    )

    return parser.parse_args()


def main(args):
    if args.scenario == "broad":
        # Geralton to Esperance area
        g = TernSynthesizer(args.num, box(115.992191, -33.871399, 121.9467547, -28.572837)).to_graph()
    elif args.scenario == "degree":
        # 1 degree square area
        g = TernSynthesizer(args.num, box(117, -30, 118, -29)).to_graph()
    elif args.scenario == "narrow":
        g = TernSynthesizer(args.num, box(116, -30, 116.01, -29.99)).to_graph()
    elif args.scenario == "embargoed":
        g = AbisSynthesizer("embargoed").to_graph()
    elif args.scenario == "conservation":
        g = AbisSynthesizer("conservation").to_graph()

    return g.serialize()


if __name__ == "__main__":
    args = process_args()
    print(main(args))
