from django.shortcuts import render
from django.http import FileResponse
from PyPDF2 import PdfMerger
import io

def Test_Case1(request):
    if request.method == "POST":
        pdfs = request.FILES.getlist("pdfs")

       
        if not pdfs:
            return render(request, "application1/S1.html", {
                "message": "⚠️ Please select at least one file!"
            })

        if any(not f.name.lower().endswith(".pdf") for f in pdfs):
            return render(request, "application1/S1.html", {
                "message": "❌ Only PDF files are allowed! Please upload valid PDFs."
            })

        try:
           
            merger = PdfMerger()
            pdfs = sorted(pdfs, key=lambda x: x.name.lower())

            for pdf in pdfs:
                merger.append(pdf)

            merged_pdf = io.BytesIO()
            merger.write(merged_pdf)
            merger.close()
            merged_pdf.seek(0)

            
            return FileResponse(
                merged_pdf,
                as_attachment=True,
                filename="merged.pdf"
            )

        except Exception as e:
            return render(request, "application1/S1.html", {
                "message": f"⚠️ Error while merging: {str(e)}"
            })

    
    return render(request, "application1/S1.html")
