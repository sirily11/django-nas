from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import File, Document as Doc


@registry.register_document
class FileDocument(Document):
    class Index:
        name = 'files'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = File
        fields = ['file', 'size']


@registry.register_document
class DocDocument(Document):
    class Index:
        name = 'docs'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Doc
        fields = ['name', 'content']
