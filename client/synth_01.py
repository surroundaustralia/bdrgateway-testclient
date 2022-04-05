from typing import Literal as Lit

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD

from _TERN import TERN
from synth import MESSAGE_TYPES, BDRM, GEO
from synth import validate_number, sampling_number, rdf_ds_number
from client.model import *


def prefix_creation():
    g = Graph()
    g.bind("bdrm", BDRM)
    g.bind("dcterms", DCTERMS)
    g.bind("geo", GEO)
    g.bind("sosa", SOSA)
    g.bind("tern", TERN)
    g.bind("void", VOID)
    return g


def create_synth_data(n: int, msg_type: Lit["create", "update", "delete", "exists"]):
    # validate the data and ensure data points is within 1 - 10000
    if not validate_number(n):
        raise ValueError("%s is not >= 1" % n)

    # ensuring a bdrm message is used
    if msg_type not in MESSAGE_TYPES:
        raise ValueError(f"msg_type must be one of {', '.join(MESSAGE_TYPES)}")

    # Prefix and base URI creation
    g = prefix_creation()
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


def create_feature_of_interest(n: int):
    pass


def create_sample(n: int):
    pass


def link_sample_to_sampling_is_result_of(n: int):
    pass


def create_observation(n: int):
    pass


def create_site(n: int):
    pass


def append_site(n: int):
    pass


def add_to_graph(n: int):
    pass


# 200 samplings -> 1 dataset
def create_synthetic_data(n):
    create_rdf_dataset(n)
    create_feature_of_interest(n)
    create_sample(n)
    create_sampling(n)
    link_sample_to_sampling_is_result_of(n)
    create_observation(n)
    create_site(n)
    append_site(n)
    add_to_graph(n)


if __name__ == "__main__":
    from client.model import *

    # Creating one of each
    # Sample
    # Sampling
    # FoI
    # RDFDataset
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
    # Site
    # Observation
    # Value
    # Attribute
    observation_1 = Observation(
        dataset_1,
        Value(),
        feature_of_interest_1,
        Literal("timple result"),
        URIRef("http://example.com/observedproperty/n"),
        URIRef("http://example.com/instant/z"),
        Literal("2000-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/a"),
    )
    site1 = Site(observation_1, [feature_of_interest_1], dataset_1, Concept())
    sample_1.is_sample_of.append(site1)
    g = sample_1.to_graph()
    g += sampling_1.to_graph()
    g += feature_of_interest_1.to_graph()
    g += dataset_1.to_graph()

    g += site1.to_graph()
    g += observation_1.to_graph()

    # print(g.serialize())

