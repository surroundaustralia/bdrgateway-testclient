import argparse
import random
import string
from typing import Literal as Lit

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD

from _TERN import TERN
from synth import FEATURE_TYPES, METHOD_TYPES, MESSAGE_TYPES, BDRM, GEO, ATTRIBUTE_LIST, GEOMETRY_DICT
from synth import validate_number, random_char, rdf_ds_number, sampling_number, every_50_function
from model import Sampling


# need to be able to create N samplings
# start with making attribute list
# allow the sampling to have different:
# attribute, concept, foi,
# observations, rdfdatasets, sample,
# samplings, sites, values
# ADDITIONALLY: should have some geosparql data -> using the geometry dict
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
    msg_iri = URIRef("http://created_message.org/1")  # TODO: figure out what this iri is meant to be
    if msg_type == "create":
        g.add((msg_iri, RDF.type, msg_iris[msg_type]))
    else:  # TODO: fill in various options after following bdrm update/delete logic completed
        pass

    # Create Sampling Data -> every 50 samples should have a new feature of interest

    print(g.serialize())


def create_sampling_data(n: int):
    # Sampling - has foi, result_date_time, used_procedure, _has_result, optional iri
    # an activity of sampling carries out a sampling procedure to create a sample.
    # a sampling is the higher level of a sample
    # we should say that every 50 samples we create a new sampling. (therefore link to the has_result)
    # the feature of interest can be every 50 samplings -> generate another loop to create 50 of these
    # can have a fixed result_date_time for the time being

    # every 50 samples create a new sampling and append to sampling list
    # have a new rdf data set every 200 samplings

    # SUMMARY:
    # every 50 samplings -> sample, create a foi, every 4 foi create dataset
    sampling = []
    for index in range(0, sampling_number(n)):
        pass
    return sampling


def create_feature_of_interest(n: int):
    pass


def create_rdf_dataset(n: int):
    pass


def create_sample(n: int):
    pass

# create_synth_data(3, "create")


if __name__ == "__main__":
    from client.model import *

    # Sample
    # Sampling
    # FoI
    # RDFDataset
    ds1 = RDFDataset()
    foi1 = FeatureOfInterest(Concept(), ds1)
    sam1 = Sample(
        [foi1],
        Concept(),
        ds1,
        None
    )
    s1 = Sampling(
        foi1,
        Literal("2000-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/x"),
        [sam1]
    )
    sam1.is_result_of = s1
    # Site
    # Observation
    # Value
    # Attribute
    obs1 = Observation(
        ds1,
        Value(),
        foi1,
        Literal("timple result"),
        URIRef("http://example.com/observedproperty/n"),
        URIRef("http://example.com/instant/z"),
        Literal("2000-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/a"),
    )
    site1 = Site(
        obs1,
        [foi1],
        ds1,
        Concept()
    )
    sam1.is_sample_of.append(site1)
    g = sam1.to_graph()
    g += s1.to_graph()
    g += foi1.to_graph()
    g += ds1.to_graph()

    g += site1.to_graph()
    g += obs1.to_graph()

    print(g.serialize())
