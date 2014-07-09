from fbg.models import Centralina
from fbg.models import Canale
from fbg.models import Location
from fbg.models import NrsEnvironment
from fbg.models import NrsNode
from fbg.models import NrsDatastream
from fbg.models import NrsMeta
from fbg.models import FbgPicture
from django.contrib import admin

class CanaleInline(admin.TabularInline):
    model = Canale
    extra = 5

class CentralinaAdmin(admin.ModelAdmin):
    list_display = ('descrizione', 'creation_date')
    inlines = [CanaleInline]
	
admin.site.register(Centralina,CentralinaAdmin)
#admin.site.register(Canale)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'latitude', 'longitude')

admin.site.register(Location,LocationAdmin)

class NrsEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'environment_uid', 'description')

admin.site.register(NrsEnvironment,NrsEnvironmentAdmin)

class NrsNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'node_uid', 'description')

admin.site.register(NrsNode,NrsNodeAdmin)

class NrsDatastreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'datastream_uid', 'unit_label')

admin.site.register(NrsDatastream,NrsDatastreamAdmin)

class NrsMetaAdmin(admin.ModelAdmin):
    list_display = ( 'meta_key','nrs_datastream', 'nrs_entity_type')

admin.site.register(NrsMeta,NrsMetaAdmin)

class FbgPictureAdmin(admin.ModelAdmin):
    list_display = ( 'title','filename')

admin.site.register(FbgPicture,FbgPictureAdmin)