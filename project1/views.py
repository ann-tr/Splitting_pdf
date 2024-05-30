from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os 
from PyPDF2 import PdfReader, PdfWriter

# Create your views here.
def say(request):
    return render(request,'template/hello.html')

def uploads(request):
    if request.method == 'POST' and request.FILES['pdf-upload']:
        pdf_file = request.FILES['pdf-upload']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_path = fs.path(filename)
        
        # Call the split_pdfs function
       
        output_files = split_pdfs(uploaded_file_path)
        
        # Generate URLs for the split files
        split_file_urls = [fs.url(os.path.basename(file)) for file in output_files]
        
        return render(request, 'uploads.html', {'split_file_urls': split_file_urls})
    return render(request, 'uploads.html')


def split_pdfs(input_file_path):
    inputpdf = PdfReader(open(input_file_path, "rb"))
    output_path = "C:\\Users\\anavr\\myproject\\project1\\template\\outputs"

    base_filename = os.path.basename(input_file_path)
    name, ext = os.path.splitext(base_filename)
    
    for i, page in enumerate(inputpdf.pages):
        output = PdfWriter()
        output.add_page(page)

        out_file_path = os.path.join(output_path, f"{name}_page_{i+1}.pdf")
        with open(out_file_path, "wb") as output_stream:
            output.write(output_stream)

        output_path.append(out_file_path)

    return output_path





