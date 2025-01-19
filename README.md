# Dreamer Document AI Agent v1

AI-powered document analysis system that provides comprehensive literary analysis of PDF and Word documents using GPT-4, with output in Chinese.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.0-blue.svg)

## 🌟 Features

### Document Analysis
- Supports PDF (.pdf) and Word (.docx) documents up to 20MB
- Uses MarkItDown for robust text extraction
- Fallback to PyPDF for enhanced compatibility
- Unicode filename support (including Chinese characters)

### AI Analysis (in Chinese)
- Powered by OpenAI's GPT-4o model (May 2024)
- Comprehensive literary analysis:
  - Document summarization
  - Character analysis
  - Plot structure analysis
  - Thematic exploration
  - Readability assessment
  - Sentiment analysis
  - Style consistency evaluation

### User Interface
- Modern, responsive design
- Dark/light theme toggle
- Drag-and-drop file upload
- Real-time progress tracking
- Interactive analysis display
- One-click JSON export

### Payment Integration
- Secure Stripe payment processing
- Support for Chinese Yuan (CNY)
- Multiple payment methods including Alipay
- Tiered pricing based on document length:
  ```
  ¥3.50  - Minimum charge
  ¥5.00  - Up to 50,000 characters
  ¥8.00  - Up to 100,000 characters
  ¥10.00 - Over 100,000 characters
  ```

## 🚀 Quick Start

### Prerequisites
```bash
# Required
Python 3.8+
pip (Python package installer)
Git

# Optional but recommended
Virtual environment tool
```

### Installation

1. **Get the Code**
```bash
git clone https://github.com/gilzero/EditorDocAIAgentV1.git
cd EditorDocAIAgentV1
```

2. **Set Up Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Copy example configuration
cp .env.example .env
```

Edit `.env` with your credentials:
```plaintext
# Description: Environment configuration
FLASK_SECRET_KEY=           # Your Flask secret key
DATABASE_URL=sqlite:///dreamer_document_ai.db   # Keep this as is
OPENAI_API_KEY=            # Your OpenAI API key
STRIPE_SECRET_KEY=         # Your Stripe secret key
STRIPE_PUBLISHABLE_KEY=    # Your Stripe publishable key
STRIPE_PAYMENT_METHOD_CONFIG=  # Your Stripe payment method configuration
```

### API Keys Setup

1. **OpenAI API Key**
- Sign up at https://platform.openai.com
- Create an API key in your dashboard
- Ensure you have access to GPT-4 models

2. **Stripe Keys**
- Register at https://dashboard.stripe.com
- Get test keys from the Developers section
- Configure CNY as your payment currency
- Set up Alipay in payment methods

### Launch the Application

1. **Start the Server**
```bash
python main.py
```

2. **Access the Interface**
- Open http://localhost:5001 in your browser
- Default port is 5001 (configurable in main.py)

## 💻 Development

### Project Structure
```
├── app.py                 # App initialization
├── main.py               # Entry point
├── models.py             # Database models
├── routes.py             # API endpoints
├── static/               # Frontend assets
│   ├── css/
│   └── js/
├── templates/            # HTML templates
├── utils/               # Helper functions
│   ├── ai_analyzer.py
│   ├── document_processor.py
│   └── stripe_utils.py
└── uploads/             # Document storage
```

### Key Components

#### Document Processing
- `MarkItDown`: Primary text extraction
- `PyPDF`: Fallback extraction
- Automatic cleanup of processed files
- UTF-8 encoding for Chinese text

#### Database
- SQLite database (created automatically)
- Located in instance/dreamer_document_ai.db
- SQLAlchemy ORM for database operations
- Automatic schema migrations

#### AI Integration
- Asynchronous document processing
- Configurable analysis options
- Error handling and retry logic
- Debug logging for AI responses

## 🔧 Troubleshooting

### Common Issues

1. **File Upload Fails**
   ```
   - Check file size (max 20MB)
   - Verify file format (.pdf or .docx)
   - Ensure uploads/ directory is writable
   ```

2. **Database Issues**
   ```
   - Verify instance/ directory exists
   - Check write permissions
   - Confirm DATABASE_URL in .env
   ```

3. **Payment Problems**
   ```
   - Validate Stripe configuration
   - Check CNY currency setup
   - Verify payment method configuration
   ```

### Debug Mode
Enable detailed logging:
```python
# In main.py
app.run(debug=True)
```

Logs are written to:
- Console output
- debug/ai_analyzer_request.txt
- debug/ai_analyzer_response.txt

## 📖 Documentation

Additional documentation:
- API Reference: `/documentation`
- User Guide: `/documentation/user-guide.md`
- Development: `/documentation/development.md`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

[MIT License](LICENSE)

## 👥 Team

- **Author**: Weiming Chen
- **Organization**: 
  - Weiming AI (https://weiming.ai)
  - Dreamer Studio (https://dreamer.xyz)
- **Contact**: alan at dreamer.xyz

## 🙋 Support

- GitHub Issues: Bug reports and feature requests
- Email: Technical support and inquiries
- Documentation: Integration and API questions