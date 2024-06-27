from django.db import models
from django.contrib.auth.models import User


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.timestamp}"

class Pdfinfo(models.Model):
    #created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    input_file_path = models.CharField(max_length= 200,null = True ,blank = True  )
    output_folder_path = models.CharField(max_length= 200  )
    date_time = models.DateTimeField(auto_now_add= True)
    
   
    
    def __str__(self):
        return f"{self.input_file_path }- {self.output_folder_path} - {self.date_time} "
