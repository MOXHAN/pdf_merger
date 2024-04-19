from flask import Flask
from flask import render_template, request, send_file
from PyPDF2 import PdfFileMerger, PdfFileReader
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        
        files = request.files.getlist("file")
        
        if not all(f.filename for f in files):
            return "No file selected", 400
        
        if files:

            merger = PdfFileMerger()

            for file in files:
                if file and file.filename.endswith(".pdf"):
                    file_stream = BytesIO(file.read())

                    try:
                        pdf_reader = PdfFileReader(file_stream)
                        merger.append(pdf_reader)
                    except Exception as e:
                        return f"Error reading file {file.filename}: {str(e)}", 400
                    
            file_io = BytesIO()
            merger.write(file_io)
            merger.close()
            file_io.seek(0)
            return send_file(file_io, mimetype="application/pdf", as_attachment=True, download_name="appended_document.pdf")
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5100)
