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
FEATURE_TYPES = ["administrative_area", "animal_individual", "animal_occurrence",
                 "animal_population", "animal_specimen", "climate", "fungal_occurrence",
                 "geologic_substrate", "habitat", "land_surface_substrate", "landform",
                 "soil_profile", "soil_sample", "soil_specimen", "individual_stem",
                 "plant_specimen", "vegetation_stand", "plant_community", "plant_litter",
                 "plant_occurrence", "plant_population", "vegetation_disturbance",
                 "vegetation_fuel", "plant_taxa_per_stratum"]
METHOD_TYPES = ["HCL_droplets_1_ML", "densitometer", "dgps",
                "electrical_conductivity_meter", "ph_meter", "point_intercept",
                "soil_core", "soil_pit", "visual_assessment", "basal_wedge",
                "diameter_measurement_instrument", "diameter_tape",
                "human_measurement", "human_observation", "instrument_measurement",
                "munsell_soil_colour_chart", "soil_10_cm_samples",
                "soil_auger_boring", "soil_vertical_exposure", "vertex_hypsometer"]


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
        g.add((foi, TERN.featureType, Literal(random.choice(FEATURE_TYPES))))

        # I NEED TO COME BACK TO THIS PROBLEM -> integrating fois into ds
        # can probs do some mathematical formula for this.
        #  0 - 200 -> dataset 1, 200 - 400, dataset 2, 400-600, dataset 3 ...
        # 0 - 50 -> foi 1, 50 - 100 -> foi 2 ....
        # every 4 fois swtich up
        # 1 - 4 -> d1, 5-8 -> d2 etc
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

    print(g.serialize())


create_dataset(2)
