import math, random, time
from typing import List, Optional
from typing import Literal as Lit
from uuid import uuid4

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import DCTERMS, SOSA, VOID, XSD, OWL, RDF, RDFS, TIME, PROV, SDO
from shapely.geometry import Polygon, Point
from shapely.geometry import box

try:
    from client.model._TERN import TERN
    from client.model import *
except:
    import sys
    from pathlib import Path

    p = Path(__file__).parent.parent.resolve()
    sys.path.append(str(p))
    from client.model._TERN import TERN
    from client.model import *

BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")

MESSAGE_TYPES = ["create", "update", "delete", "exists"]
ANIMAL_CONCEPT = Concept(
    "http://linked.data.gov.au/def/tern-cv/2361dea8-598c-4b6f-a641-2b98ff199e9e"
)
ANIMAL_POPULATION_CONCEPT = Concept(
    "http://linked.data.gov.au/def/tern-cv/cd5cbdbb-07d9-4a5b-9b11-5ab9d6015be6"
)

SCIENTIFIC_NAME_IDS = [
    URIRef("https://fake-scientific-name-id.com/name/afd/001"),
    URIRef("https://fake-scientific-name-id.com/name/afd/002"),
    URIRef("https://fake-scientific-name-id.com/name/afd/003"),
    URIRef("https://fake-scientific-name-id.com/name/afd/004"),
    URIRef("https://fake-scientific-name-id.com/name/afd/005"),
    URIRef("https://fake-scientific-name-id.com/name/afd/006"),
    URIRef("https://fake-scientific-name-id.com/name/afd/007"),
    URIRef("https://fake-scientific-name-id.com/name/afd/008"),
    URIRef("https://fake-scientific-name-id.com/name/afd/009"),
    URIRef("https://fake-scientific-name-id.com/name/afd/010"),
]

NSL_REAL_VALUES = [
    URIRef("https://id.biodiversity.org.au/tree/aal"),
    URIRef("https://id.biodiversity.org.au/tree/abl"),
    URIRef("https://id.biodiversity.org.au/tree/afd"),
    URIRef("https://id.biodiversity.org.au/tree/afl"),
    URIRef("https://id.biodiversity.org.au/tree/all"),
    URIRef("https://id.biodiversity.org.au/tree/apc"),
]


class TernSynthesizerNonUUIDLabels:
    datasets: List[RDFDataset]
    fois = List[FeatureOfInterest]
    sites = List[Site]
    samplings = List[Sampling]
    samples = List[Sample]
    observations = List[Observation]
    taxa = List[Taxon]
    coordinate_bounding_box: Polygon
    coordinate_points = List[Point]
    site_visit = List[SiteVisit]

    def __init__(
            self, n: int,
            coordinate_bounding_box: Polygon,
            randomised_or_regular: Optional[Lit["randomised", "regular"]] = "randomised"
    ):
        init_total_st = time.time()
        assert n > 0, "n, the number of Samples, must be greater than zero"

        assert randomised_or_regular in ["randomised", "regular"], \
            "The value for randomised_or_regular mut be either 'randomised', or 'regular'"

        self.datasets = []
        self.fois = []
        self.sites = []
        self.samplings = []
        self.samples = []
        self.observations = []
        self.taxa = []
        self.attributes = []
        self.site_visits = []
        self.coordinate_bounding_box = coordinate_bounding_box
        self.coordinate_points = self._generate_coordinate_points(
            n,
            self.coordinate_bounding_box,
            randomised_or_regular
        )

        # create a list of RDFDataset instances
        rdf_st = time.time()
        for i in range(math.floor(n / 100) + 1):  # 1 per 100 Samplings
            self.datasets.append(RDFDataset())
        rdf_et = time.time()

        foi_st = time.time()
        # create a list of FoI instances: 1 per 50 Samplings
        for i in range(math.floor(n / 50) + 1):
            self.fois.append(
                FeatureOfInterest(Concept(random.choice(FEATURE_TYPES)), self.datasets[math.floor(i / 2)])
            )
        foi_et = time.time()

        site_st = time.time()
        # create a list of Site instances: 1 per 25 Samplings
        for i in range(math.floor(n / 25) + 1):
            this_site_dataset = random.choice(self.datasets)
            this_site_foi = random.choice(self.fois)
            self.sites.append(
                Site(
                    Observation(
                        this_site_dataset,
                        Value(),
                        this_site_foi,
                        Literal("Site establishment"),
                        URIRef("http://linked.data.gov.au/def/tern-cv/889dfc31-5b1c-48c0-8bc7-e12f13d63891"),  # site id
                        URIRef(f"http://example.com/instant/{uuid4()}"),
                        Literal("2000-01-01", datatype=XSD.date),
                        URIRef(random.choice(METHOD_TYPES))
                    ),
                    [this_site_foi],
                    this_site_dataset,
                    Concept("http://linked.data.gov.au/def/tern-cv/e1c7c434-1321-4601-9079-e837b7ffc293")  # site
                )
            )
        site_et = time.time()

        site_visit_st = time.time()
        # create a list of SiteVisits instances: 1 per 12 Samplings
        for i in range(math.floor(n / 12) + 1):
            self.site_visits.append(
                SiteVisit(
                    random.choice(self.datasets),
                    Literal("2000-01-01T10:00:00", datatype=XSD.dateTime))
            )
        site_visit_et = time.time()

        sampling_st = time.time()
        # create Samplings
        for i in range(n):
            self.datasets[math.floor(n / 100)].creator = Agent("person")
            self.datasets[math.floor(n / 100)].publisher = Agent("organisation")

            this_foi = self.fois[math.floor(i / 50)]
            this_sni = random.choice(NSL_REAL_VALUES)
            if (
                    random.random() < 0.667
            ):  # 2/3 of Samplings have Samples with Observations with Taxa
                this_concept = ANIMAL_CONCEPT
                this_simple_result = Literal(f"Species {this_sni.split('/')[1]}")
                this_result = Taxon(scientific_name_id=this_sni)
                this_observed_property = URIRef(
                    "http://linked.data.gov.au/def/tern-cv/70646576-6dc7-4bc5-a9d8-c4c366850df0"
                )  # Taxon
            else:  # 1/3 of Samplings have Observations with some numerical count, not Taxa
                this_concept = ANIMAL_POPULATION_CONCEPT
                this_simple_result = Literal(f"Count {this_sni.split('/')[1]}")
                this_result = Float(random.randint(0, 1000))
                this_observed_property = URIRef(
                    "http://linked.data.gov.au/def/tern-cv/2023575a-f0f9-40cc-b211-febbb652da22"
                )  # basal area count
                this_attribute = Attribute(
                    URIRef(random.choice(ATTRIBUTE_TYPES)),
                    Literal(42),
                    Value(True),
                    this_result,
                    self.datasets[math.floor(n / 100)],
                )
                self.attributes.append(this_attribute)
            this_sample = Sample(
                [this_foi], this_concept, self.datasets[math.floor(1 / 100)], None
            )
            this_sampling = Sampling(
                self.datasets[math.floor(1 / 100)],
                this_foi,
                Literal("2000-01-01", datatype=XSD.date),
                URIRef(random.choice(METHOD_TYPES)),
                [this_sample],
                geometry=self.coordinate_points[i]
            )
            this_sample.is_result_of = this_sampling
            # linking the foi to the sample
            this_foi.has_sample = this_sample

            this_obs = Observation(
                self.datasets[math.floor(n / 100)],
                this_result,
                this_sample if this_observed_property == URIRef(
                    "http://linked.data.gov.au/def/tern-cv/70646576-6dc7-4bc5-a9d8-c4c366850df0") else this_foi,
                this_simple_result,
                this_observed_property,
                URIRef(f"http://example.com/instant/{uuid4()}"),
                Literal("2000-01-01", datatype=XSD.date),
                URIRef(random.choice(METHOD_TYPES)),
            )
            site1 = random.choice(self.sites)
            this_sampling.has_site_visit = site1

            # creating site visit and links
            sv1 = random.choice(self.site_visits)
            this_sampling.has_site_visit = sv1
            this_obs.has_site_visit = sv1
            site1.has_site_visit = sv1

            self.sites.append(site1)
            self.samplings.append(this_sampling)
            self.observations.append(this_obs)
        sampling_et = time.time()

        rdf_time = rdf_et - rdf_st
        foi_time = foi_et - foi_st
        site_time = site_et - site_st
        site_visit_time = site_visit_et - site_visit_st
        sampling_time = sampling_et - sampling_st

        init_total_et = time.time()
        init_elapsed_time = init_total_et - init_total_st
        print(f"Individual \n"
              f"_____________________________________________\n"
              f"Init function elapsed time: {init_elapsed_time} \n"
              f"Dataset elapsed time: {rdf_time} \n"
              f"FOI elapsed time: {foi_time} \n"
              f"Site elapsed time: {site_time} \n"
              f"SiteVisit elapsed time: {site_visit_time} \n"
              f"Sampling elapsed time: {sampling_time} \n")

    def _bind_prefixes(self, g: Graph):
        g.bind("bdrm", BDRM)
        g.bind("dcterms", DCTERMS)
        g.bind("dwc", DWC)
        g.bind("geo", GEO)
        g.bind("sosa", SOSA)
        g.bind("tern", TERN)
        g.bind("void", VOID)
        g.bind("owl", OWL)
        g.bind("time", TIME)
        g.bind("prov", PROV)
        g.bind("xmlns", SDO)


    def _generate_coordinate_points(
            self,
            no_of_points: int,
            bounding_box: Polygon,
            randomised_or_regular: Lit["randomised", "regular"] = "randomised"
    ) -> List[Point]:
        # buffer area by 0.01
        min_long = bounding_box.exterior.coords[2][0] + 0.01
        max_long = bounding_box.exterior.coords[0][0] - 0.01
        min_lat = bounding_box.exterior.coords[0][1] + 0.01
        max_lat = bounding_box.exterior.coords[2][1] - 0.01

        sqt = math.ceil(math.sqrt(no_of_points))

        coords = []

        if randomised_or_regular == "randomised":
            for x in range(sqt):
                for y in range(sqt):
                    x_rand = random.random()
                    y_rand = random.random()
                    coords.append(
                        Point(
                            round(((max_long - min_long) * x_rand) + min_long, 3),
                            round(((max_lat - min_lat) * y_rand) + min_lat, 3)
                        )
                    )
        else:  # "regular"
            long_step = ((max_long - min_long) / sqt)
            lat_step = ((max_lat - min_lat) / sqt)

            for x in range(sqt):
                x_long = round(min_long + x * long_step, 3)
                for y in range(sqt):
                    y_lat = round(min_lat + y * lat_step, 3)
                    coords.append(Point(x_long, y_lat))

        return coords

    def to_graph(self):
        graph_st = time.time()
        g = Graph()
        self._bind_prefixes(g)
        print("Bound Prefixes\n")
        samp_timings = time.time()
        print(f"Began Samplings to graph. There are {len(self.samplings)} samplings")
        for s in self.samplings:
            g += s.to_graph()
        print(f"Finished the samplings tograph in {time.time() - samp_timings}........ 1/4 Complete\n")
        obs_timings = time.time()
        print(f"Began Observations to graph. There are {len(self.observations)} observations")
        for o in self.observations:
            g += o.to_graph()
        print(f"Finished observations tograph in {time.time() - obs_timings}......... 2/4 Complete\n")
        att_timings = time.time()
        print(f"Began Attributes to graph. THere are {len(self.attributes)} attributes")
        for o in self.attributes:
            g += o.to_graph()
        print(f"Finished attributes tograph in {time.time() - att_timings}.......... 3/4 Complete\n")
        sites_timings = time.time()
        print(f"Began sites to graph. There are {len(self.sites)} sites")
        for s in self.sites:
            g += s.to_graph()
        print(f"Finished sites tograph in {time.time() - sites_timings}............ 4/4 Complete\n")
        # Ontology adding
        print("Note the ontology for this dataset is: https://linked.data.gov.au/dataset/bdr/generated_"
              "dataset/23_mil_samplings_1_bil_triples")
        g.add((URIRef("https://linked.data.gov.au/dataset/bdr/generated_dataset/23_mil_samplings_1_bil_triples"),
               RDF.type,
               OWL.Ontology))
        g.add((URIRef("https://linked.data.gov.au/dataset/bdr/generated_dataset/23_mil_samplings_1_bil_triples"),
               RDFS.comment,
               Literal("Generated Scale Testing Dataset With 1 billion triples")))
        g.add((URIRef("https://linked.data.gov.au/dataset/bdr/generated_dataset/23_mil_samplings_1_bil_triples"),
               RDFS.label,
               Literal("Generated Scale Testing Dataset With 1 billion triples")))
        graph_et = time.time()
        print(f"to_graph fx elapsed time {graph_et - graph_st}")
        print("\n _______________________________________________________________________ \n")
        return g


if __name__ == '__main__':
    g = TernSynthesizerNonUUIDLabels(23000000, box(115.992191, -33.871399, 121.9467547, -28.572837)).to_graph()
    serialize_st = time.time()
    g.serialize(destination="23_mil_samplings_1_bil_triples.nt", format="nt", encoding="utf-8")
    print(f"serialize fx completed, it took {time.time() - serialize_st}")
    print("Final files completed!")
    # for i in [10, 20, 30, 40]:
    #     print(i)
    # 100 samplings should have assertion (random) with abisdm:conservationstatussupplied cstatus:p2,
    # these 100 and then another 100 on top of that should also have
    # "Pseudohydryphantes doegi" ;   dwc:scientificNameID <https://test-idafd.biodiversity.org.au/name/afd/70433252>

    # another 100 should have dwc:scientificNameID <https://test-idafd.biodiversity.org.au/name/afd/70404974> ;
    # Nedsia sp

    # essentially a 300 datapoints with 200 protected species, 100 non-protected.
    # of the protected species, half being with the conservation status flag, half without

    # 120 billion triples timing -> 260k samplings
    # Init function elapsed time: 37.18876791000366
    # Dataset elapsed time: 0.01701521873474121
    # FOI elapsed time: 0.0790717601776123
    # Site elapsed time: 0.6050221920013428
    # SiteVisit elapsed time: 0.5637328624725342
    # Sampling elapsed time: 34.49554467201233


