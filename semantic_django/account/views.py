from rdflib import Graph
from django.conf import settings
from rest_framework import viewsets, renderers
from . import serializers
from . import models


class Nested:
    pass


class StaticXmlRenderer(renderers.StaticHTMLRenderer):

    media_type = "text/xml"
    format = "xml"


class MetaModelViewset(viewsets.ModelViewSet):

    def info_graph(self):
        graph = Graph()

        # namespace = str(self.__class__).split("'")[1]
        # result = Nested()
        # result.appname = Literal(f"#{namespace.split('.')[2]}")
        # result.viewname = Literal(f"#{namespace.split('.')[1]}")
        # result.appuri = URIRef(result.appname)
        # result.viewuri = URIRef(result.viewname)
        # result.organizationuri = URIRef('Organization')
        # result.personuri = URIRef('Person')

        # graph.add((result.personuri, RDF.type, PROV.Person))
        # graph.add((result.organizationuri, RDF.type, PROV.Organization))

        # graph.add((PROV.Organization, DC.relation, PROV.Person))
        # graph.add((PROV.Organization, DC.description, Literal('can have employees and general relations to persons')))
        # graph.add((PROV.Organization, FOAF.name, Literal('Organization')))
        # graph.add((PROV.Organization, DC.identifier, Literal('Organization')))
        # graph.add((PROV.Person, SDO.employee ,PROV.Organization))
        # graph.add((PROV.Person, FOAF.name ,Literal('Person')))
    # graph.add((PROV.Person, DC.description, Literal('can be employed at organization or have a general relation')))
        # graph.add((PROV.Person, DC.identifier, Literal('Person')))

        return graph

    def list(self, request, **kwargs):
        result = super().list(self, request, **kwargs)
        data = result.data
        graph = self.info_graph()
        if request.GET.get('format') == "xml":
            for instance in data:
                graph.parse(data=instance['rdf'], format=settings.GLOBAL_GRAPH_IO_FORMAT, )
            result.data = graph.serialize(format="xml")
        return result

    def retrieve(self, request, **kwargs):
        result = super().retrieve(self, request, **kwargs)
        if request.GET.get('format') == "xml":
            result.data = result.data['rdf']
        return result


class PersonModelViewSet(MetaModelViewset):

    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()
    renderer_classes = [
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
        StaticXmlRenderer
    ]

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.PersonRDFSerializer
        return self.serializer_class


class OrganizationModelViewSet(MetaModelViewset):

    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()
    renderer_classes = [
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
        StaticXmlRenderer
    ]

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.OrganizationRDFSerializer
        return self.serializer_class
