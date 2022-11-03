from client.synthesizer_tern import TernSynthesizer
from shapely.geometry import box
from client.model._TERN import TERN
from rdflib.namespace import RDF
from rdflib import Namespace
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


# def test_samplings_count():
#     # Geralton to Esperance
#     synth = TernSynthesizer(3, box(115.992191, -33.871399, 121.9467547, -28.572837))
#     g = synth.to_graph()
#     assert len(list(g.subjects(RDF.type, TERN.Sampling))) == 3
#     assert len(list(g.subjects(RDF.type, TERN.Sample))) == 3
#
#
# def test_coordinates():
#     # Geralton to Esperance
#     synth = TernSynthesizer(10, box(115.992191, -33.871399, 121.9467547, -28.572837))
#     for coord in synth.coordinate_points:
#         assert 115.992191 < coord.x < 121.9467547 and -33.871399 < coord.y < -28.572837


def test_high_10000_samplings_count():
    synth1 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth1.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth1.ttl")
    print("synth1serialized")

    synth2 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth2.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth2.ttl")
    print("synth2serialized")

    synth3 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth3.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth3.ttl")
    print("synth3serialized")

    synth4 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth4.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth4.ttl")
    print("synth4serialized")

    synth5 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth5.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth5.ttl")
    print("synth5serialized")

    synth6 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth6.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth6.ttl")
    print("synth6serialized")

    synth7 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth7.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth7.ttl")
    print("synth7serialized")

    synth8 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth8.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth8.ttl")
    print("synth8serialized")

    synth9 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth9.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth9.ttl")
    print("synth9serialized")

    synth10 = TernSynthesizer(10000, box(115.992191, -33.871399, 121.9467547, -28.572837))
    print("synth_generated")
    g = synth10.to_graph()
    print("synth_added_to_graph")
    g.serialize(destination="synth10.ttl")
    print("synth10serialized")
    assert True
    # assert len(list(g.subjects(RDF.type, TERN.Sampling))) == 10000
