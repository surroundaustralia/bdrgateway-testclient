import math
import random
from typing import Literal as Lit

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD
from shapely.geometry import box

from model.agent import Agent
from model.concept import Concept
from model.rdf_dataset import RDFDataset
from synthesizer_tern import TernSynthesizer

ABISDM = Namespace("https://linked.data.gov.au/def/abisdm/")

class AbisSynthesizer:
    def __init__(
            self,
            abis_additions: Lit["embargoed_datasets", "conservation_statues", "ed_and_cs"]
    ):
        if abis_additions == "embargoed_datasets":
            self.graph = Graph()
            titles = [
                "Dataset Title 01",
                "Dataset Title 02",
                "Dataset Title 03",
                "Dataset Title 04",
                "Dataset Title 05",
                "Dataset Title 06",
                "Dataset Title 07",
                "Dataset Title 08",
                "Dataset Title 09",
                "Dataset Title 10",
                "Dataset Title 11",
                "Dataset Title 12",
                "Dataset Title 13",
                "Dataset Title 14",
                "Dataset Title 15",
                "Dataset Title 16",
                "Dataset Title 17",
                "Dataset Title 18",
                "Dataset Title 19",
                "Dataset Title 20",
                "Dataset Title 21",
                "Dataset Title 22",
                "Dataset Title 23",
                "Dataset Title 24",
                "Dataset Title 25",
            ]
            descriptions = [
                "Dataset Description 01",
                "Dataset Description 02",
                "Dataset Description 03",
                "Dataset Description 04",
                "Dataset Description 05",
                "Dataset Description 06",
                "Dataset Description 07",
                "Dataset Description 08",
                "Dataset Description 09",
                "Dataset Description 10",
                "Dataset Description 11",
                "Dataset Description 12",
                "Dataset Description 13",
                "Dataset Description 14",
                "Dataset Description 15",
                "Dataset Description 16",
                "Dataset Description 17",
                "Dataset Description 18",
                "Dataset Description 19",
                "Dataset Description 20",
                "Dataset Description 21",
                "Dataset Description 22",
                "Dataset Description 23",
                "Dataset Description 24",
                "Dataset Description 25",
            ]

            def _make_subjects():
                subject_choices_01 = [
                    Concept(pref_label="flora"),
                    Concept(pref_label="fauna"),
                ]
                subject_choices_01_flora = [
                    Concept(pref_label="orchid"),
                    Concept(pref_label="non-orchid"),
                    Concept(pref_label="eucalyptus"),
                ]
                subject_choices_01_fauna = [
                    Concept(pref_label="invertebrate"),
                    Concept(pref_label="marsupial"),
                    Concept(pref_label="bird"),
                ]
                subject_choices_03 = [
                    Concept(pref_label="WA"),
                    Concept(pref_label="Australia"),
                ]
                s1 = random.choice(subject_choices_01)
                if s1.pref_label == "flora":
                    s2 = random.choice(subject_choices_01_flora)
                else:
                    s2 = random.choice(subject_choices_01_fauna)
                s3 = random.choice(subject_choices_03)

                return [s1, s2, s3]

            wa_bio_agent = Agent(agent_type="organisation", name="Consultant X")
            creators = [
                wa_bio_agent,
                Agent(agent_type="organisation", name="Consultant X"),
                Agent(agent_type="organisation", name="Consultant Y"),
            ]
            publishers = [
                wa_bio_agent,
            ]
            # make 20 datasets, embargo several of them
            for i in range(20):
                dataset_iri = f"http://example.com/dataset/{str(i+1).zfill(2)}"
                # Create a TERN Dataset
                d = RDFDataset(
                    dataset_iri,
                    titles[i],
                    descriptions[i],
                    _make_subjects(),
                    creator=random.choice(creators),
                    publisher=random.choice(publishers),
                    created=f"2022-01-{str(i+1).zfill(2)}"
                )
                # Create ABIS properties for the Dataset
                dataset_graph = d.to_graph()
                r = random.random()
                if r >= 0.75:
                    dataset_graph.add((
                        URIRef(dataset_iri),
                        ABISDM.embargoEndDate,
                        Literal(f"2022-10-{str(i+1).zfill(2)}", datatype=XSD.date)
                    ))
                elif r >= 0.5:
                    dataset_graph.add((
                        URIRef(dataset_iri),
                        ABISDM.embargoPeriod,
                        Literal(f"P{i}M", datatype=XSD.duration)
                    ))
                else:
                    # add no embargoed properties
                    pass

                # create TERN data for the Dataset
                x = math.floor(i / 4) + 1
                y = math.floor(i / 5) + 1
                tern_graph = TernSynthesizer(10, box(116 + x, -32 + y, 116 + x + 1, -28 + y + 1), "randomised").to_graph()
                u = """
                    DELETE {
                        ?d a tern:RDFDataset .
                        ?x ?y ?d .
                    }
                    INSERT {
                        <xx> a tern:RDFDataset .
                        ?x ?y <xx> .                    
                    }
                    WHERE {
                        ?d a tern:RDFDataset .
                        ?x ?y ?d .                    
                    }                     
                """.replace("xx", dataset_iri)
                tern_graph.update(u)
                tern_graph += dataset_graph

                self.graph += tern_graph

    def to_graph(self):
        self.graph.bind("tern", Namespace("https://w3id.org/tern/ontologies/tern/"))
        self.graph.bind("geo", Namespace("http://www.opengis.net/ont/geosparql#"))
        self.graph.bind("dwc", Namespace("http://rs.tdwg.org/dwc/terms/"))
        self.graph.bind("abisdm", ABISDM)

        return self.graph
