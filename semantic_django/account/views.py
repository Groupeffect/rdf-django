from rdflib import Graph
from django.conf import settings
from rest_framework import viewsets, renderers
from . import serializers
from . import models


class StaticXmlRenderer(renderers.StaticHTMLRenderer):

    media_type = "text/xml"
    format = "xml"

class MetaModelViewset(viewsets.ModelViewSet):

    def list(self, request, **kwargs):
        result = super().list(self, request, **kwargs)
        data = result.data
        graph = Graph()
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