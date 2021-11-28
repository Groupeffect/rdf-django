from django.contrib import admin
from . import models

admin.site.register(models.Person)
admin.site.register(models.Organization)
admin.site.register(models.Skill)
admin.site.register(models.Category)
admin.site.register(models.Project)
admin.site.register(models.Website)
