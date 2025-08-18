from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
import logging
from datetime import datetime
import threading

from config import Config
from document_processor import DocumentProcessor
from test_generator import TestCaseGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Store processing status for each session
processing_status = {}

def process_document_async(session_id, file_path):
    """Process document asynchronously"""
    try:
        # Update status
        processing_status[session_id]['status'] = 'reading_document'
        processing_status[session_id]['message'] = 'Reading FRD document...'
        
        # Read document content
        content = DocumentProcessor.get_document_content(file_path)
        if not content:
            processing_status[session_id]['status'] = 'error'
            processing_status[session_id]['message'] = 'Failed to read document content'
            return
        
        # Check content length
        if len(content.strip()) < 100:
            processing_status[session_id]['status'] = 'error'
            processing_status[session_id]['message'] = 'Document content is too short or empty'
            return
        
        # Update status
        processing_status[session_id]['status'] = 'processing'
        processing_status[session_id]['message'] = 'Processing document with AI...'
        
        # Initialize test case generator
        generator = TestCaseGenerator()
        
        # Process document and generate test cases
        def progress_callback(message):
            processing_status[session_id]['message'] = message
        
        success, message = generator.process_frd_document(content, progress_callback)
        
        if not success:
            processing_status[session_id]['status'] = 'error'
            processing_status[session_id]['message'] = message
            return
        
        # Update status
        processing_status[session_id]['status'] = 'saving'
        processing_status[session_id]['message'] = 'Saving test cases to CSV...'
        
        # Save to CSV
        csv_path, save_message = generator.save_to_csv()
        
        if not csv_path:
            processing_status[session_id]['status'] = 'error'
            processing_status[session_id]['message'] = save_message
            return
        
        # Get summary statistics
        stats = generator.get_summary_stats()
        
        # Update final status
        processing_status[session_id]['status'] = 'completed'
        processing_status[session_id]['message'] = 'Test cases generated successfully!'
        processing_status[session_id]['csv_file'] = os.path.basename(csv_path)
        processing_status[session_id]['stats'] = stats
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        processing_status[session_id]['status'] = 'error'
        processing_status[session_id]['message'] = f'Error: {str(e)}'

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not Config.allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload PDF, DOCX, or TXT files.'}), 400
        
        # Check if API key is configured
        if not Config.GEMINI_API_KEY:
            return jsonify({'error': 'Gemini API key not configured. Please contact administrator.'}), 500
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Initialize processing status
        processing_status[session_id] = {
            'status': 'uploaded',
            'message': 'File uploaded successfully',
            'filename': filename,
            'upload_time': datetime.now().isoformat()
        }
        
        # Start processing in background
        thread = threading.Thread(target=process_document_async, args=(session_id, file_path))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'File uploaded successfully. Processing started.',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/status/<session_id>')
def get_status(session_id):
    """Get processing status"""
    if session_id not in processing_status:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify(processing_status[session_id])

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated CSV file"""
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'gemini_api_configured': bool(Config.GEMINI_API_KEY)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
