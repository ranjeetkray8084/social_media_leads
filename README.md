# Social Media Lead Generator

AI-powered lead generation system that scrapes Instagram, Facebook, and YouTube for real estate leads using Gemini Pro API.

## 🚀 Features

### AI-Powered Lead Generation
- **Gemini Pro Integration**: Advanced AI analysis for lead qualification
- **Multi-Platform Scraping**: Instagram, Facebook, YouTube support
- **Smart Lead Scoring**: Automatic quality assessment (1-10 scale)
- **Contact Extraction**: AI-powered phone/email detection
- **Requirement Analysis**: Property type and location parsing

### Supported Platforms
- **Instagram**: Hashtag monitoring (#gurgaonproperty, #realestate)
- **Facebook**: Group post analysis
- **YouTube**: Comment sentiment analysis

### Dashboard Features
- **Real-time Monitoring**: Live scraping status and statistics
- **Interactive Controls**: Easy configuration and management
- **Lead Export**: JSON export functionality
- **CRM Integration**: Ready for CRM system integration

## 🏗️ Architecture

```
social-media-lead-generator/
├── backend/                    # Flask API server
│   ├── app.py                 # Main Flask application
│   ├── services/              # AI and scraping services
│   │   ├── gemini_service.py  # Gemini Pro API integration
│   │   ├── instagram_service.py # Instagram scraping
│   │   ├── facebook_service.py  # Facebook scraping
│   │   └── youtube_service.py   # YouTube scraping
│   ├── models/                # Data models
│   ├── utils/                 # Utility functions
│   ├── requirements.txt       # Python dependencies
│   └── config.env            # Environment configuration
├── frontend/                  # Dashboard interface
│   ├── index.html            # Main dashboard
│   ├── package.json          # Frontend dependencies
│   └── README.md             # Frontend documentation
└── README.md                 # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser
- Gemini Pro API key
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd social-media-lead-generator
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config.env .env
# Edit .env with your Gemini API key
```

### 3. Frontend Setup
```bash
# Navigate to frontend
cd ../frontend

# Start development server
python -m http.server 3000
```

## ⚙️ Configuration

### Backend Configuration (config.env)
```bash
# Gemini Pro API
GEMINI_API_KEY=your_gemini_api_key_here

# Server Settings
SERVER_PORT=5000
DEBUG=False

# CRM Integration
CRM_API_URL=http://localhost:8080/api

# Instagram (Optional - for better access)
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# Scraping Limits
MAX_POSTS_PER_HASHTAG=50
MAX_COMMENTS_PER_VIDEO=50
```

### Frontend Configuration
The frontend automatically connects to the backend API. Update API URLs in `index.html` if needed.

## 🚀 Usage

### 1. Start Backend Server
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

### 2. Access Dashboard
Open browser and navigate to:
```
http://localhost:3000
```

### 3. Configure Scraping
- Set Instagram hashtags (e.g., gurgaonproperty, realestate)
- Configure Facebook groups to monitor
- Add YouTube video IDs for comment analysis

### 4. Generate Leads
- Click "Scrape Instagram" for hashtag monitoring
- Use "Scrape Facebook" for group analysis
- Try "Scrape YouTube" for comment analysis
- Use "Scrape All Platforms" for comprehensive scraping

### 5. Manage Results
- View generated leads in the dashboard
- Export leads as JSON
- Analyze lead quality with AI
- Send to CRM (integration ready)

## 📊 API Endpoints

### Health Check
```
GET /api/health
```

### Platform Scraping
```
POST /api/scrape/instagram
POST /api/scrape/facebook
POST /api/scrape/youtube
POST /api/scrape/all
```

### Lead Analysis
```
POST /api/leads/analyze
```

### Gemini Test
```
POST /api/gemini/test
```

## 🤖 AI Features

### Lead Quality Analysis
- **Intent Detection**: Identifies buying intent from content
- **Contact Extraction**: Finds phone numbers and emails
- **Requirement Parsing**: Extracts property type, location, budget
- **Scoring Algorithm**: 1-10 quality score based on multiple factors

### Content Analysis
- **Language Detection**: Supports Hindi and English
- **Sentiment Analysis**: Determines urgency and interest level
- **Context Understanding**: Real estate specific terminology
- **Recommendation Engine**: Suggests next actions

## 💰 Cost Analysis

### Free Setup (Recommended Start)
- **Gemini Pro API**: Free tier (60 requests/minute)
- **Scraping Tools**: Free libraries
- **Hosting**: Local development
- **Total Cost**: ₹0/month

### Professional Setup (When Scaling)
- **Gemini Pro API**: Free tier sufficient for most use cases
- **Premium Scraping**: ₹1000-1500/month for better reliability
- **Proxy Services**: ₹800-1200/month for anti-detection
- **Total Cost**: ₹1800-2700/month

### Expected ROI
- **Leads per Day**: 50-150 (depending on setup)
- **Conversion Rate**: 3-8%
- **Revenue per Conversion**: ₹10,000-50,000
- **Monthly Revenue Potential**: ₹1,50,000-6,00,000

## 🔧 Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check Python version
python --version

# Verify dependencies
pip list

# Check port availability
netstat -an | grep 5000
```

#### No Leads Generated
- Verify hashtags are active and popular
- Check Instagram/Facebook rate limits
- Review backend logs for errors
- Ensure Gemini API key is valid

#### Frontend Connection Issues
- Confirm backend is running on port 5000
- Check browser console for CORS errors
- Verify API endpoints are accessible

### Debug Mode
```bash
# Enable debug mode
export DEBUG=True
python app.py
```

## 📈 Performance Optimization

### Scraping Optimization
- **Rate Limiting**: Respectful delays between requests
- **Parallel Processing**: Multiple platforms simultaneously
- **Caching**: Store results to avoid re-scraping
- **Error Handling**: Robust retry mechanisms

### AI Optimization
- **Batch Processing**: Analyze multiple leads together
- **Caching**: Store AI responses for similar content
- **Prompt Engineering**: Optimize prompts for better results
- **Rate Limiting**: Manage Gemini API usage

## 🔒 Security Considerations

### API Security
- **Environment Variables**: Store sensitive data securely
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize all inputs
- **Error Handling**: Don't expose sensitive information

### Data Privacy
- **GDPR Compliance**: Handle personal data responsibly
- **Data Retention**: Implement data cleanup policies
- **Access Control**: Restrict API access
- **Audit Logging**: Track all operations

## 🚀 Deployment

### Local Development
```bash
# Backend
cd backend && python app.py

# Frontend
cd frontend && python -m http.server 3000
```

### Production Deployment
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Use Nginx as reverse proxy
# Configure SSL certificates
# Set up monitoring and logging
```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Check README files in each directory
- **Issues**: Open GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact the development team

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Basic scraping functionality
- ✅ Gemini Pro integration
- ✅ Dashboard interface
- ✅ Lead export

### Phase 2 (Next)
- 🔄 Advanced AI analysis
- 🔄 CRM integrations
- 🔄 Automated scheduling
- 🔄 Performance optimization

### Phase 3 (Future)
- 📋 Machine learning models
- 📋 Advanced analytics
- 📋 Multi-tenant support
- 📋 Enterprise features

---

**Ready to generate leads with AI? Start with the free setup and scale as you grow!** 🚀
