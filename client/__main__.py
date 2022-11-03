import argparse
import pstats
import time
import cProfile as profile
from synthesizer_tern import TernSynthesizer
from synthesizer_abis import AbisSynthesizer
from synthesiser_simple import BasicSynthesizer
from synthesiser_conservation import TernSynthesizerConservation
from uuid import uuid4

import httpx
from rdflib import Graph, URIRef, Literal

from shapely.geometry import box

SCENARIOS = ["broad", "degree", "narrow", "embargoed", "conservation", "simple_different", "simple_same",
             "RA_ask"]
MESSAGE_TYPES = ["create", "update", "delete", "exists"]


def post_rdf_to_gateway(g: Graph):
    return httpx.post(
        "http://bdrgateway.surroundaustralia.com/validate",
        data=g.serialize(),
        headers={"Accept": "application/json"},
    )


def validate_number(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 15000000:
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
    total_st = time.time()
    process_st = time.process_time()
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
    elif args.scenario == "simple_different":
        g = BasicSynthesizer.different_types_graph(args.num)
    elif args.scenario == "simple_same":
        g = BasicSynthesizer.repeated_types_graph(args.num)
    elif args.scenario == "RA_ask":
        g = TernSynthesizerConservation(args.num, box(115.992191, -33.871399, 121.9467547, -28.572837)).to_graph()


    prof = profile.Profile()
    serialize_st = time.time()
    prof.enable()
    g.serialize(destination="test_data.ttl")
    prof.disable()
    serialize_et = time.time()

    total_et = time.time()
    process_et = time.process_time()
    total_process_time = process_et - process_st
    total_elapsed_time = total_et - total_st
    stats = pstats.Stats(prof).strip_dirs().sort_stats("cumtime")
    return print(f"g.serialize time: {serialize_et - serialize_st} \n"
                 f"_____________________________________________\n"
                 f"Total execution time: {total_elapsed_time} seconds \n"
                 f"Total process time: {total_process_time} seconds\n"
                 f"{stats.print_stats(15)}")


if __name__ == "__main__":
    args = process_args()
    main(args)

