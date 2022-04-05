from typing import Literal as Lit

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD

from client.model._TERN import TERN
from client.tern_synthesizer import BDRM, GEO, validate_number, sampling_number, rdf_ds_number
from client.__main__ import MESSAGE_TYPES
from model import *


def bind_prefixes(g: Graph):
    g.bind("bdrm", BDRM)
    g.bind("dcterms", DCTERMS)
    g.bind("geo", GEO)
    g.bind("sosa", SOSA)
    g.bind("tern", TERN)
    g.bind("void", VOID)


def create_synth_data(n: int, msg_type: Lit["create", "update", "delete", "exists"]):
    # validate the data and ensure data points is within 1 - 10000
    if not validate_number(n):
        raise ValueError("%s is not >= 1" % n)

    # ensuring a bdrm message is used
    if msg_type not in MESSAGE_TYPES:
        raise ValueError(f"msg_type must be one of {', '.join(MESSAGE_TYPES)}")

    # Prefix and base URI creation
    g = bind_prefixes()
    # BDR Message
    msg_iris = {
        "create": BDRM.CreateMessage,
        "update": BDRM.UpdateMessage,
        "delete": BDRM.DeleteMessage,
        "exists": BDRM.ExistsMessage,
    }
    msg_iri = URIRef(
        "http://created_message.org/1"
    )  # TODO: figure out what this iri is meant to be
    if msg_type == "create":
        g.add((msg_iri, RDF.type, msg_iris[msg_type]))
    else:  # TODO: fill in various options after following bdrm update/delete logic completed
        pass

    # Create Sampling Data -> every 50 samples should have a new feature of interest

    print(g.serialize())


def create_rdf_dataset(n: int):
    g = Graph()
    for index in range(0, rdf_ds_number(n)):
        rdf_data_set = RDFDataset()
        g += rdf_data_set.to_graph()
    return g


def create_sampling(n: int):
    sampling = []
    for index in range(0, sampling_number(n)):
        pass
    return sampling


def link_sample_to_sampling_is_result_of(n: int):
    pass


def create_n_samples_graph(n: int) -> Graph:

    dataset_1 = RDFDataset()
    feature_of_interest_1 = FeatureOfInterest(Concept(), dataset_1)
    sample_1 = Sample([feature_of_interest_1], Concept(), dataset_1, None)
    sampling_1 = Sampling(
        feature_of_interest_1,
        Literal("2000-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/x"),
        [sample_1],
    )
    sample_1.is_result_of = sampling_1
    observation_1 = Observation(
        dataset_1,
        Float(Literal(42.3)),
        feature_of_interest_1,
        Literal("simple result"),
        URIRef("http://example.com/observedproperty/n"),
        URIRef("http://example.com/instant/z"),
        Literal("2000-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/a"),
    )
    site1 = Site(observation_1, [feature_of_interest_1], dataset_1, Concept())
    sample_1.is_sample_of.append(site1)

    return sample_1.to_graph()


if __name__ == "__main__":
    print(create_n_samples_graph(n).serialize())
