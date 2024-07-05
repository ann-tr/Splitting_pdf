from rest_framework import serializers
from .models import Pdfinfo

class MessageSerializer(serializers.ModelSerializer):
    input_file_path = serializers.FileField()
    output_folder_path = serializers.FileField(read_only = True)
    class Meta:
        model = Pdfinfo
        fields = ['input_file_path','output_folder_path']
        
        
    def update(self, instance,validated_data):
        instance.output_folder_path = validated_data.get('output_folder_path',instance.output_folder_path)
        
        return super().update(instance,validated_data)
   