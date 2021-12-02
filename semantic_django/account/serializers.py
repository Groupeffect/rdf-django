from django.conf import settings
from rest_framework import serializers, reverse
from . import models


def uri_builder(name, obj, hash=''):
    return f"{settings.GLOBAL_HOST_URL}{reverse.reverse(str(name)+'-detail', kwargs={'pk': obj.id})}#{hash}"


class MetaModelSerializer(serializers.ModelSerializer):
    rdf = serializers.SerializerMethodField(read_only=True)

    def get_rdf(self, obj):
        return obj.get_rdf_representation()


class CategorySerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Category
        fields = ('__all__')

    def get_uri(self, obj):
        return uri_builder('category', obj, obj.value)


class SkillCategorySerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = models.Skill
        fields = ('__all__')

    def get_uri(self, obj):
        return uri_builder('skill', obj, obj.value)

    def get_category(self, obj):

        return uri_builder('category', obj.category, obj.category.value)


class PersonSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Person
        fields = ('__all__')

    def get_uri(self, obj):
        return uri_builder('person', obj, obj.label)


class PersonReadSerializer(PersonSerializer):
    skills = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    organizations = serializers.SerializerMethodField()
    isHostOfProjects = serializers.SerializerMethodField()
    memberOfProjects = serializers.SerializerMethodField()
    employedAt = serializers.SerializerMethodField()
    websites = serializers.SerializerMethodField()

    class Meta:
        model = models.Person
        fields = ('__all__')

    def get_websites(self, obj):
        uris = []
        for i in obj.websites.all():
            uris.append(uri_builder('website', i, i.value))
        return uris

    def get_skills(self, obj):
        uris = []
        for i in obj.skills.all():
            uris.append(uri_builder('skill', i, i.value))
        return uris

    def get_projects(self, obj):
        uris = []
        for i in obj.projects.all():
            uris.append(uri_builder('project', i, i.label))
        return uris

    def get_organizations(self, obj):
        uris = []
        for i in obj.organizations.all():
            uris.append(uri_builder('organization', i, i.label))
        return uris

    def get_employedAt(self, obj):
        uris = []
        for i in obj.employedAt.all():
            uris.append(uri_builder('organization', i, i.label))
        return uris

    def get_isHostOfProjects(self, obj):
        uris = []
        for i in obj.isHostOfProjects.all():
            uris.append(uri_builder('project', i, i.label))
        return uris

    def get_memberOfProjects(self, obj):
        uris = []
        for i in obj.memberOfProjects.all():
            uris.append(uri_builder('project', i, i.label))
        return uris


class PersonRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Person
        fields = ["rdf", ]

    def get_rdf(self, obj):
        param = self.context['request'].GET.get('param')
        if param == 'flat':
            return obj.get_rdf_flat_representation()
        return obj.get_rdf_representation()


class OrganizationSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Organization
        fields = ('__all__')

    def get_uri(self, obj):
        return uri_builder('organization', obj, obj.label)


class OrganizationReadSerializer(OrganizationSerializer):

    skills = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Project
        fields = ('__all__')

    def get_skills(self, obj):
        uris = []
        for i in obj.skills.all():
            uris.append(uri_builder('skill', i, i.value))
        return uris


class OrganizationRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["rdf", ]


class ProjectSerializer(MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Project
        fields = ('__all__')

    def get_uri(self, obj):
        return uri_builder('project', obj, obj.label)


class ProjectReadSerializer(MetaModelSerializer):

    skills = serializers.SerializerMethodField(read_only=True)
    organizations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Project
        fields = ('__all__')

    def get_skills(self, obj):
        uris = []
        for i in obj.skills.all():
            uris.append(uri_builder('skill', i, i.value))
        return uris

    def get_organizations(self, obj):
        uris = []
        for i in obj.organizations.all():
            uris.append(uri_builder('organization', i, i.label))
        return uris


class ProjectRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Project
        fields = ["rdf", ]


class SkillRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Skill
        fields = ["rdf", ]


class CategoryRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Skill
        fields = ["rdf", ]
