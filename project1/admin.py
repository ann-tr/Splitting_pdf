from django.contrib import admin
from .models import AccessLog , Pdfinfo
# Register your models here.


admin.site.register(AccessLog)


class PdfinfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_file_path', 'output_folder_path', 'date_time')  # Add 'id' here

admin.site.register(Pdfinfo)
