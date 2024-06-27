from rest_framework import serializers
from .models import Pdfinfo

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdfinfo
        fields = '__all__'