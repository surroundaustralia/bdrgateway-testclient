from typing import Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID

from client._TERN import TERN
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset
from client.model.value import Value


# attribute list (http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924) TODO: Make attribute list
class Attribute(Klass):
    def __init__(
        self,
            attribute: URIRef,
            has_simple_value: str or URIRef,
            has_value: Value,    # in the tern this says its a class but am unsure how to execute properly TODO: Confirm Value.py is correct
            in_dataset: RDFDataset,
            iri: Optional[str] = None
    ):
        assert (
            len(attribute) >= 1
        ), "You must supply exactly 1 attributes"

        assert (
            len(has_simple_value) >= 1
        ), "You must supply a exactly 1 attributes"

        assert (
            type(has_value) == Value
        ), "The object supplied for the property has_value must be of type Value"

        assert (
            type(in_dataset) == RDFDataset
        ), "The object supplied for the property in_dataset must be of type RDFDataset"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/attribute/{self.id}")

        self.iri = URIRef(iri)
        super().__init__(iri)

        self.label = f"Attribute with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
        self.attribute = attribute
        self.has_simple_value = has_simple_value
        self.has_value = has_value
        self.in_dataset = in_dataset

    def to_graph(self) -> Graph:
        g = super().to_graph()
        # removing Klass.py graph structures
        g.remove((self.iri, RDF.type, OWL.Class))
        g.remove((self.iri, RDFS.label, None))
        # overwriting/adding the klass.py

        g.add((self.iri, RDF.type, TERN.Attribute))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.Attribute, self.attribute))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        g.add((self.iri, TERN.hasSimpleValue, self.has_simple_value))

        # unsure how to complete the one below Please fix when you can!
        g.add((self.iri, TERN.hasValue, self.has_value.iri))

        return g
