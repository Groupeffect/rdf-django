import os
from django.db import models
from django.conf import settings
from rdflib import (
    Graph, URIRef, Literal, 
    # namespaces:
    DC, PROV, RDF, FOAF,
)


class MetaModel(models.Model):
    label = models.CharField(max_length=100, default='no label')
    description = models.TextField(default='no desription')
    class Meta:
        abstract = True


class Organization(MetaModel):
    website = models.URLField(blank=True, null=True)
    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_ORGANIZATION_URL,str(self.id)))

    def get_rdf_representation(self, serialize: bool=True, format: str=settings.GLOBAL_GRAPH_IO_FORMAT):
            graph = Graph()
            uri = self.get_uri()
            graph.add((uri, RDF.type, PROV.Organization))
            graph.add((
                uri,
                FOAF.Organization,
                Literal(self.label)
            ))
            if self.website:
                graph.add((
                    uri,
                    FOAF.workInfoHomepage,
                    Literal(self.website)
                ))
            if serialize:
                return graph.serialize(format=format)
            return graph

    def __str__(self):
        return self.get_rdf_representation()

class Person(MetaModel):
    organizations = models.ManyToManyField(Organization, blank=True)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_PERSON_URL,str(self.id)))

    def get_rdf_representation(self, serialize: bool=True, format: str=settings.GLOBAL_GRAPH_IO_FORMAT):
        graph = Graph()
        uri = self.get_uri()
        graph.add((uri, RDF.type, PROV.Person))
        graph.add((
            uri,
            FOAF.Person,
            Literal(self.label)
        ))
        if self.firstName:
            graph.add((
                uri,
                FOAF.firstName,
                Literal(self.firstName)
            ))
        if self.lastName:
            graph.add((
                uri,
                FOAF.lastName,
                Literal(self.lastName)
            ))

        if self.organizations:
            for organization in self.organizations.all():
                graph += organization.get_rdf_representation(serialize=False)
                graph.add((
                    organization.get_uri(),
                    DC.relation,
                    uri
                ))

        if serialize:
            return graph.serialize(format=format)
        return graph

    def __str__(self):
        return self.get_rdf_representation()