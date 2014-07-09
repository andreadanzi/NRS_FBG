from django.db import models

# Create your models here.
class Centralina(models.Model):
    descrizione = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')
    # ...
    def __unicode__(self):
        return self.descrizione

class Canale(models.Model):
    centralina = models.ForeignKey(Centralina)
    codice = models.CharField(max_length=200)
    no_sensori = models.IntegerField()
    # ...
    def __unicode__(self):
        return self.codice
		
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

class Location(models.Model):
    #id = models.IntegerField(primary_key=True)
    location_name = models.CharField(max_length=255, blank=True)
    country_id = models.IntegerField()
    latitude = models.FloatField() # This field type is a guess.
    longitude = models.FloatField() # This field type is a guess.
    location_visible = models.IntegerField() # This field type is a guess.
    location_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'location'
    # ...
    def __unicode__(self):
        return self.location_name

class NrsEnvironment(models.Model):
    #id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    environment_uid = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    status = models.IntegerField()
    updated = models.DateTimeField(null=True, blank=True)
    location_id = models.ForeignKey(Location, db_column="location_id")
    location_name = models.CharField(max_length=100, blank=True)
    location_disposition = models.CharField(max_length=255, blank=True)
    location_exposure = models.CharField(max_length=255, blank=True)
    location_latitude = models.CharField(max_length=255, blank=True)
    location_longitude = models.CharField(max_length=255, blank=True)
    location_elevation = models.IntegerField(blank=True) # This field type is a guess.
    feed = models.TextField(blank=True)
    active = models.IntegerField() # This field type is a guess.
    person_first = models.CharField(max_length=200, blank=True)
    person_last = models.CharField(max_length=200, blank=True)
    person_email = models.CharField(max_length=120, blank=True)
    person_phone = models.CharField(max_length=60, blank=True)
    automatic_reports = models.IntegerField() # This field type is a guess.
    class Meta:
        db_table = u'nrs_environment'
    # ...
    def __unicode__(self):
        return self.title

class NrsNode(models.Model):
    #id = models.IntegerField(primary_key=True)
    nrs_environment_id = models.ForeignKey(NrsEnvironment,db_column="nrs_environment_id")
    title = models.CharField(max_length=100, blank=True)
    node_uid = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    status = models.IntegerField()
    node_disposition = models.CharField(max_length=255, blank=True)
    node_exposure = models.CharField(max_length=255, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    risk_level = models.IntegerField()
    updated = models.DateTimeField(null=True, blank=True)
    active = models.IntegerField()
    class Meta:
        db_table = u'nrs_node'		
    # ...
    def __unicode__(self):
        return self.title

class NrsDatastream(models.Model):
    #id = models.IntegerField(primary_key=True)
    nrs_node_id = models.ForeignKey(NrsNode,db_column="nrs_node_id")
    title = models.CharField(max_length=100, blank=True)
    datastream_uid = models.CharField(max_length=32)
    unit_label = models.CharField(max_length=100, blank=True)
    unit_type = models.CharField(max_length=100, blank=True)
    unit_symbol = models.CharField(max_length=100, blank=True)
    unit_format = models.CharField(max_length=100, blank=True)
    tags = models.TextField(blank=True)
    current_value = models.FloatField() # This field type is a guess.
    min_value = models.FloatField() # This field type is a guess.
    max_value = models.FloatField() # This field type is a guess.
    updated = models.DateTimeField(null=True, blank=True)
    nrs_environment_id = models.ForeignKey(NrsEnvironment,db_column="nrs_environment_id")
    active = models.IntegerField()
    samples_num = models.IntegerField()
    factor_title = models.CharField(max_length=100, blank=True)
    factor_value = models.DecimalField(max_digits=10,decimal_places=6) # This field type is a guess.
    lambda_value = models.DecimalField(max_digits=10,decimal_places=6) # This field type is a guess.
    constant_value = models.DecimalField(max_digits=10,decimal_places=6) # This field type is a guess.
    class Meta:
        db_table = u'nrs_datastream'
    # ...
    def __unicode__(self):
        return self.title

class NrsDatastreamPicture(models.Model):
    #id = models.IntegerField(primary_key=True)
    datastream_id = models.ForeignKey(NrsDatastream,db_column="datastream_id")
    filename = models.TextField(blank=True)
    filepath = models.TextField(blank=True)
    px = models.IntegerField(blank=True) # This field type is a guess.
    py = models.IntegerField(blank=True) # This field type is a guess.
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'nrs_datastream_picture'
    # ...
    def __unicode__(self):
        return self.description
		
class FbgPicture(models.Model):
    title = models.CharField(max_length=100, blank=True)
    nrs_environment_id = models.ForeignKey(NrsEnvironment,db_column="nrs_environment_id")
    filename = models.TextField(blank=True)
    filepath = models.TextField(blank=True)
    px = models.IntegerField(blank=True)
    py = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    spandir = models.CharField(max_length=25, blank=True)
    class Meta:
        db_table = u'fbg_picture'
    # ...
    def __unicode__(self):
        return self.description

class NrsDatapoint(models.Model):
    #id = models.IntegerField(primary_key=True)
    nrs_environment_id = models.ForeignKey(NrsEnvironment,db_column="nrs_environment_id")
    nrs_node_id = models.ForeignKey(NrsNode,db_column="nrs_node_id")
    nrs_datastream_id = models.ForeignKey(NrsDatastream,db_column="nrs_datastream_id")
    incident_id = models.IntegerField()
    sample_no = models.IntegerField()
    value_at = models.DecimalField(max_digits=10,decimal_places=6) # This field type is a guess.
    datetime_at = models.CharField(max_length=29)
    updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'nrs_datapoint'

class NrsCsvClient(models.Model):
    #id = models.IntegerField(primary_key=True)
    active = models.IntegerField()
    folder = models.TextField(blank=True)
    file_name = models.TextField(blank=True)
    sha256sum = models.TextField(blank=True)
    noitems = models.IntegerField()
    saved_folder = models.TextField(blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'nrs_csv_client'

class NrsMeta(models.Model):
    #id = models.IntegerField(primary_key=True)
    nrs_datastream =  models.ForeignKey(NrsDatastream, db_column="nrs_entity_id")
    nrs_entity_type = models.IntegerField()
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = u'nrs_meta'
    # ...
    def __unicode__(self):
        return self.nrs_datastream.__unicode__() + " " + self.meta_key

