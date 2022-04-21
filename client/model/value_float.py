from typing import Optional, Union

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

from client.model._TERN import TERN
from client.model.value import Value


class Float(Value):
    def __init__(self, value: Union[int, float], unit: Optional[URIRef] = None):
        assert isinstance(value.__class__, int.__class__) or isinstance(
            value.__class__, float.__class__
        ), "You must supply an integer or a float for the value input parameter"

        if unit is not None:
            assert (
                type(unit) == URIRef
            ), "If you supply a value for the input parameter unit, it must ne a URIRef"

        super().__init__()

        self.value = Literal(value, datatype=XSD.double)
        self.unit = unit

    def to_graph(self) -> Graph:
        g = super().to_graph()
        # g.remove((self.iri, RDF.type, TERN.Value))
        g.add((self.iri, RDF.type, TERN.Float))
        g.remove((self.iri, RDFS.label, None))
        # no label

        g.add((self.iri, RDF.value, self.value))
        if self.unit is not None:
            g.add((self.iri, TERN.unit, self.unit))

        return g
