from os import read
from rest_framework import fields, serializers, reverse
from rdflib import Graph
from . import models


class MetaModelSerializer(serializers.ModelSerializer):
    rdf = serializers.SerializerMethodField(read_only=True)

    def get_rdf(self, obj):
        return obj.get_rdf_representation()


class PersonSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Person
        fields = [
            "id",
            "label",
            "description",
            "rdf",
            "uri",
        ]

    def get_uri(self, obj):

        return reverse.reverse('person-detail', kwargs={"pk": obj.id})
