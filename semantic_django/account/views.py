from rdflib import Graph
from django.conf import settings
from rest_framework import viewsets, renderers, filters
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from . import models


class Nested:
    pass


class StaticXmlRenderer(renderers.StaticHTMLRenderer):

    media_type = "text/xml"
    format = "xml"


class MetaModelViewset(viewsets.ModelViewSet):
    renderer_classes = [
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
        StaticXmlRenderer
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def info_graph(self):
        graph = Graph()
        return graph

    def list(self, request, **kwargs):
        result = super().list(self, request, **kwargs)
        data = result.data
        graph = self.info_graph()
        if request.GET.get('format') == "xml":
            for instance in data['results']:
                graph.parse(
                    data=instance['rdf'], format=settings.GLOBAL_GRAPH_IO_FORMAT, )
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
    search_fields = ['label', 'firstName', 'lastName']

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.PersonRDFSerializer
        if self.action in ['list', 'retrieve', ]:
            return serializers.PersonReadSerializer
        return self.serializer_class


class OrganizationModelViewSet(MetaModelViewset):

    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()
    search_fields = ['label']

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.OrganizationRDFSerializer
        return self.serializer_class


class ProjectModelViewSet(MetaModelViewset):

    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()
    search_fields = ['label']

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.ProjectRDFSerializer

        if self.action in ['list', 'retrieve', ]:
            return serializers.ProjectReadSerializer
        return self.serializer_class


class SkillCategoryViewSet(MetaModelViewset):

    queryset = models.Skill.objects.all()
    serializer_class = serializers.SkillCategorySerializer
    search_fields = ['value']

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.SkillRDFSerializer
        return self.serializer_class


class CategoryViewSet(MetaModelViewset):

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    search_fields = ['value']

    def get_serializer_class(self):
        if self.request.GET.get('format') == "xml":
            return serializers.CategoryRDFSerializer
        return self.serializer_class
