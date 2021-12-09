from django.conf import settings
from rest_framework import serializers, reverse
from . import models


def uri_builder(name, instance, hash=False, format=False):
    if format:
        format = f'?format={format}'
    else:
        format = ""

    if hash:
        hash = f"#{hash}"
    else:
        hash = ""
    return f"{settings.GLOBAL_HOST_URL}{reverse.reverse(str(name)+'-detail', kwargs={'pk': instance.id})}{format}{hash}"


class MetaRdfUrlMixin:
    def get_rdf(self, instance):
        name = str(self.Meta.model.__name__).lower()
        return uri_builder(str(name), instance, format="xml")

    def get_websites(self, instance):
        uris = []
        for i in instance.websites.all():
            uris.append(f"{i.value}#{uri_builder('website', i)}")
        return uris


class MetaModelSerializer(serializers.ModelSerializer):
    rdf = serializers.SerializerMethodField(read_only=True)

    def get_rdf(self, instance):
        return instance.get_rdf_representation()


class CategorySerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Category
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('category', instance, instance.value)


class SkillSerializer(MetaRdfUrlMixin, MetaModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Skill
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('skill', instance, instance.value)


class SkillReadSerializer(SkillSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField()
    websites = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Skill
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('skill', instance, instance.value)

    def get_category(self, instance):

        return uri_builder('category', instance.category, instance.category.value)


class SkillRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Skill
        fields = ["rdf", ]

    def get_rdf(self, instance):
        include = self.context['request'].GET.get('include')
        exclude_persons = True
        if include == 'person':
            exclude_persons = False
        return instance.get_rdf_representation(exclude_persons=exclude_persons)


class PersonSerializer(MetaRdfUrlMixin, MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Person
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('person', instance, instance.label)


class PersonReadSerializer(PersonSerializer):
    skills = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    organizations = serializers.SerializerMethodField(read_only=True)
    isHostOfProjects = serializers.SerializerMethodField()
    memberOfProjects = serializers.SerializerMethodField()
    employedAt = serializers.SerializerMethodField()
    websites = serializers.SerializerMethodField()

    class Meta:
        model = models.Person
        fields = ('__all__')

    def get_skills(self, instance):
        uris = []
        for i in instance.skills.all():
            uris.append(uri_builder('skill', i, i.value))
        return uris

    def get_projects(self, instance):
        uris = []
        for i in instance.projects.all():
            uris.append(uri_builder('project', i, i.label))
        return uris

    def get_organizations(self, instance):
        uris = []
        for i in instance.organizations.all():
            uris.append(uri_builder('organization', i, i.label))
        return uris

    def get_employedAt(self, instance):
        uris = []
        for i in instance.employedAt.all():
            uris.append(uri_builder('organization', i, i.label))
        return uris

    def get_isHostOfProjects(self, instance):
        uris = []
        for i in instance.isHostOfProjects.all():
            uris.append(uri_builder('project', i, i.label))
        return uris

    def get_memberOfProjects(self, instance):
        uris = []
        for i in instance.memberOfProjects.all():
            uris.append(uri_builder('project', i, i.label))
        return uris


class PersonRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Person
        fields = ["rdf", ]

    def get_rdf(self, instance):
        param = self.context['request'].GET.get('param')
        if param == 'flat':
            return instance.get_rdf_flat_representation()
        return instance.get_rdf_representation()


class OrganizationSerializer(MetaRdfUrlMixin, MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Organization
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('organization', instance, instance.label)


class OrganizationReadSerializer(OrganizationSerializer):

    skills = serializers.SerializerMethodField(read_only=True)
    persons = serializers.SerializerMethodField()

    class Meta:
        model = models.Organization
        fields = ('__all__')

    def get_skills(self, instance):
        uris = []
        for i in instance.skills.all():
            uris.append(uri_builder('skill', i, i.value))
        return uris

    def get_persons(self, instance):
        return instance.persons.all().values("id", "label")


class OrganizationRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["rdf", ]


class ProjectSerializer(MetaRdfUrlMixin, MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Project
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('project', instance, instance.label)


class ProjectReadSerializer(MetaModelSerializer):

    skills = serializers.SerializerMethodField(read_only=True)
    organizations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Project
        fields = ('__all__')

    def get_skills(self, instance):
        uris = []
        for i in instance.skills.all():
            uris.append(uri_builder('skill', i, i.value))
        return uris

    def get_organizations(self, instance):
        uris = []
        for i in instance.organizations.all():
            uris.append(uri_builder('organization', i, i.label))
        return uris


class ProjectRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Project
        fields = ["rdf", ]


class CategoryRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Skill
        fields = ["rdf", ]


class WebsiteSerializer(MetaRdfUrlMixin, MetaModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Website
        fields = ('__all__')

    def get_uri(self, instance):
        return uri_builder('website', instance)


class WebsiteReadSerializer(WebsiteSerializer):

    skills = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Website
        fields = ('__all__')

    def get_website(self, instance):
        return uri_builder('website', instance, instance.value)


class WebsiteRDFSerializer(MetaModelSerializer):
    class Meta:
        model = models.Website
        fields = ["rdf", ]
