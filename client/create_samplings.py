from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD

# from _TERN import TERN
# adding this for now as I'm recieing errors
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


# Feature Types vocab http://linked.data.gov.au/def/tern-cv/68af3d25-c801-4089-afff-cf701e2bd61d
# Method Types vocab http://linked.data.gov.au/def/tern-cv/9b6e057f-271b-48f6-8c33-0528bf6b60df

samplings_data = [
    {
        "foi": "tbjc",
        "time": "2022-01-03T12:13:14",
        "procedure": "http://example.com/procedure/x",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        }
    },
    {
        "foi": "tbjc",
        "time": "2022-01-03T12:13:14",
        "procedure": "http://example.com/procedure/y",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        }
    },
    {
        "foi": "tbjc",
        "time": "2022-01-03T12:13:14",
        "procedure": "http://example.com/procedure/x",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        },
        "geometry": {
            "WKT": "POINT (145.609997 -35.238957)"
        }
    },
    {
        "foi": "tbjc",
        "time": "2022-01-03T12:13:14",
        "procedure": "http://example.com/procedure/x",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        },
        "geometry": {
            "WKT": "POINT (145.772569 -35.265073)"
        }
    },
]
g = Graph(base="https://linked.data.gov.au/dataset/bdr/")
g.bind("bdrm", BDRM)
g.bind("dcterms", DCTERMS)
g.bind("geo", GEO)
g.bind("sosa", SOSA)
g.bind("tern", TERN)
g.bind("void", VOID)

# BDR Message
msg_iri = URIRef("http://createme.org/1")
g.add((msg_iri, RDF.type, BDRM.CreateMessage))

# RDFDataset
# TODO: scale this up from 1 to total no. of Samplings / y (y = 200)
ds = URIRef("http://example.com/dummy/dataset")
g.add((ds, RDF.type, TERN.RDFDataset))

# FoI
# TODO: scale this up from 1 to total no. of Samplings / x (x = 50)
foi = URIRef("https://linked.data.gov.au/dataset/bdr/site/tbjc")
g.add((foi, RDF.type, TERN.FeatureOfInterest))
g.add((foi, TERN.featureType, URIRef("http://linked.data.gov.au/def/tern-cv/2090cfd9-8b6b-497b-9512-497456a18b99")))
# TODO: use all of the Datasets in the list that you've generated above
g.add((foi, VOID.inDataset, ds))

createme_id_max = 1
for sampling in samplings_data:
    # Sampling
    createme_id_max += 1
    sampling_iri = URIRef("http://createme.org/" + str(createme_id_max))
    g.add((msg_iri, DCTERMS.hasPart, sampling_iri))  # link Sampling to CreateMessage

    # TODO: use all of the FoIs in the list that you've generated above
    foi_iri = URIRef("https://linked.data.gov.au/dataset/bdr/site/" + sampling["foi"])

    g.add((sampling_iri, RDF.type, TERN.Sampling))
    g.add((sampling_iri, SOSA.hasFeatureOfInterest, foi_iri))
    g.add((sampling_iri, SOSA.resultTime, Literal(sampling["time"], datatype=XSD.dateTime)))
    g.add((sampling_iri, SOSA.usedProcedure, URIRef(sampling["procedure"])))

    if sampling.get("geometry") is not None:
        geom = BNode()
        g.add((geom, RDF.type, GEO.Geometry))
        g.add((geom, GEO.asWKT, Literal(sampling.get("geometry")["WKT"], datatype=GEO.wktLiteral)))
        g.add((sampling_iri, GEO.hasGeometry, geom))

    # Sample
    createme_id_max += 1
    sample_iri = URIRef("http://createme.org/" + str(createme_id_max))
    dataset_iri = URIRef("https://linked.data.gov.au/dataset/bdr/dataset/" + sampling["result"]["dataset"])
    g.add((sample_iri, RDF.type, TERN.Sample))
    g.add((sample_iri, SOSA.isResultOf, sampling_iri))
    g.add((sample_iri, SOSA.isSampleOf, foi_iri))
    g.add((sample_iri, VOID.inDataset, dataset_iri))
    g.add((sample_iri, TERN.featureType, URIRef(sampling["result"]["feature_type"])))

    # link Sample to Sampling
    g.add((sampling_iri, SOSA.hasResult, sample_iri))

print(g.serialize())

