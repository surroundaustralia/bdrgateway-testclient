from typing import Optional, List

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, DCTERMS, XSD

from client.model._TERN import TERN
from client.model.klass import Klass
from client.model.agent import Agent
from client.model.concept import Concept
import re


class RDFDataset(Klass):
    def __init__(
        self,
        iri: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        subjects: List[Concept] = None,
        creator: Optional[Agent] = None,
        publisher: Optional[Agent] = None,
        contributors: Optional[List[Agent]] = None,
        modified: Optional[str] = None,
        created: Optional[str] = None,
        issued: Optional[str] = None,
    ):
        if title is not None:
            assert isinstance(title.__class__, str.__class__), \
                "If you provide a value for the title parameter, it must be of type string"

        if description is not None:
            assert isinstance(description.__class__, str.__class__), \
                "If you provide a value for the description parameter, it must be of type string"

        if subjects is not None:
            for subject in subjects:
                assert isinstance(subject.__class__, Concept.__class__), \
                    "If supplied, each subject must be of type Concept"

        if creator is not None:
            assert isinstance(creator.__class__, Agent.__class__), "If supplied a creator must be of type Agent"

        if contributors is not None:
            for contributor in contributors:
                assert isinstance(contributor.__class__, Agent.__class__), \
                    "If supplied, each contributor must be of type Agent"

        if publisher is not None:
            assert isinstance(publisher.__class__, Agent.__class__), "If supplied a publisher must be of type Agent"

        date_pattern = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
        
        if created is not None:
            assert isinstance(created.__class__, str.__class__), \
                "If you provide a value for the created parameter, it must be of type string"
            assert date_pattern.match(created), "The value for created you provided is not in the YYYY-MM-DD format"
            
        if modified is not None:
            assert isinstance(modified.__class__, str.__class__), \
                "If you provide a value for the modified parameter, it must be of type string"            
            assert date_pattern.match(modified), "The value for modified you provided is not in the YYYY-MM-DD format"
            
        if issued is not None:
            assert isinstance(issued.__class__, str.__class__), \
                "If you provide a value for the issued parameter, it must be of type string"
            assert date_pattern.match(issued), "The value for issued you provided is not in the YYYY-MM-DD format"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/sample/{self.id}")

        self.iri = URIRef(iri)

        super().__init__(iri)
        
        if title is not None:
            self.title = title
            self.label = title
        else:
            self.title = f"RDF Dataset with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"
            self.label = self.title

        if description is not None:
            self.description = description
        if subjects is not None:
            self.subjects = subjects
            
        if creator is not None:
            self.creator = creator
        if contributors is not None:
            self.contributors = contributors
        if publisher is not None:
            self.publisher = publisher
            
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if issued is not None:
            self.issued = issued

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.RDFDataset))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        if hasattr(self, "title"):
            g.add((self.iri, DCTERMS.title, Literal(self.title)))
            
        if hasattr(self, "description"):
            g.add((self.iri, DCTERMS.description, Literal(self.description)))

        if hasattr(self, "subjects"):
            for subject in self.subjects:
                g.add((self.iri, DCTERMS.creator, subject.iri))
                if (subject.iri, RDF.type, None) not in g:
                    g += subject.to_graph()

        if hasattr(self, "creator"):
            g.add((self.iri, DCTERMS.creator, self.creator.iri))
            if (self.creator.iri, RDF.type, None) not in g:
                g += self.creator.to_graph()

        if hasattr(self, "contributors"):
            for contributor in self.contributors:
                g.add((self.iri, DCTERMS.creator, contributor.iri))
                if (contributor.iri, RDF.type, None) not in g:
                    g += contributor.to_graph()

        if hasattr(self, "publisher"):
            g.add((self.iri, DCTERMS.publisher, self.publisher.iri))
            if (self.publisher.iri, RDF.type, None) not in g:
                g += self.publisher.to_graph()

        if hasattr(self, "created"):
            g.add((self.iri, DCTERMS.created, Literal(self.created, datatype=XSD.date)))
            
        if hasattr(self, "modified"):
            g.add((self.iri, DCTERMS.modified, Literal(self.modified, datatype=XSD.date)))

        if hasattr(self, "issued"):
            g.add((self.iri, DCTERMS.issued, Literal(self.issued, datatype=XSD.date)))
        
        return g
