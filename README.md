# Dreamer Document AI Agent v1

## Overview
Dreamer Document AI Agent is a Flask-based web application designed for AI-powered analysis of PDF and Word documents. The application provides a seamless user experience for document analysis, with modern UI features and secure payment integration.

## Key Features

### Document Upload and Processing
- Supports PDF (.pdf) and Word (.docx) files.
- Maximum upload size: 20MB.
- Unicode filename support, including non-Latin characters.
- Secure file handling with automatic cleanup.

### AI-Powered Analysis
- Uses OpenAI's GPT-4 model for:
  - Document summarization.
  - Character and plot analysis.
  - Thematic and readability assessments.
  - Sentiment and style analysis.

### User Interface
- Responsive and accessible design with light/dark theme toggle.
- Drag-and-drop file upload functionality.
- Detailed document metadata display.
- Step-by-step progress indicators.
- Interactive and collapsible result sections.

### Payment Integration
- Stripe integration for secure payments.
- Pricing tiers based on character count.
- Minimum charge of ¥3.50.
- Supports multiple payment methods.

## Technology Stack

### Backend
- Flask (Python)
- SQLAlchemy ORM
- OpenAI API integration
- Alembic for database migrations

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap for responsive layout
- Feather Icons and custom CSS

### Additional Libraries
- MarkItDown for text extraction
- Toastify for notifications
- Stripe.js for payment handling

## Setup and Installation

### Prerequisites
- Python 3.8 or later
- PostgreSQL database

### Installation Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/gilzero/EditorDocAIAgentV1.git
   cd EditorDocAIAgentV1
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file with the following:
   ```plaintext
   FLASK_SECRET_KEY=<your-secret-key>
   DATABASE_URL=<your-database-url>
   OPENAI_API_KEY=<your-openai-api-key>
   STRIPE_SECRET_KEY=<your-stripe-secret-key>
   STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
   ```

4. **Run Database Migrations:**
   ```bash
   flask db upgrade
   ```

5. **Start the Application:**
   ```bash
   python main.py
   ```

   The application will be available at [http://localhost:5001](http://localhost:5001).

## Deployment
- Use Gunicorn as the WSGI server for production.
- Configure a reverse proxy (e.g., Nginx) for enhanced scalability and security.

## Testing
- Implement unit and integration tests for key functionalities.
- Use tools like Pytest for automated testing.

## Security Features
- Input validation and secure file handling.
- Payment validation on the server side.
- Use of environment variables for sensitive configurations.
- SQL injection and XSS protection.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any proposed changes.

## License
[MIT License](LICENSE)

## Author
Weiming Chen

## Organization
Weiming AI (https://weiming.ai)
Dreamer Studio (https://dreamer.xyz)

## Contact
For inquiries or support, please contact alan at dreamer.xyz.

