import argparse
import random
import string
from typing import Literal as Lit

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import DCTERMS, RDF, SOSA, VOID, XSD

from _TERN import TERN

BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")

# randomised points in WA
GEOMETRY_DICT = {
    "CF": "POINT (-33.463985, 116.195552)",
    "MSF": "POINT (-33.458375, 116.118227)",
    "WF": "POINT (-33.351726, 116.030816)",
    "HRSF": "POINT (-33.289922, 116.094693)",
    "ACF": "POINT (-33.455571, 116.245981)",
    "TW": "POINT (-33.629302, 116.511577)",
    "OV": "POINT (-33.947830, 116.827601)",
    "W": "POINT (-33.177438, 116.720018)",
    "RW": "POINT (-32.836297, 116.948632)",
}

# Note this isn't complete attribute list
ATTRIBUTE_LIST = [
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/dbff3449-2ec9-4722-a953-87c78da86f74"
    ),  # bioregion
    URIRef(
        "https://linkeddata.tern.org.au/viewer/tern/id/http://linked.data.gov.au/def/tern-cv/335a84cd-01af-49cb-8532-acf71dc1d980"
    ),  # comment on community extent
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/e5953626-5c62-4baa-b8e5-36a7e6660611"
    ),  # comment on distance to infrastructure
    URIRef(
        "https://linkeddata.tern.org.au/viewer/tern/id/http://linked.data.gov.au/def/tern-cv/5acbfe4f-19e0-456c-89db-961013e6cd7c"
    ),  # date identified
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/e926b2ca-2688-486c-aa28-435f91c3c110"
    ),  # distance to nearest human infrastructure
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/76806e0f-61a2-447c-8177-7e666637e23a"
    ),  # elevation of site
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924"
    ),  # growth form
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/45a86abc-43c7-4a30-ac73-fc8d62538140"
    ),  # identification remarks
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/54e40f12-8c13-495a-9f8d-838d78faa5a7"
    ),  # identification uncertainty
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/2ad7e552-5bca-45cf-805a-10ba5a98862a"
    ),  # identified by
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/9b2ab960-da97-473a-81af-d50ab6041739"
    ),  # canopy sky
]

# Feature Types vocab http://linked.data.gov.au/def/tern-cv/68af3d25-c801-4089-afff-cf701e2bd61d
FEATURE_TYPES = [
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/05dac53a-269c-4699-9673-bf99a9406b14"
    ),
    # administrative_area
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/ecb855ed-50e1-4299-8491-861759ef40b7"
    ),
    # animal Individuals
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/2361dea8-598c-4b6f-a641-2b98ff199e9e"
    ),
    # animal occurence
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/8a68b4a9-167b-40f0-9222-293a2d20ffee"
    ),
    # animal population
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/cd5cbdbb-07d9-4a5b-9b11-5ab9d6015be6"
    ),
    # animal specimen
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/6d40d71e-58cd-4f75-8304-40c01fe5f74c"
    ),  # climate
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/45a73139-f6bf-47b7-88d4-4b2865755545"
    ),
    # fungal occurence
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/afc81cca-9122-4e36-823d-31dd765e9257"
    ),
    # Geologic substrate
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/2090cfd9-8b6b-497b-9512-497456a18b99"
    ),  # habitat
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/7e256d28-e686-4b6a-b64a-ac1b1a8f164d"
    ),
    # land surface disturbance
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/aef12cd6-3826-4988-a54c-8578d3fb4c8d"
    ),
    # land surface substrate
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/2cf3ed29-440e-4a50-9bbc-5aab30df9fcd"
    ),  # landform
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/80c39b95-0912-4267-bb66-2fa081683723"
    ),  # soil profile
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/06461021-a6c2-4175-9651-23653c2b9116"
    ),  # soil sample
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/d738a3f9-9b00-4adf-9dc8-0577269b691d"
    ),  # soil Specimen
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/60d7edf8-98c6-43e9-841c-e176c334d270"
    ),
    # plant individual
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/2e122e23-881c-43fa-a921-a8745f016ceb"
    ),
    # plant specimen
]

# Method Types vocab http://linked.data.gov.au/def/tern-cv/9b6e057f-271b-48f6-8c33-0528bf6b60df
METHOD_TYPES = [
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/40261295-d985-4739-a420-048093e4d3ac"
    ),  # HCL Droplets
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/80df57c3-be8a-4e6a-a730-34d31d01923c"
    ),  # densitometer
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/9f0624f0-86d2-41a5-9c43-b49fbff0abc7"
    ),  # dgps
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/f7b2bb78-8ca2-4437-b2b2-45a8c2456dfb"
    ),
    # Electricity conductivity meter
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/931d9940-f25c-43b0-980a-d235f4d8a4b0"
    ),  # PH meter
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/ae1a6ef6-c56f-441e-bb1b-ec87ae5f5c05"
    ),  # point intercept
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/7a28af9b-13b2-49c3-9b72-b94850a1c2b6"
    ),  # soil core
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/70e2c6e3-c699-4505-aeb0-4af2684f3bb2"
    ),  # soil pit
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/8fef9acb-e702-4b2c-8b79-3b22b00987da"
    ),
    # visual assessment
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/693aca27-8c3b-44c4-b535-78bc92b4142d"
    ),  # basal wedge
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/6226f002-84ff-457b-bd0c-712f131cf60a"
    ),
    # diameter measurement
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/d0c3ba01-ff35-40bd-8d0b-e9a222240ddf"
    ),  # diameter tape
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/5e097749-4293-49c5-8f53-c7c92e20ecc8"
    ),  # gridded data
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/591086c7-a52b-45cc-b506-3fa1bc0be7d8"
    ),
    # human measurement
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/ea1d6342-1901-4f88-8482-3111286ec157"
    ),
    # human observation
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/b11d2a42-9982-4e40-896c-df909f14839d"
    ),
    # instrument measurement
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/e9ce7cdb-cb2f-4d2e-8011-05b1669cfade"
    ),
    # munsell soil colour chart
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/3f9c834b-2188-4fad-871e-fcca0a406c21"
    ),
    # SOIL 10 CM SAMPLES
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/cfe311c1-c762-4b86-b59c-1ff216f077c5"
    ),
    # soil auger boring
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/21e03c11-719c-4298-a9a5-efd3d53a8fe8"
    ),
    # soil vertical exposure
    URIRef(
        "http://linked.data.gov.au/def/tern-cv/b6bbfc2d-97e1-4fee-b86b-c02594350c1b"
    ),
    # vertex hypsometer
]


MESSAGE_TYPES = ["create", "update", "delete", "exists"]


def validate_number(n):
    if n < 1 or n > 10000:
        print("The number of Samplings you select must be > 1, < 10,000")
        return False
    return True


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for x in range(y))


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
        samplings_data.append(
            {
                "foi": x[int(index / 50)],
                "time": "2022-01-03T12:13:14",
                "procedure": random.choice(
                    METHOD_TYPES
                ),  # "http://example.com/procedure/" +
                "result": {
                    "dataset": "fake",
                    "feature_type": random.choice(FEATURE_TYPES),
                },
            }
        )
        # can consider the geometry but will see after
    return samplings_data


def create_dataset(n: int, msg_type: Lit["create", "update", "delete", "exists"]):
    if not validate_number(n):
        raise ValueError("%s is not >= 1" % n)

    if msg_type not in MESSAGE_TYPES:
        raise ValueError(f"msg_type must be one of {', '.join(MESSAGE_TYPES)}")

    # Prefix and base URI creation
    g = Graph(base="https://linked.data.gov.au/dataset/bdr/")
    g.bind("bdrm", BDRM)
    g.bind("dcterms", DCTERMS)
    g.bind("geo", GEO)
    g.bind("sosa", SOSA)
    g.bind("tern", TERN)
    g.bind("void", VOID)

    # BDR Message
    msg_iris = {
        "create": BDRM.CreateMessage,
        "update": BDRM.UpdateMessage,
        "delete": BDRM.DeleteMessage,
        "exists": BDRM.ExistsMessage,
    }
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
        foi = URIRef(
            "https://linked.data.gov.au/dataset/bdr/site/"
            + samplings_data[index]["foi"]
        )
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
        g.add(
            (msg_iri, DCTERMS.hasPart, sampling_iri)
        )  # link Sampling to CreateMessage

        foi_iri = URIRef(
            "https://linked.data.gov.au/dataset/bdr/site/" + sampling["foi"]
        )
        g.add((sampling_iri, RDF.type, TERN.Sampling))
        g.add((sampling_iri, SOSA.hasFeatureOfInterest, foi_iri))
        g.add(
            (
                sampling_iri,
                SOSA.resultTime,
                Literal(sampling["time"], datatype=XSD.dateTime),
            )
        )
        g.add((sampling_iri, SOSA.usedProcedure, URIRef(sampling["procedure"])))

        createme_id_max += 1
        sample_iri = URIRef("http://createme.org/" + str(createme_id_max))
        dataset_iri = URIRef(
            "https://linked.data.gov.au/dataset/bdr/dataset/"
            + sampling["result"]["dataset"]
        )
        g.add((sample_iri, RDF.type, TERN.Sample))
        g.add((sample_iri, SOSA.isResultOf, sampling_iri))
        g.add((sample_iri, SOSA.isSampleOf, foi_iri))
        g.add((sample_iri, VOID.inDataset, dataset_iri))
        g.add(
            (sample_iri, TERN.featureType, URIRef(sampling["result"]["feature_type"]))
        )

        # link Sample to Sampling
        g.add((sampling_iri, SOSA.hasResult, sample_iri))

    return g.serialize()


def main():
    parser = argparse.ArgumentParser()

    def check_positive_one(value):
        ivalue = int(value)
        if ivalue <= 1:
            raise argparse.ArgumentTypeError("%s is not >= 1" % value)
        return ivalue

    parser.add_argument(
        "num",
        help="The number of Samplings you want to synthesise data for",
        type=check_positive_one,
    )

    parser.add_argument(
        "msg_type",
        help="The type of message to wrap the data in",
        choices=MESSAGE_TYPES,
    )

    args = parser.parse_args()

    print(create_dataset(args.num, args.msg_type))


if __name__ == "__main__":
    # main()
    create_dataset(2, "nick")
