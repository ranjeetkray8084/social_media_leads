"""
Social Media Lead Generator API
Main Flask application with Gemini Pro integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)

# Import services
from services.gemini_service import GeminiService
from services.instagram_service_fixed import InstagramService
from services.facebook_service import FacebookService
from services.youtube_service import YouTubeService
from utils.simple_excel_service import SimpleExcelService as ExcelService
from services.scheduler_service import scheduler_service

# Initialize services
gemini_service = GeminiService()
instagram_service = InstagramService()
facebook_service = FacebookService()
youtube_service = YouTubeService()
excel_service = ExcelService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Social Media Lead Generator API is running',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gemini/test', methods=['POST'])
def test_gemini():
    """Test Gemini API integration"""
    try:
        data = request.json or {}
        test_text = data.get('text', 'Hello, this is a test message for Gemini API')
        
        # Test Gemini API
        response = gemini_service.test_api(test_text)
        
        return jsonify({
            'success': True,
            'gemini_response': response,
            'message': 'Gemini API is working correctly'
        })
        
    except Exception as e:
        logging.error(f"Gemini test error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scrape/instagram', methods=['POST'])
def scrape_instagram():
    """Scrape Instagram for leads"""
    try:
        data = request.json or {}
        hashtags = data.get('hashtags', ['gurgaonproperty', 'realestate'])
        
        logging.info(f"Starting Instagram scraping for hashtags: {hashtags}")
        
        # Scrape Instagram
        posts = instagram_service.scrape_hashtags(hashtags)
        
        # AI analysis with Gemini
        leads = gemini_service.analyze_posts_for_leads(posts)
        
        # Save results to logs
        logging.info(f"Instagram scraping completed. Found {len(leads)} leads")
        
        return jsonify({
            'success': True,
            'leads': leads,
            'total_found': len(leads),
            'platform': 'instagram',
            'hashtags_scraped': hashtags,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Instagram scraping error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'platform': 'instagram'
        }), 500

@app.route('/api/scrape/facebook', methods=['POST'])
def scrape_facebook():
    """Scrape Facebook groups for leads"""
    try:
        data = request.json or {}
        groups = data.get('groups', ['gurgaonproperty', 'realestate'])
        
        logging.info(f"Starting Facebook scraping for groups: {groups}")
        
        # Scrape Facebook
        posts = facebook_service.scrape_groups(groups)
        
        # AI analysis with Gemini
        leads = gemini_service.analyze_posts_for_leads(posts)
        
        logging.info(f"Facebook scraping completed. Found {len(leads)} leads")
        
        return jsonify({
            'success': True,
            'leads': leads,
            'total_found': len(leads),
            'platform': 'facebook',
            'groups_scraped': groups,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Facebook scraping error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'platform': 'facebook'
        }), 500

@app.route('/api/scrape/youtube', methods=['POST'])
def scrape_youtube():
    """Scrape YouTube comments for leads"""
    try:
        data = request.json or {}
        video_ids = data.get('video_ids', [])
        
        logging.info(f"Starting YouTube scraping for videos: {video_ids}")
        
        # Scrape YouTube
        comments = youtube_service.scrape_comments(video_ids)
        
        # AI analysis with Gemini
        leads = gemini_service.analyze_comments_for_leads(comments)
        
        logging.info(f"YouTube scraping completed. Found {len(leads)} leads")
        
        return jsonify({
            'success': True,
            'leads': leads,
            'total_found': len(leads),
            'platform': 'youtube',
            'videos_scraped': video_ids,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"YouTube scraping error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'platform': 'youtube'
        }), 500

@app.route('/api/scrape/all', methods=['POST'])
def scrape_all():
    """Scrape all platforms and return combined leads"""
    try:
        data = request.json or {}
        
        logging.info("Starting comprehensive social media scraping")
        
        all_leads = []
        results = {}
        
        # Instagram scraping
        try:
            instagram_posts = instagram_service.scrape_hashtags(['gurgaonproperty', 'realestate'])
            instagram_leads = gemini_service.analyze_posts_for_leads(instagram_posts)
            all_leads.extend(instagram_leads)
            results['instagram'] = {
                'success': True,
                'leads_count': len(instagram_leads)
            }
        except Exception as e:
            results['instagram'] = {
                'success': False,
                'error': str(e)
            }
        
        # Facebook scraping
        try:
            facebook_posts = facebook_service.scrape_groups(['gurgaonproperty'])
            facebook_leads = gemini_service.analyze_posts_for_leads(facebook_posts)
            all_leads.extend(facebook_leads)
            results['facebook'] = {
                'success': True,
                'leads_count': len(facebook_leads)
            }
        except Exception as e:
            results['facebook'] = {
                'success': False,
                'error': str(e)
            }
        
        # YouTube scraping
        try:
            youtube_comments = youtube_service.scrape_comments(['real_estate_video_id'])
            youtube_leads = gemini_service.analyze_comments_for_leads(youtube_comments)
            all_leads.extend(youtube_leads)
            results['youtube'] = {
                'success': True,
                'leads_count': len(youtube_leads)
            }
        except Exception as e:
            results['youtube'] = {
                'success': False,
                'error': str(e)
            }
        
        logging.info(f"Comprehensive scraping completed. Total leads found: {len(all_leads)}")
        
        return jsonify({
            'success': True,
            'leads': all_leads,
            'total_found': len(all_leads),
            'platforms': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Comprehensive scraping error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/leads/analyze', methods=['POST'])
def analyze_leads():
    """Analyze lead quality and scoring"""
    try:
        data = request.json or {}
        leads = data.get('leads', [])
        
        if not leads:
            return jsonify({
                'success': False,
                'error': 'No leads provided for analysis'
            }), 400
        
        # Analyze leads with Gemini
        analyzed_leads = gemini_service.analyze_lead_quality(leads)
        
        return jsonify({
            'success': True,
            'analyzed_leads': analyzed_leads,
            'total_analyzed': len(analyzed_leads),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Lead analysis error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/leads/export/excel', methods=['POST'])
def export_leads_to_excel():
    """Export leads to Excel file"""
    try:
        data = request.json or {}
        leads = data.get('leads', [])
        filename = data.get('filename')
        
        if not leads:
            return jsonify({
                'success': False,
                'error': 'No leads provided for export'
            }), 400
        
        # Export to Excel
        filepath = excel_service.export_leads_to_excel(leads, filename)
        
        if filepath:
            # Create summary sheet
            excel_service.create_summary_sheet(leads, filepath)
            
            # Get file info
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)
            
            return jsonify({
                'success': True,
                'message': f'Successfully exported {len(leads)} leads to Excel',
                'filename': filename,
                'filepath': filepath,
                'file_size': file_size,
                'download_url': f'/api/download/{filename}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to export leads to Excel'
            }), 500
            
    except Exception as e:
        logging.error(f"Excel export error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download exported Excel file"""
    try:
        from flask import send_file
        
        filepath = os.path.join(excel_service.output_dir, filename)
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
            
    except Exception as e:
        logging.error(f"File download error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/exports/history', methods=['GET'])
def get_export_history():
    """Get export history"""
    try:
        history = excel_service.get_export_history()
        
        return jsonify({
            'success': True,
            'exports': history,
            'total_files': len(history)
        })
        
    except Exception as e:
        logging.error(f"Export history error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/exports/<filename>', methods=['DELETE'])
def delete_export_file(filename):
    """Delete export file"""
    try:
        success = excel_service.delete_export_file(filename)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'File {filename} deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'File not found or could not be deleted'
            }), 404
            
    except Exception as e:
        logging.error(f"File deletion error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Scheduler endpoints
@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    """Start automatic scanning scheduler"""
    try:
        data = request.get_json() or {}
        
        # Update configuration if provided
        if 'hashtags' in data:
            scheduler_service.set_config(hashtags=data['hashtags'])
        if 'facebook_groups' in data:
            scheduler_service.set_config(facebook_groups=data['facebook_groups'])
        if 'youtube_videos' in data:
            scheduler_service.set_config(youtube_videos=data['youtube_videos'])
        
        # Start scheduler
        scheduler_service.start_scheduler()
        
        return jsonify({
            'success': True,
            'message': f'Automatic scanning started every {scheduler_service.scan_interval} minutes',
            'status': scheduler_service.get_status()
        })
        
    except Exception as e:
        logging.error(f"Error starting scheduler: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """Stop automatic scanning scheduler"""
    try:
        scheduler_service.stop_scheduler()
        
        return jsonify({
            'success': True,
            'message': 'Automatic scanning stopped',
            'status': scheduler_service.get_status()
        })
        
    except Exception as e:
        logging.error(f"Error stopping scheduler: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """Get scheduler status"""
    try:
        status = scheduler_service.get_status()
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logging.error(f"Error getting scheduler status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scheduler/interval', methods=['POST'])
def set_scheduler_interval():
    """Set scheduler interval"""
    try:
        data = request.get_json()
        minutes = data.get('minutes', 10)
        
        if minutes < 1:
            return jsonify({'success': False, 'error': 'Interval must be at least 1 minute'}), 400
        
        scheduler_service.set_interval(minutes)
        
        return jsonify({
            'success': True,
            'message': f'Scan interval updated to {minutes} minutes',
            'status': scheduler_service.get_status()
        })
        
    except Exception as e:
        logging.error(f"Error setting scheduler interval: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('../logs', exist_ok=True)
    
    # Start the application
    port = int(os.environ.get('SERVER_PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logging.info(f"Starting Social Media Lead Generator API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
