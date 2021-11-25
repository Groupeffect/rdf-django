import os
from django.db import models
from django.conf import settings
from rdflib import (
    Graph, URIRef, Literal,
    # namespaces:
    DC, PROV, RDF, FOAF, SDO, DOAP, SOSA, ORG,
)


class MetaModel(models.Model):
    label = models.CharField(max_length=100, default='no label')
    description = models.TextField(default='no desription')

    class Meta:
        abstract = True

    def get_meta_labels(self):
        """ get app model class name"""
        app_label = Literal(str(self.__class__).split("'")[1])
        label = Literal(str(self.__class__).split("'")[1].split('.')[2])
        return app_label, label

    def get_rdf_description(self, serialize=True):
        graph = Graph()
        uri = self.get_uri()
        graph.add((uri, DC.description, Literal(self.description)))

        if serialize:
            return graph.serialize(format=settings.GLOBAL_GRAPH_IO_FORMAT)
        return graph

    def __str__(self):
        return self.label


class Person(MetaModel):
    organizations = models.ManyToManyField("Organization", blank=True)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    employedAt = models.ManyToManyField(
        "Organization", related_name="employedAt", blank=True)
    projects = models.ManyToManyField(
        'Project', related_name="projects", blank=True)
    isHostOfProjects = models.ManyToManyField('Project', blank=True)
    memberOfProjects = models.ManyToManyField(
        'Project', related_name="memberOf", blank=True)

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_PERSON_URL, str(self.id)))

    def get_rdf_representation(self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT):
        entity = PROV.Person
        graph = Graph()
        uri = self.get_uri()
        graph.parse(data=self.get_rdf_description(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, RDF.type, entity))

        if self.firstName:
            graph.add((uri, FOAF.firstName, Literal(self.firstName)))
        if self.lastName:
            graph.add((uri, FOAF.lastName, Literal(self.lastName)))

        for organization in self.organizations.all():
            graph.parse(data=organization.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, DC.relation, organization.get_uri()))

        for employedAt in self.employedAt.all():
            graph.parse(data=employedAt.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, SDO.employee, employedAt.get_uri()))

        for project in self.projects.all():
            graph.parse(data=project.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, DC.relation, project.get_uri()))

        for project in self.isHostOfProjects.all():
            graph.parse(data=project.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((project.get_uri(), SOSA.isHostedBy, uri))

        for project in self.memberOfProjects.all():
            graph.parse(data=project.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, ORG.memberOf, project.get_uri()))

        if serialize:
            return graph.serialize(format=format)
        return graph


class Organization(MetaModel):
    website = models.URLField(blank=True, null=True)

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_ORGANIZATION_URL, str(self.id)))

    def get_rdf_representation(self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT):
        entity = PROV.Organization
        graph = Graph()
        uri = self.get_uri()
        graph.add((uri, RDF.type, entity))
        graph.parse(data=self.get_rdf_description(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, entity, Literal(self.label)))
        if self.website:
            graph.add((uri, FOAF.workInfoHomepage, Literal(self.website)))
        if serialize:
            return graph.serialize(format=format)
        return graph


class Project(MetaModel):
    website = models.URLField(blank=True, null=True)
    repository = models.URLField(blank=True, null=True)
    organizations = models.ManyToManyField(
        "Organization", blank=True, related_name='organizations')
    isHostedByOrganizations = models.ManyToManyField(
        "Organization", blank=True)

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_PROJECT_URL, str(self.id)))

    def get_rdf_representation(
        self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT
    ):
        entity = FOAF.Project
        graph = Graph()
        uri = self.get_uri()
        graph.add((uri, RDF.type, entity))
        graph.parse(data=self.get_rdf_description(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, entity, Literal(self.label)))
        if self.website:
            graph.add((uri, FOAF.workInfoHomepage, Literal(self.website)))
        if self.repository:
            graph.add((uri, DOAP.repository, Literal(self.repository)))
        for organization in self.organizations.all():
            graph.parse(data=organization.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, DC.relation, organization.get_uri()))
        for organization in self.isHostedByOrganizations.all():
            graph.parse(data=organization.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, SOSA.isHostedBy, organization.get_uri()))

        if serialize:
            return graph.serialize(format=format)
        return graph
