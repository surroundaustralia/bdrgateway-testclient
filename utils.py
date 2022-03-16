from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD
import random
import string

# from _TERN import TERN
# adding this for now as I'm recieing errors
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
# Feature Types vocab http://linked.data.gov.au/def/tern-cv/68af3d25-c801-4089-afff-cf701e2bd61d
# Method Types vocab http://linked.data.gov.au/def/tern-cv/9b6e057f-271b-48f6-8c33-0528bf6b60df
FEATURE_TYPES = [URIRef("http://linked.data.gov.au/def/tern-cv/05dac53a-269c-4699-9673-bf99a9406b14"),
                 # administrative_area
                 URIRef("http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"),
                 # animal Individuals
                 URIRef("http://linked.data.gov.au/def/tern-cv/2361dea8-598c-4b6f-a641-2b98ff199e9e"),
                 # animal occurence
                 URIRef("http://linked.data.gov.au/def/tern-cv/8a68b4a9-167b-40f0-9222-293a2d20ffee"),
                 # animal population
                 URIRef("http://linked.data.gov.au/def/tern-cv/cd5cbdbb-07d9-4a5b-9b11-5ab9d6015be6"),
                 # animal specimen
                 URIRef("http://linked.data.gov.au/def/tern-cv/6d40d71e-58cd-4f75-8304-40c01fe5f74c"),  # climate
                 URIRef("http://linked.data.gov.au/def/tern-cv/45a73139-f6bf-47b7-88d4-4b2865755545"),
                 # fungal occurence
                 URIRef("http://linked.data.gov.au/def/tern-cv/afc81cca-9122-4e36-823d-31dd765e9257"),
                 # Geologic substrate
                 URIRef("http://linked.data.gov.au/def/tern-cv/2090cfd9-8b6b-497b-9512-497456a18b99"),  # habitat
                 URIRef("http://linked.data.gov.au/def/tern-cv/7e256d28-e686-4b6a-b64a-ac1b1a8f164d"),
                 # land surface disturbance
                 URIRef("http://linked.data.gov.au/def/tern-cv/aef12cd6-3826-4988-a54c-8578d3fb4c8d"),
                 # land surface substrate
                 URIRef("http://linked.data.gov.au/def/tern-cv/2cf3ed29-440e-4a50-9bbc-5aab30df9fcd"),  # landform
                 URIRef("http://linked.data.gov.au/def/tern-cv/80c39b95-0912-4267-bb66-2fa081683723"),  # soil profile
                 URIRef("http://linked.data.gov.au/def/tern-cv/06461021-a6c2-4175-9651-23653c2b9116"),  # soil sample
                 URIRef("http://linked.data.gov.au/def/tern-cv/d738a3f9-9b00-4adf-9dc8-0577269b691d"),  # soil Specimen
                 URIRef("http://linked.data.gov.au/def/tern-cv/60d7edf8-98c6-43e9-841c-e176c334d270"),
                 # plant individual
                 URIRef("http://linked.data.gov.au/def/tern-cv/2e122e23-881c-43fa-a921-a8745f016ceb"),
                 # plant specimen
                 ]

METHOD_TYPES = ["HCL_droplets_1_ML", "densitometer", "dgps",
                "electrical_conductivity_meter", "ph_meter", "point_intercept",
                "soil_core", "soil_pit", "visual_assessment", "basal_wedge",
                "diameter_measurement_instrument", "diameter_tape",
                "human_measurement", "human_observation", "instrument_measurement",
                "munsell_soil_colour_chart", "soil_10_cm_samples",
                "soil_auger_boring", "soil_vertical_exposure", "vertex_hypsometer"]


def validate_number(n):
    if n < 0 or n > 10000:
        print("Data number has to be greater than 0 and less than 10000")
        return False
    return True


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def rdf_ds_number(n):
    if n < 200:
        x = 1
        return x
    # every increment of 200, I want to add a dataset
    y = 1 + int(n / 200)
    return y


def sampling_number(n):
    if n < 50:
        x = 1
        return x
    y = 1 + int(n / 50)
    return y


def every_50_function(n):
    x = []
    for index in range(0, sampling_number(n)):
        x.append(str(random_char(5)))
    return x


# only every 50 samples should there be new foi
def create_sampling_data(n):
    samplings_data = []
    x = every_50_function(n)
    for index in range(0, n):
        samplings_data.append({"foi": x[int(index / 50)],
                               "time": "2022-01-03T12:13:14",
                               "procedure": "http://example.com/procedure/" + random.choice(METHOD_TYPES),
                               "result": {
                                   "dataset": "fake",
                                   "feature_type": random.choice(FEATURE_TYPES)
                               }})
        # can consider the geometry but will see after
    return samplings_data


def create_dataset(n):
    if validate_number(n) != False:
        pass
    else:
        exit(1)
    # Prefix and base URI creation
    g = Graph(base="https://linked.data.gov.au/dataset/bdr/")
    g.bind("bdrm", BDRM)
    g.bind("dcterms", DCTERMS)
    g.bind("geo", GEO)
    g.bind("sosa", SOSA)
    g.bind("tern", TERN)
    g.bind("void", VOID)

    # BDR Messages
    msg_iri = URIRef("http://createme.org/1")
    g.add((msg_iri, RDF.type, BDRM.CreateMessage))

    # creating sampling data
    samplings_data = create_sampling_data(n)

    # RDF Dataset created based on increments of 200
    for index in range(0, rdf_ds_number(n)):
        ds = URIRef("http://example.com/dummy/dataset/" + str(index + 1))
        g.add((ds, RDF.type, TERN.RDFDataset))

    # FOI
    # need to keep track of list for code below
    foi_list = []
    for index in range(0, sampling_number(n)):
        foi = URIRef("https://linked.data.gov.au/dataset/bdr/site/" + samplings_data[index]["foi"])
        # + "/foi_number/" + str(index + 1))
        foi_list.append(foi)
        g.add((foi, RDF.type, TERN.FeatureOfInterest))
        g.add((foi, TERN.featureType, random.choice(FEATURE_TYPES)))

        # integrating foi into associated ds
        x = int(index / 4) + 1
        ds = URIRef("http://example.com/dummy/dataset/" + str(x))
        g.add((foi, VOID.inDataset, ds))

    # creating sampling stuff
    createme_id_max = 1
    for sampling in samplings_data:
        # sampling
        createme_id_max += 1
        sampling_iri = URIRef("http://createme.org/" + str(createme_id_max))
        g.add((msg_iri, DCTERMS.hasPart, sampling_iri))  # link Sampling to CreateMessage

        foi_iri = URIRef("https://linked.data.gov.au/dataset/bdr/site/" + sampling["foi"])
        g.add((sampling_iri, RDF.type, TERN.Sampling))
        g.add((sampling_iri, SOSA.hasFeatureOfInterest, foi_iri))
        g.add((sampling_iri, SOSA.resultTime, Literal(sampling["time"], datatype=XSD.dateTime)))
        g.add((sampling_iri, SOSA.usedProcedure, URIRef(sampling["procedure"])))

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

    print(g.serialize(destination="test.ttl"))


create_dataset(10000)
