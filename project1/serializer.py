from rest_framework import serializers
from .models import Pdfinfo
from django.core.validators import FileExtensionValidator 

class MessageSerializer(serializers.ModelSerializer):
    #input_file = serializers.FileField(write_only = True,validators = [FileExtensionValidator( ['pdf'] ) ])
    upload_file_path = serializers.FileField()
    output_folder_path = serializers.FileField()
    class Meta:
        model = Pdfinfo
        fields = ['upload_file_path','output_folder_path']
        
        
    def update(self, instance,validated_data):
        instance.output_folder_path = validated_data.get('output_folder_path',instance.output_folder_path)
        
        instance.input_file_path = validated_data.get('input_file_path',instance.input_file_path)
        
        return super().update(instance,validated_data)
   