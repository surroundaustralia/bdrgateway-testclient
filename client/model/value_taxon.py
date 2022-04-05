from typing import Optional
from uuid import uuid4

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL

from client._TERN import TERN
from client.model.value import Value

DWC = Namespace("http://rs.tdwg.org/dwc/terms/")


class Taxon(Value):
    def __init__(
        self,
        scientific_name_id: URIRef,
        is_blank_node: Optional[bool] = True,
        iri: Optional[str] = None,
        scientific_name: Optional[Literal] = None
    ):
        assert type(scientific_name_id) == URIRef, "You must supply a URIRef for the property scientific_name_id"

        if scientific_name is not None:
            assert type(scientific_name) == Literal, \
                "If you provide a value for scientific_name, it must be an RDFLib Literal "

        super().__init__(is_blank_node, iri)

        self.scientific_name_id = scientific_name_id
        self.scientific_name = scientific_name

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, TERN.Value))
        g.add((self.iri, RDF.type, TERN.Taxon))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        g.add((self.iri, DWC.scientificNameID, self.scientific_name_id))
        if self.scientific_name is not None:
            g.add((self.iri, DWC.scientificName, self.scientific_name))

        return g
