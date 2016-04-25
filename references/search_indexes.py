from haystack import indexes

from .models import Reference


class ReferenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    add_date = indexes.DateTimeField(model_attr="add_date")
    added_by = indexes.CharField(model_attr='added_by')

    def get_model(self):
        return Reference
