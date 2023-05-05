from rest_framework import serializers
from .models import *

class ClassSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length = 200)
    medium_id = serializers.RelatedField(source='medium')

    class Meta:
        model = Class
        fields = ('adminbase_ptr_id', 'class_name', 'medium_id_id')
