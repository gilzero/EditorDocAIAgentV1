# Dreamer Document AI Agent v0

A Flask-based web application that uses AI to analyze PDF and Word documents with a modern, user-friendly interface.

## Features

### Document Processing
- Supports PDF (.pdf) and Word (.docx) document uploads
- Maximum file size: 20MB
- Unicode filename support (including Chinese characters)
- Secure file handling and processing
- Uses MarkItDown library for data ingestion and text extraction

### AI Analysis
- Powered by OpenAI's GPT-4o model
- Provides comprehensive document analysis including:
  - General document summary (3-5 sentences)
  - Character analysis
  - Plot analysis
  - Thematic analysis
  - Readability assessment
  - Sentiment analysis
  - Style consistency evaluation

### User Interface
- Clean, modern interface with paper-like styling
- Drag-and-drop file upload
- Progress indicators during processing
- Dark/light mode support
- Toast notifications for user feedback
- Responsive design for mobile and desktop
- Detailed metadata display
- Results displayed in organized, collapsible sections

### Payment Integration
- Stripe payment integration
- Supports multiple payment methods
- Cost: ¥3 per document analysis
- Secure payment processing

## Technical Stack

### Backend
- Python/Flask
- SQLAlchemy for database management
- PostgreSQL database
- OpenAI API integration
- Stripe API for payments

### Frontend
- HTML5/CSS3/JavaScript
- Bootstrap for responsive design
- Feather Icons
- Custom CSS with theme support
- Modern UI components

### Key Libraries
- MarkItDown for document processing
- Flask-SQLAlchemy for ORM
- OpenAI for AI analysis
- Stripe for payment processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gilzero/DreamerDocumentAI.git
cd DreamerDocumentAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
FLASK_SECRET_KEY=<your-secret-key>
DATABASE_URL=<your-database-url>
OPENAI_API_KEY=<your-openai-api-key>
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Error Handling
- Comprehensive error handling system
- User-friendly error messages
- Handles various edge cases:
  - Empty files
  - Invalid formats
  - File size limits
  - Processing errors
  - Payment failures

## Security Features
- Secure file handling
- Input validation
- Secure payment processing
- Environmental variable protection
- SQL injection prevention
- XSS protection

## License
[Include License Information]

## Contributing
[Include Contributing Guidelines]

## Author
[Your Name/Organization]

---
For more information or support, please [create an issue](https://github.com/gilzero/DreamerDocumentAI/issues) or contact the maintainers.