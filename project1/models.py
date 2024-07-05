from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator 


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.timestamp}"

class Pdfinfo(models.Model):
    #created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    input_file_path = models.FileField( upload_to= "input_pdfs/",null = True ,blank = True , validators=[FileExtensionValidator( ['pdf'] ) ] )
    output_folder_path = models.FileField(upload_to = "outputs/", null = True ,blank = True ,validators=[FileExtensionValidator( ['pdf'] ) ])
    date_time = models.DateTimeField(auto_now_add= True)

    
    def __str__(self):
        return f"{self.id}- {self.input_file_path }- {self.output_folder_path} - {self.date_time} "
