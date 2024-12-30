# Dreamer Document AI Agent v0

An advanced multilingual document analysis platform that leverages AI and sophisticated payment integrations to transform document processing through intelligent machine learning insights.

## Features

- Document Upload & Processing
  - Support for PDF (.pdf) and Word (.docx) documents
  - Maximum file size: 20MB
  - Unicode filename support (including Chinese characters)
  - Advanced document parsing with MarkItDown library

- AI Analysis (OpenAI GPT-4o)
  - Comprehensive document summarization
  - Character analysis
  - Plot analysis
  - Thematic analysis
  - Readability assessment
  - Sentiment analysis
  - Style consistency evaluation

- Payment Integration
  - Stripe payment processing
  - Multiple payment methods support:
    - Alipay
    - WeChat Pay
    - Apple Pay
    - Credit/Debit Cards
  - Price: ¥3 per document analysis

- User Interface
  - Clean, modern interface with paper-like styling
  - Progress indicators during upload and processing
  - Toast notifications for user feedback
  - Detailed metadata panel
  - Dark/Light mode support
  - Responsive design
  - Export analysis results as JSON

## Tech Stack

- Backend
  - Flask web framework
  - PostgreSQL database
  - OpenAI GPT-4o for document analysis
  - MarkItDown for document parsing

- Frontend
  - HTML5, CSS3, JavaScript
  - Bootstrap 5
  - Feather Icons
  - Canvas Confetti for animations

- Payment Processing
  - Stripe API with enhanced multi-payment gateway support

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd dreamer-document-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@host:port/dbname
OPENAI_API_KEY=your_openai_api_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_PAYMENT_METHOD_CONFIG=your_stripe_payment_method_config_id
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

## Deployment

This application is configured for deployment on Replit:

1. Fork the repository on Replit
2. Set up the required environment variables in Replit's Secrets tab
3. The application will automatically use the PostgreSQL database provided by Replit
4. Run the server using the "Run" button

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask session management
- `DATABASE_URL`: PostgreSQL database connection URL
- `OPENAI_API_KEY`: API key for OpenAI GPT-4o access
- `STRIPE_SECRET_KEY`: Stripe secret key for payment processing
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key for client-side integration
- `STRIPE_PAYMENT_METHOD_CONFIG`: Stripe payment method configuration ID

## File Upload Guidelines

- Supported formats: PDF (.pdf), Word (.docx)
- Maximum file size: 20MB
- Unicode filenames are supported
- Files are processed securely and temporarily stored

## Payment Integration

The application uses Stripe for payment processing with support for:
- Alipay
- WeChat Pay
- Apple Pay
- Credit/Debit Cards

Payment configuration ID: `pmc_1QbcRB00zr9oQIWafBW2LMWF`

## License

MIT License - see LICENSE file for details
