from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os 
from PyPDF2 import PdfReader, PdfWriter
from django.conf import settings
# Create your views here.
def say(request):
    return render(request,'template/hello.html')

def uploads(request):
    if request.method == 'POST' and request.FILES['pdf-upload']:
        pdf_file = request.FILES['pdf-upload']
        
        #saveing uploaded file in sytem storage
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_path = fs.path(filename)
        
        # Call the split_pdfs function
       
        output_files = split_pdfs(uploaded_file_path)
        
        # Generate URLs for the split files
    
        split_file_urls =   [request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(file)) for file in output_files]
        
        return render(request, 'template/uploads.html', {'split_file_urls': split_file_urls})
    return render(request, 'template/uploads.html')



def split_pdfs(input_file_path):
    inputpdf = PdfReader(open(input_file_path, "rb"))
    output_path = settings.MEDIA_ROOT
    base_filename = os.path.basename(input_file_path)
    name, ext = os.path.splitext(base_filename)

    output_files = []
    
    for i, page in enumerate(inputpdf.pages):
        output = PdfWriter()
        output.add_page(page)
        
        #Generating file path for the split files
        out_file_path = os.path.join(output_path, f"{name}_page_{i+1}.pdf")
        
        #writing contents of Pdfwriter object to the new output files
        with open(out_file_path, "wb") as output_stream:
            output.write(output_stream)

        #Appending path of output files to output_files list
        output_files.append(out_file_path)

    return output_files



