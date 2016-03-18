from import_export import resources, fields, widgets

from .models import Reference

# Resource for importing CSV file of article
class ReferenceResource(resources.ModelResource):

    class Meta:
        model = Reference
        fields = ('title','url','notes')
        import_id_fields = ('url',)
