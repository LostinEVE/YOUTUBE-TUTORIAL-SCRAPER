"""Flask web application for YouTube Tutorial Scraper"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from youtube_scraper import YouTubeScraper
from database import TutorialDatabase
from config import PROGRAMMING_LANGUAGES, PROGRAMMING_SUBJECTS, MIN_VIDEO_DURATION_SECONDS

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
db = TutorialDatabase()

# Cache for scraper instance
scraper_instance = None


def get_scraper():
    """Get or create YouTube scraper instance"""
    global scraper_instance
    if scraper_instance is None:
        try:
            scraper_instance = YouTubeScraper()
        except ValueError:
            return None
    return scraper_instance


@app.route('/')
def index():
    """Home page with statistics"""
    summary = db.get_categories_summary()
    recent_tutorials = db.get_all_tutorials()[:10]
    return render_template('index.html',
                           summary=summary,
                           recent_tutorials=recent_tutorials)


@app.route('/scrape')
def scrape_page():
    """Scraping page"""
    return render_template('scrape.html',
                           languages=PROGRAMMING_LANGUAGES,
                           subjects=PROGRAMMING_SUBJECTS)


@app.route('/api/scrape', methods=['POST'])
def scrape_tutorials():
    """API endpoint to scrape tutorials"""
    scraper = get_scraper()
    if not scraper:
        return jsonify({
            'success': False,
            'error': 'YouTube API key not configured. Please set YOUTUBE_API_KEY environment variable.'
        }), 400

    data = request.get_json()
    scrape_type = data.get('type', 'all')
    language = data.get('language')
    subject = data.get('subject')

    tutorials = []

    try:
        if scrape_type == 'all':
            # Scrape all categories (simplified version)
            # Limit to first 5 to avoid timeouts
            for lang in PROGRAMMING_LANGUAGES[:5]:
                results = scraper.search_tutorials(language=lang)
                tutorials.extend(results)
        elif scrape_type == 'language' and language:
            tutorials = scraper.search_tutorials(language=language)
        elif scrape_type == 'subject' and subject:
            tutorials = scraper.search_tutorials(subject=subject)

        # Save to database
        added = 0
        duplicates = 0
        for tutorial in tutorials:
            if db.add_tutorial(tutorial):
                added += 1
            else:
                duplicates += 1

        return jsonify({
            'success': True,
            'added': added,
            'duplicates': duplicates,
            'total': len(tutorials)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/browse/languages')
def browse_languages():
    """Browse tutorials by programming language"""
    summary = db.get_categories_summary()
    return render_template('browse_languages.html',
                           languages=summary['by_language'])


@app.route('/browse/language/<language>')
def view_language(language):
    """View tutorials for a specific language"""
    tutorials = db.get_tutorials_by_language(language)
    return render_template('tutorials.html',
                           title=f'{language} Tutorials',
                           tutorials=tutorials)


@app.route('/browse/subjects')
def browse_subjects():
    """Browse tutorials by subject"""
    summary = db.get_categories_summary()
    return render_template('browse_subjects.html',
                           subjects=summary['by_subject'])


@app.route('/browse/subject/<subject>')
def view_subject(subject):
    """View tutorials for a specific subject"""
    tutorials = db.get_tutorials_by_subject(subject)
    return render_template('tutorials.html',
                           title=f'{subject} Tutorials',
                           tutorials=tutorials)


@app.route('/search')
def search():
    """Search tutorials"""
    query = request.args.get('q', '')
    if query:
        tutorials = db.search_tutorials(query)
        return render_template('tutorials.html',
                               title=f'Search results for "{query}"',
                               tutorials=tutorials,
                               search_query=query)
    return render_template('search.html')


@app.route('/favorites')
def favorites():
    """View favorite tutorials"""
    tutorials = [t for t in db.get_all_tutorials() if t.get('is_favorite')]
    return render_template('tutorials.html',
                           title='Favorite Tutorials',
                           tutorials=tutorials)


@app.route('/all')
def all_tutorials():
    """View all tutorials"""
    page = request.args.get('page', 1, type=int)
    per_page = 50

    all_tuts = db.get_all_tutorials()
    total = len(all_tuts)
    start = (page - 1) * per_page
    end = start + per_page

    tutorials = all_tuts[start:end]
    total_pages = (total + per_page - 1) // per_page

    return render_template('tutorials.html',
                           title='All Tutorials',
                           tutorials=tutorials,
                           page=page,
                           total_pages=total_pages)


@app.route('/statistics')
def statistics():
    """View statistics"""
    summary = db.get_categories_summary()
    return render_template('statistics.html', summary=summary)


@app.route('/api/favorite/<video_id>', methods=['POST'])
def toggle_favorite(video_id):
    """Toggle favorite status"""
    data = request.get_json()
    is_favorite = data.get('is_favorite', True)
    db.mark_favorite(video_id, is_favorite)
    return jsonify({'success': True})


@app.route('/api/watched/<video_id>', methods=['POST'])
def mark_watched(video_id):
    """Mark tutorial as watched"""
    db.mark_watched(video_id)
    return jsonify({'success': True})


@app.route('/settings')
def settings():
    """View settings"""
    return render_template('settings.html',
                           languages=PROGRAMMING_LANGUAGES,
                           subjects=PROGRAMMING_SUBJECTS,
                           min_duration=MIN_VIDEO_DURATION_SECONDS)


@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
