from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os 
from PyPDF2 import PdfReader, PdfWriter
from .models import Pdfinfo,User
#from .forms import UploadForm
from django.conf import settings


#API imports 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import MessageSerializer
from rest_framework.permissions import   AllowAny
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def say(request):
    return render(request,'template/hello.html')

def api_upload(request):
    return render(request,'template/api_upload.html')


def uploads(request):
    if request.method == 'POST' and request.FILES['pdf-upload']:
        pdf_file = request.FILES['pdf-upload']
        
        #saveing uploaded file in sytem storage
        folder_path =  os.path.join(str(settings.MEDIA_ROOT) , "input_pdfs")
        fs = FileSystemStorage(location = folder_path)
        filename = fs.save(pdf_file.name, pdf_file)
        name, ext = os.path.splitext(filename)
        uploaded_file_path = fs.path(filename)
        
        # Call the split_pdfs function
       
        output_files = split_pdfs(uploaded_file_path)
        name = f"{name}/"
        # Generate URLs for the split files
        folder_location = Pdfinfo.objects.create( input_file_path = uploaded_file_path , output_folder_path = output_files)
        folder_location.save()
        files = os.listdir(output_files)
    
        split_file_urls =   [request.build_absolute_uri(settings.MEDIA_URL + "outputs/" + name + file) for file in files]
       
        
        return render(request, 'template/uploads.html', {'split_file_urls': split_file_urls})
    return render(request, 'template/uploads.html')


def split_pdfs(input_file_path):
    inputpdf = PdfReader(open(input_file_path, "rb"))
    output_path = os.path.join(str(settings.MEDIA_ROOT) , "outputs")
   
    #extracting base file name
    base_filename = os.path.basename(input_file_path)
    name, ext = os.path.splitext(base_filename)
    output_folder_path = os.path.join(output_path,name)
    os.mkdir(output_folder_path) 
   
    
    for i, page in enumerate(inputpdf.pages):
        output = PdfWriter()
        output.add_page(page)
        print(f"{name}_page_{i+1}.pdf")
        #Generating file path for the split files
        out_file_path = os.path.join(output_folder_path, f"{name}_page_{i+1}.pdf")
        print("path of output  files",out_file_path)
        
        #writing contents of Pdfwriter object to the new output files
        with open(out_file_path, "wb") as output_stream:
            output.write(output_stream)
            
    return output_folder_path


#API POST
class MyModelView(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [FormParser,MultiPartParser,FileUploadParser]
    serializer_class = MessageSerializer
    
    @csrf_exempt
    def post(self,request):
        '''if request.method == 'POST':
            
            request.user = Pdfinfo.objects.first()'''
            
        try:
            request.user = Pdfinfo.objects.first()
            print("YES INSiDE TRY ----------")
            serializer = self.serializer_class(request.user,data = request.FILES)
            file_input = request.FILES['upload_file_path']
            print(file_input)
            folder_path =  os.path.join(str(settings.MEDIA_ROOT) , "input_pdfs")
            fs = FileSystemStorage(location = folder_path)
            filename = fs.save(file_input.name, file_input)
            uploaded_file_path = fs.path(filename)
            print(uploaded_file_path)
            print("FILE PATH IS GIEVN HERE ---------->",file_input)
            split_pdf_function = split_pdfs( uploaded_file_path)
            ''' pdf_info = Pdfinfo.objects.create( input_file_path = uploaded_file_path,  # Include uploaded file path
                        output_folder_path = split_pdf_function )'''
            print(split_pdf_function)
                        
            serializer = self.serializer_class(data={
                        'input_file_path': uploaded_file_path,  # Include uploaded file path
                        'output_folder_path': split_pdf_function  # Include output folder path
                    })
            if serializer.is_valid():
                serializer.save()
            
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            
        except  Exception as e :
            return Response({'error' : str(e)},status=status.HTTP_406_NOT_ACCEPTABLE)
                

        #return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
           
           
           # USE THISSSSS ------->   serializer.validated_data['file']
           
        ''' serializer_instance = serializer.save()
            file_path = serializer_instance.input_file_path.path
            split_pdf_function = split_pdfs(file_path)
                #pdfinfo_instance = Pdfinfo.objects.create(input_file_path=input_file, output_folder=split_pdf_function)
            serializer.save(output_folder = split_pdf_function)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            #return Response({"input_file_path":serializer.data['input_file_path'] ,"out_folder_path": serializer.output_folder}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)'''
        
        
        
    
    ''' form = UploadForm(request.POST or None ,  request.FILES or None)

        if 'file-upload' not in request.FILES:
            return Response({"detail": "File not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        #if form.is_valid():
        
        if UploadForm(request.POST ,request.FILES):
            files_path = request.FILES
            folder_path =  os.path.join(settings.MEDIA_ROOT + "inputpdfs")
            fs = FileSystemStorage(location = folder_path)
            filename = fs.save(files_path.name, files_path)
            
            uploaded_file_path = fs.path(filename)                
            obj = Pdfinfo.objects.create(input_file_path = uploaded_file_path )
            obj.save()
                
        return Response (status=status.HTTP_201_CREATED)
    #return Response(status= status.HTTP_406_NOT_ACCEPTABLE)'''
    
      
    