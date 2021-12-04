import os
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from rdflib import (
    Graph, URIRef, Literal,
    # namespaces:
    DC, PROV, RDF, FOAF, SDO, DOAP, SOSA, ORG,
)

alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class MetaModel(models.Model):
    label = models.CharField(max_length=100, default='no_label_set')
    description = models.TextField(default='no_desription')
    unification = models.CharField(
        blank=True, null=True, max_length=100, validators=[alphanumeric])
    groupby = models.CharField(
        default='groupby',
        blank=True, null=True, max_length=100, validators=[alphanumeric])

    class Meta:
        abstract = True

    def get_unique_uri(self, graph, uri=None, base_uri=None, serialize=True):

        if not base_uri:
            base_uri = os.path.join(settings.GLOBAL_HOST_URL, 'api', 'account')

        app_label, app = self.get_meta_labels()

        unique_path = os.path.join(
            base_uri,
            str(app).replace('.', '/').lower(),
            str(self.groupby).replace(' ', '_'),
            str(self.unification).replace(' ', '_'),
        )
        print(unique_path)
        uuri = URIRef(unique_path)
        unique_name = unique_path.split('/')[-1]

        graph.add((uuri, RDF.type, PROV.Delegation))
        graph.add((uuri, FOAF.name, Literal(unique_name)))
        graph.add((uri, DC.description, uuri))

        if serialize:
            return graph.serialize(format=settings.GLOBAL_GRAPH_IO_FORMAT)
        return graph

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


class Category(MetaModel):
    value = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.value

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_CATEGORY_URL, str(self.id)))

    def get_rdf_representation(self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT):
        entity = PROV.Collection
        graph = Graph()
        uri = self.get_uri()
        graph.parse(data=self.get_rdf_description(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, RDF.type, entity))

        if serialize:
            return graph.serialize(format=format)
        return graph


class Skill(MetaModel):
    value = models.CharField(max_length=120, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    websites = models.ManyToManyField(
        'Website', related_name="websites", blank=True)

    def __str__(self):
        return self.value

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_SKILL_URL, str(self.id)))

    def get_rdf_representation(
            self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT,
            exclude_persons: bool = True):

        entity = PROV.Activity
        graph = Graph()
        uri = self.get_uri()

        graph.parse(data=self.get_rdf_description(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, RDF.type, entity))

        graph.parse(data=self.category.get_rdf_representation(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, DOAP.category, self.category.get_uri()))
        graph.add((uri, FOAF.name, Literal(self.value)))
        graph.parse(data=self.get_unique_uri(graph, uri),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)

        for website in self.websites.all():
            graph.parse(data=website.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, FOAF.weblog, website.get_uri()))

        if not exclude_persons:
            for person in self.persons.all():
                graph.parse(data=person.get_rdf_flat_representation(),
                            format=settings.GLOBAL_GRAPH_IO_FORMAT)
                graph.add((person.get_uri(), SDO.skills, uri))

        if serialize:
            return graph.serialize(format=format)
        return graph


class Website(MetaModel):
    organizations = models.ManyToManyField(
        "Organization", blank=True, related_name='organization_websites')
    persons = models.ManyToManyField(
        "Person", blank=True, related_name='persons')
    value = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.value

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_WEBSITE_URL, str(self.id)))

    def get_rdf_representation(self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT,):
        entity = SDO.WebSite
        graph = Graph()
        uri = self.get_uri()
        graph.parse(data=self.get_rdf_description(),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
        graph.add((uri, RDF.type, entity))

        if self.value:
            graph.add((uri, FOAF.weblog, Literal(self.value)))

        for organization in self.organizations.all():
            graph.parse(data=organization.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, FOAF.weblog, organization.get_uri()))

        for person in self.persons.all():
            graph.parse(data=person.get_rdf_flat_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, FOAF.weblog, person.get_uri()))

        if serialize:
            return graph.serialize(format=format)
        return graph


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
    website = models.URLField(
        default=settings.GLOBAL_HOST_URL, blank=True, null=True)
    websites = models.ManyToManyField('Website', blank=True)
    skills = models.ManyToManyField(
        Skill, related_name='persons', blank=True)

    def get_uri(self):
        return URIRef(os.path.join(settings.GLOBAL_API_ACCOUNT_PERSON_URL, str(self.id)))

    def get_rdf_flat_representation(self, serialize: bool = True, format: str = settings.GLOBAL_GRAPH_IO_FORMAT,):
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
        if self.website:
            graph.add((uri, FOAF.weblog, Literal(self.website)))

        if serialize:
            return graph.serialize(format=format)
        return graph

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
        if self.website:
            graph.add((uri, FOAF.weblog, Literal(self.website)))

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

        for skill in self.skills.all():
            graph.parse(data=skill.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, SDO.skills, skill.get_uri()))

        for website in self.websites.all():
            graph.parse(data=website.get_rdf_representation(),
                        format=settings.GLOBAL_GRAPH_IO_FORMAT)
            graph.add((uri, FOAF.weblog, website.get_uri()))

        if serialize:
            return graph.serialize(format=format)
        return graph


class Organization(MetaModel):
    website = models.URLField(blank=True, null=True)
    websites = models.ManyToManyField('Website', blank=True)
    skills = models.ManyToManyField(Skill, related_name='skills', blank=True)

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
        graph.parse(data=self.get_unique_uri(graph, uri),
                    format=settings.GLOBAL_GRAPH_IO_FORMAT)
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
    readPermissions = models.ManyToManyField(
        'Person', related_name="readPermission", blank=True)
    writePermissions = models.ManyToManyField(
        'Person', related_name="writePermission", blank=True)
    deletePermissions = models.ManyToManyField(
        'Person', related_name="deletePermission", blank=True)

    skills = models.ManyToManyField(Skill, blank=True)

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
        for person in self.readPermissions.all():
            graph.add((person.get_uri(), SDO.ReadPermission, uri))
        for person in self.writePermissions.all():
            graph.add((person.get_uri(), SDO.WritePermission, uri))
        for person in self.deletePermissions.all():
            graph.add((person.get_uri(), SDO.DeleteAction, uri))
        for skill in self.skills.all():
            graph.add((uri, DC.relation, skill.get_uri()))
        if serialize:
            return graph.serialize(format=format)
        return graph
