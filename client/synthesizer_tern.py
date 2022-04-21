import math
import random
from typing import List, Optional
from typing import Literal as Lit
from uuid import uuid4

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import DCTERMS, SOSA, VOID, XSD
from shapely.geometry import Polygon, Point

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


class TernSynthesizer:
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
        self.site_visit = []
        self.coordinate_bounding_box = coordinate_bounding_box
        self.coordinate_points = self._generate_coordinate_points(
            n,
            self.coordinate_bounding_box,
            randomised_or_regular
        )

        # create a list of RDFDataset instances
        for i in range(math.floor(n / 100) + 1):  # 1 per 100 Samplings
            self.datasets.append(RDFDataset())

        # create a list of FoI instances: 1 per 50 Samplings
        for i in range(math.floor(n / 50) + 1):
            self.fois.append(
                FeatureOfInterest(Concept(random.choice(FEATURE_TYPES)), self.datasets[math.floor(i / 2)])
            )

        # create Samplings
        for i in range(n):
            this_foi = self.fois[math.floor(i / 50)]
            this_sni = random.choice(SCIENTIFIC_NAME_IDS)
            if (
                random.random() > 0.667
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
                this_foi,
                Literal("2000-01-01+09:00", datatype=XSD.dateTime),
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
                this_foi,
                this_simple_result,
                this_observed_property,
                URIRef(f"http://example.com/instant/{uuid4()}"),
                Literal("2000-01-01+09:00", datatype=XSD.dateTime),
                URIRef(random.choice(METHOD_TYPES)),
            )
            # Potential site
            site1 = Site(this_obs, [this_foi], self.datasets[math.floor(n / 100)], this_concept)
            this_sampling.has_site_visit = site1

            # creating site visit and links
            this_site_visit = SiteVisit(self.datasets[math.floor(1 / 100)],
                                        Literal("2000-01-01+09:00", datatype=XSD.dateTime))
            this_sampling.has_site_visit = this_site_visit
            this_obs.has_site_visit = this_site_visit
            site1.has_site_visit = this_site_visit

            self.site_visit.append(this_site_visit)
            self.sites.append(site1)
            self.samplings.append(this_sampling)
            self.observations.append(this_obs)

    def _bind_prefixes(self, g: Graph):
        g.bind("bdrm", BDRM)
        g.bind("dcterms", DCTERMS)
        g.bind("dwc", DWC)
        g.bind("geo", GEO)
        g.bind("sosa", SOSA)
        g.bind("tern", TERN)
        g.bind("void", VOID)

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
        g = Graph()
        self._bind_prefixes(g)
        for s in self.samplings:
            g += s.to_graph()
        for o in self.observations:
            g += o.to_graph()
        for o in self.attributes:
            g += o.to_graph()
        for s in self.sites:
            g += s.to_graph()
        for o in self.site_visit:
            g += o.to_graph()
        return g
