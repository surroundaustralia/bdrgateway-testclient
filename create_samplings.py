from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD
BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")

samplings_data = [
    {
        "foi": "tbjc",
        "time": "2022-01-03",
        "procedure": "http://example.com/procedure/x",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        }
    },
    {
        "foi": "tbjc",
        "time": "2022-01-03",
        "procedure": "http://example.com/procedure/y",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        }
    },
    {
        "foi": "tbjc",
        "time": "2022-01-03",
        "procedure": "http://example.com/procedure/x",
        "result": {
            "dataset": "fake",
            "feature_type": "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
        }
    },
]
g = Graph(base="https://linked.data.gov.au/dataset/bdr/")
g.bind("bdrm", BDRM)
g.bind("dcterms", DCTERMS)
g.bind("sosa", SOSA)
g.bind("tern", TERN)
g.bind("void", VOID)

msg_iri = URIRef("http://createme.org/1")
g.add((msg_iri, RDF.type, BDRM.CreateMessage))

createme_id_max = 1
for sampling in samplings_data:
    # Sampling
    createme_id_max += 1
    sampling_iri = URIRef("http://createme.org/" + str(createme_id_max))
    g.add((msg_iri, DCTERMS.hasPart, sampling_iri))  # link Sampling to CreateMessage

    foi_iri = URIRef("https://linked.data.gov.au/dataset/bdr/site/" + sampling["foi"])

    g.add((sampling_iri, RDF.type, TERN.Sampling))
    g.add((sampling_iri, SOSA.hasFeatureOfInterest, foi_iri))
    g.add((sampling_iri, SOSA.resultTime, Literal(sampling["time"], datatype=XSD.date)))
    g.add((sampling_iri, SOSA.usedProcedure, URIRef(sampling["procedure"])))

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
