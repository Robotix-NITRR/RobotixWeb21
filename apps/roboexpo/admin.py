from django.contrib import admin
from .models import Roboexpo
from import_export.admin import ImportExportModelAdmin


class RoboexpoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    model = Roboexpo
    list_display = ('id', 'team_name', 'selected', 'mail_delivered', 'bid')
    list_display_links = ('id' ,'team_name')
    list_filter = ('selected',)
    list_editable = ('selected','mail_delivered',)

admin.site.register(Roboexpo, RoboexpoAdmin)
