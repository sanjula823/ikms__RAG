## ✅ PDF Indexing - Fixed!

Your PDF indexing endpoint is now fixed. Here's how to use it correctly.

---

## 🚀 How to Index a PDF

### Option 1: Using Swagger UI (EASIEST)
1. Make sure server is running: `python -m uvicorn src.app.api:app --port 8000`
2. Open browser: **http://localhost:8000/docs**
3. Find the **POST /index-pdf** endpoint
4. Click "Try it out"
5. Click "Choose file" and select your PDF
6. Click "Execute"

### Option 2: Using cURL
```bash
# Upload a PDF file
curl -X POST http://localhost:8000/index-pdf \
  -F "file=@C:\path\to\your\document.pdf"
```

### Option 3: Using PowerShell
```powershell
$FilePath = "C:\path\to\your\document.pdf"
$Uri = "http://localhost:8000/index-pdf"

$Form = @{
    file = Get-Item -Path $FilePath
}

Invoke-WebRequest -Uri $Uri -Method Post -Form $Form
```

---

## ✨ Expected Response

If successful, you'll get:
```json
{
  "success": true,
  "filename": "document.pdf",
  "chunks_indexed": 42,
  "message": "Successfully indexed 42 chunks from document.pdf"
}
```

---

## 🔧 What Changed

### Before ❌
- Expected JSON body with file path string
- Didn't work with file uploads
- Error: "File path string is not a valid file or url"

### After ✅
- Now accepts actual file uploads (multipart form data)
- Saves file to temporary location
- Validates PDF extension
- Cleans up temp file after indexing
- Better error messages

---

## 📋 Requirements

- File must be `.pdf` extension
- File must be readable
- Server must have write permissions for temp files
- Pinecone must be configured in `.env`

---

## 🆘 Troubleshooting

### Error: "File must be a PDF"
→ Make sure file ends with `.pdf`

### Error: "No content extracted from PDF"
→ PDF might be corrupted or password-protected

### Error: "Error indexing PDF: [some error]"
→ Check server logs for detailed error message

---

## ✅ Complete Example

```bash
# 1. Start server
python -m uvicorn src.app.api:app --port 8000

# 2. Index a PDF (from another terminal)
curl -X POST http://localhost:8000/index-pdf \
  -F "file=@example.pdf"

# 3. Response
# {
#   "success": true,
#   "filename": "example.pdf",
#   "chunks_indexed": 25,
#   "message": "Successfully indexed 25 chunks from example.pdf"
# }

# 4. Ask a question about the indexed PDF
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this document about?",
    "top_k": 5
  }'
```

---

**Ready to go!** 🎉 Upload your first PDF and start asking questions!

