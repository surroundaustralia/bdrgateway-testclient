from typing import Optional, Union

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, VOID

from client.model._TERN import TERN
from client.model.klass import Klass
from client.model.rdf_dataset import RDFDataset
from client.model.value_float import Float
from client.model.value_taxon import Taxon
from client.model.value import Value


# attribute list (http://linked.data.gov.au/def/tern-cv/dd085299-ae86-4371-ae15-61dfa432f924) TODO: Make attribute list
class Attribute(Klass):
    def __init__(
        self,
        attribute: URIRef,
        has_simple_value: Union[Literal, URIRef],
        has_value: Value,
        is_attribute_of: Union[Float, Taxon, Value],
        in_dataset: RDFDataset,
        iri: Optional[str] = None,
    ):
        assert isinstance(attribute.__class__, URIRef.__class__) >= 1, "You must supply exactly 1 attributes"

        assert len(has_simple_value) >= 1, "You must supply a exactly 1 attributes"

        assert (
            isinstance(has_value.__class__, Value.__class__)
        ), "The object supplied for the property has_value must be of type Value"

        assert (
            isinstance(is_attribute_of.__class__, (Float.__class__, Taxon.__class__, Value.__class__))
        ), "The object supplied for the property is_attribute_of must be of type Float, Taxon or Value"

        assert (
            isinstance(in_dataset.__class__, RDFDataset.__class__)
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
        self.is_attribute_of = is_attribute_of
        self.in_dataset = in_dataset

    def to_graph(self) -> Graph:
        g = super().to_graph()
        # removing Klass.py graph structures
        g.remove((self.iri, RDF.type, OWL.Class))
        g.remove((self.iri, RDFS.label, None))
        # overwriting/adding the klass.py

        g.add((self.iri, RDF.type, TERN.Attribute))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.attribute, self.attribute))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        g.add((self.iri, TERN.hasSimpleValue, self.has_simple_value))
        if (self.has_value.iri, RDF.type, None) not in g:
            g += self.has_value.to_graph()
        g.add((self.iri, TERN.isAttributeOf, self.is_attribute_of.iri))
        if (self.is_attribute_of.iri, RDF.type, None) not in g:
            g += self.is_attribute_of.to_graph()
        g.add((self.iri, TERN.hasValue, self.has_value.iri))

        return g
