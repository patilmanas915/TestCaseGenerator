# AI-Powered Test Case Generator - Web Application

A modern web application that automatically generates comprehensive test cases from Functional Requirements Documents (FRD) using Google Gemini AI.

## Features

🚀 **Web-Based Interface** - Modern, responsive web interface for easy document upload  
🤖 **AI-Powered Processing** - Uses Google Gemini AI to analyze FRD documents  
📄 **Multi-Format Support** - Supports PDF, DOCX, and TXT file formats  
🔄 **Real-Time Progress** - Live status updates during processing  
📊 **Comprehensive Test Cases** - Generates positive, negative, boundary, and edge test cases  
📈 **Statistics Dashboard** - Visual summary of generated test cases  
💾 **CSV Export** - Download test cases in organized CSV format  
🎨 **Modern UI** - Beautiful, intuitive user interface with drag-and-drop upload

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Modern web browser

## Quick Start

### 1. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key for configuration

### 2. Setup and Installation

#### Windows (Easy Setup)
```bash
# Double-click start.bat file
# or run in Command Prompt:
start.bat
```

#### Manual Setup
```bash
# Clone or download the project
cd web_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the web_app directory:

```env
SECRET_KEY=your-secret-key-change-this-in-production
GEMINI_API_KEY=your-google-gemini-api-key-here
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to: `http://localhost:5000`

## How to Use

### 1. Upload FRD Document
- Drag and drop your FRD document onto the upload area
- Or click to browse and select a file
- Supported formats: PDF, DOCX, TXT (Max 16MB)

### 2. Generate Test Cases
- Click "Generate Test Cases" button
- Monitor real-time progress updates
- AI will extract features and generate comprehensive test cases

### 3. Download Results
- View generation statistics
- Download CSV file with all generated test cases
- Generate new test cases for different documents

## Generated Test Case Format

The application generates test cases with the following fields:

| Field | Description |
|-------|-------------|
| Test Case ID | Unique identifier for each test case |
| Test Case Name | Descriptive name of the test case |
| Feature ID | ID of the feature being tested |
| Feature Name | Name of the feature being tested |
| Module | Module or component name |
| Test Type | Positive/Negative/Boundary/Edge |
| Priority | High/Medium/Low |
| Category | Functional/Non-functional |
| Preconditions | Prerequisites for test execution |
| Test Steps | Detailed step-by-step instructions |
| Test Data | Required test data |
| Expected Result | Expected outcome |
| Generated On | Timestamp of generation |

## Test Case Types Generated

- **Positive Test Cases**: Valid scenarios with expected inputs
- **Negative Test Cases**: Invalid scenarios and error conditions  
- **Boundary Test Cases**: Edge values and limit testing
- **Edge Cases**: Unusual or extreme scenarios

## Project Structure

```
web_app/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── gemini_client.py      # Google Gemini AI integration
├── document_processor.py # Document reading utilities
├── test_generator.py     # Test case generation logic
├── requirements.txt      # Python dependencies
├── start.bat            # Windows startup script
├── .env                 # Environment variables
├── templates/
│   └── index.html       # Main web interface
├── uploads/             # Temporary file uploads
└── downloads/           # Generated CSV files
```

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - File upload endpoint
- `GET /status/<session_id>` - Processing status
- `GET /download/<filename>` - Download generated CSV
- `GET /health` - Health check endpoint

## Deployment Options

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Flask secret key for sessions | Yes |
| GEMINI_API_KEY | Google Gemini API key | Yes |

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify your Gemini API key is correct
   - Check API quota and usage limits
   - Ensure the API key has proper permissions

2. **File Upload Fails**
   - Check file format (PDF, DOCX, TXT only)
   - Ensure file size is under 16MB
   - Verify file is not corrupted

3. **Processing Stuck**
   - Check internet connection
   - Verify API key is valid
   - Check server logs for detailed errors

4. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Logs and Debugging

Enable debug mode in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Performance Considerations

- Processing time depends on document size and complexity
- API rate limits apply (1 request per second)
- Large documents may take 5-15 minutes to process
- Concurrent processing is limited by API quotas

## Security Notes

- Keep your API key secure and never commit it to version control
- Use strong SECRET_KEY in production
- Uploaded files are automatically cleaned up after processing
- Consider implementing file scanning for production use

## Future Enhancements

- [ ] User authentication and session management
- [ ] Database storage for test case history
- [ ] Batch processing for multiple documents
- [ ] Custom test case templates
- [ ] Integration with test management tools
- [ ] Support for additional document formats

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review server logs
3. Verify API configuration
4. Check Google Gemini API documentation

## License

This project is for educational and internal use. Please respect Google Gemini API terms of service.
