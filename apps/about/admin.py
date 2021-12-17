from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . models import *


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    pass


@admin.register(Achievements)
class AchievementsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Alumni)
class AlumniAdmin(ImportExportModelAdmin):
    pass
