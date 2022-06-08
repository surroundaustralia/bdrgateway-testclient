from typing import Optional, List
from typing import Literal as Lit

from client.model.klass import Klass

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SDO, XSD

AGENT_TYPES = Lit["person", "organisation"]


class Agent(Klass):
    def __init__(
        self,
        agent_type: AGENT_TYPES,
        iri: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        organisation_url: Optional[str] = None,
    ):
        assert agent_type in ["person", "organisation"], \
            f"You must select one of the valid agent types for agent_type. Choose from: {', '.join(AGENT_TYPES)}"

        if name is not None:
            assert isinstance(name.__class__, str.__class__), \
                "If you provide a value for the name parameter, it must be of type string"

        self.agent_type = agent_type

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/agent/{self.id}")

        self.iri = URIRef(iri)

        super().__init__(iri)
        if email is not None:
            self.email = email
        else:
            self.email = f"http://example.com/{self.make_uuid()}"

        if organisation_url is not None:
            self.organisation_url = organisation_url
        else:
            self.organisation_url = f"http://example.com/{self.make_uuid()}"

        if name is not None:
            self.name = name
            self.label = self.name
        else:
            self.name = f"Agent with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
            self.label = self.name

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        if self.agent_type == "person":
            g.add((self.iri, RDF.type, SDO.Person))
        elif self.agent_type == "organisation":
            g.add((self.iri, RDF.type, SDO.Organization))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, SDO.name, Literal(self.label)))
        if self.email:
            g.add((self.iri, SDO.email, Literal(self.email, datatype=XSD.anyURI)))
        if self.organisation_url:
            g.add((self.iri, SDO.url, Literal(self.organisation_url, datatype=XSD.anyURI)))

        return g