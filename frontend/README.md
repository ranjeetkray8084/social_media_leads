# Social Media Lead Generator - Frontend

A modern, responsive dashboard for the Social Media Lead Generator with AI-powered lead analysis.

## Features

### 🎯 Lead Generation
- **Instagram Scraping**: Extract leads from hashtags like #gurgaonproperty, #realestate
- **Facebook Groups**: Monitor real estate groups for potential leads
- **YouTube Comments**: Analyze comments on real estate videos
- **AI Analysis**: Gemini Pro integration for intelligent lead scoring

### 📊 Dashboard Features
- **Real-time Stats**: Live updates of lead generation metrics
- **Interactive Controls**: Easy-to-use scraping configuration
- **Lead Management**: View, analyze, and export generated leads
- **API Status**: Monitor backend API connection status

### 🤖 AI Integration
- **Lead Quality Analysis**: Automatic scoring and prioritization
- **Content Analysis**: Extract contact information and requirements
- **Sentiment Analysis**: Understand lead intent and urgency
- **Smart Recommendations**: AI-powered follow-up suggestions

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **UI Framework**: Tailwind CSS
- **Interactivity**: Alpine.js
- **Icons**: Font Awesome
- **Backend API**: Flask (Python)

## Quick Start

### 1. Prerequisites
- Python 3.7+ (for local server)
- Modern web browser
- Backend API running on port 5000

### 2. Installation
```bash
# Clone or download the project
cd socialend

# Start local server
python -m http.server 3000

# Or use Node.js if available
npm start
```

### 3. Access Dashboard
Open your browser and navigate to:
```
http://localhost:3000
```

## Configuration

### Backend API
Make sure your backend API is running on:
```
http://localhost:5000
```

### Gemini API Key
Add your Gemini Pro API key to the backend configuration:
```bash
# In backend/config.env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage Guide

### 1. Test Connection
- Click "Test Connection" to verify API connectivity
- Green indicator means API is ready

### 2. Configure Scraping
- **Hashtags**: Enter Instagram hashtags (comma-separated)
- **Facebook Groups**: Enter group names to monitor
- **YouTube Videos**: Enter video IDs to analyze comments

### 3. Generate Leads
- **Individual Platforms**: Click specific platform buttons
- **All Platforms**: Use "Scrape All Platforms" for comprehensive scraping
- Monitor progress with loading indicators

### 4. Manage Leads
- **View Details**: Click eye icon to see full lead information
- **AI Analysis**: Click brain icon for AI-powered insights
- **Export**: Download leads as JSON file
- **Send to CRM**: Integrate with your CRM system

## API Endpoints

The frontend communicates with these backend endpoints:

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

## Features in Detail

### Lead Scoring
Each lead gets a score from 1-10 based on:
- Contact information availability
- Requirement specificity
- Budget indication
- Timeline urgency
- Content quality

### Platform Integration
- **Instagram**: Uses Instaloader for hashtag monitoring
- **Facebook**: Selenium-based group scraping
- **YouTube**: Comment analysis from video IDs

### AI Analysis
- **Gemini Pro**: Advanced language understanding
- **Lead Qualification**: Automatic quality assessment
- **Contact Extraction**: Smart phone/email detection
- **Requirement Parsing**: Property type and location extraction

## Customization

### Styling
Modify Tailwind classes in `index.html` to customize:
- Color scheme
- Layout spacing
- Component styling
- Responsive behavior

### Functionality
Add new features by extending the Alpine.js component:
- Additional scraping platforms
- Enhanced lead analysis
- CRM integrations
- Reporting features

## Troubleshooting

### Common Issues

#### API Connection Failed
- Check if backend is running on port 5000
- Verify CORS settings in backend
- Check browser console for errors

#### No Leads Generated
- Verify hashtags/groups are active
- Check scraping configuration
- Review backend logs for errors

#### Slow Performance
- Reduce scraping limits in configuration
- Check network connectivity
- Monitor backend resource usage

## Development

### Adding New Features
1. Modify the Alpine.js component in `index.html`
2. Add corresponding backend API endpoints
3. Update the UI with new controls
4. Test with different configurations

### Styling Changes
- Use Tailwind CSS classes for styling
- Maintain responsive design principles
- Test on different screen sizes

## Deployment

### Static Hosting
This is a static frontend that can be deployed to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

### Production Setup
1. Update API URLs for production
2. Configure CORS settings
3. Set up proper error handling
4. Add monitoring and analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review backend logs
- Open an issue on GitHub
- Contact the development team
