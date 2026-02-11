from flask import Flask, render_template, send_file, request, make_response, url_for, Response
from flask_babel import Babel, _, gettext
import json
import os
import pdfkit
import gettext as python_gettext
import markdown
from models import Person

app = Flask(__name__)

def get_locale():
    # Check if 'lang' argument is present
    lang = request.args.get('lang')
    if lang in ['en', 'hu']:
        return lang
    # Otherwise, try to guess from the browser
    return request.accept_languages.best_match(['en', 'hu']) or 'en'

babel = Babel(app, locale_selector=get_locale)

# Domains for translations
DOMAINS = ['ui', 'personal', 'experience', 'education', 'languages', 'skills']

def translate_all_domains(message):
    if not message:
        return ""
    
    lang = get_locale()
    if lang == 'en':
        return message

    for domain in DOMAINS:
        translation = python_gettext.translation(domain, localedir='translations', languages=[lang], fallback=True)
        translated = translation.gettext(message)
        if translated != message:
            return translated
    
    return message

def load_json(filename):
    path = os.path.join('data', f"{filename}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_items(folder):
    items = []
    folder_path = os.path.join('data', folder)
    if not os.path.exists(folder_path):
        return items
    
    # Get all item files
    item_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    for filename in item_files:
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
            items.append(json.load(f))
    
    # Sort items by start_date descending (newest first)
    items.sort(key=lambda x: x.get('start_date', ''), reverse=True)
    return items

def load_solutions():
    solutions = []
    base_path = os.path.join('data', 'solutions')
    if not os.path.exists(base_path):
        return solutions
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            manifest_path = os.path.join(folder_path, 'manifest.json')
            readme_path = os.path.join(folder_path, 'README.md')
            
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if os.path.exists(readme_path):
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        data['description'] = f.read().strip()
                
                solutions.append(data)
    
    solutions.sort(key=lambda x: x.get('order', 999))
    return solutions

def get_all_data():
    personal_data = load_json('personal')
    personal = Person(personal_data, app.static_folder, lang=get_locale())
    return {
        'personal': personal,
        'experience': load_items('experience'),
        'skills': load_json('skills'),
        'education': load_items('education'),
        'languages': load_json('languages'),
        'lang': get_locale()
    }

@app.route('/')
def index():
    data = get_all_data()
    return render_template('index.html', **data)

@app.route('/contact.vcf')
def contact_vcf():
    data = load_json('personal')
    person = Person(data, app.static_folder, lang=get_locale())

    vcard_content = person.generate_vcard()

    response = make_response(vcard_content)
    response.headers['Content-Type'] = 'text/vcard; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename={person.full_name}.vcf'

    return response

@app.route('/solutions')
def solutions():
    offerings = load_solutions()
    data = get_all_data()
    return render_template('solutions.html', offerings=offerings, **data)

@app.route('/cv')
def cv():
    data = get_all_data()
    return render_template('cv.html', **data)

@app.route('/contact')
def contact():
    data = get_all_data()
    return render_template('contact.html', **data)

@app.route('/cv.pdf')
def cv_pdf():
    # Force locale for PDF generation if needed, or use get_locale()
    lang = get_locale()
    data = get_all_data()
    data['profile_image_base64'] = f"data:image/png;base64,{data['personal'].get_photo_b64()}"
    
    # Load CSS for inlining in PDF
    css_path = os.path.join(app.static_folder, 'css', 'cv.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        data['pdf_css'] = f.read()
    
    # We need to ensure that when rendering for PDF, we are in the correct locale context.
    # Flask-Babel usually handles this via get_locale, which checks request.args
    rendered = render_template('cv.html', **data, is_pdf=True)
    
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'quiet': ''
    }
    
    pdf = pdfkit.from_string(rendered, False, options=options)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={data["personal"].full_name} CV ({lang}).pdf'
    
    return response

@app.context_processor
def inject_translate():
    return {
        '_': translate_all_domains,
        'markdown': lambda text: markdown.markdown(text) if text else ""
    }

@app.route('/sitemap.xml')
def sitemap():
    host = 'https://nurefexc.com'
    langs = ['en', 'hu']
    paths = ['/', '/cv', '/contact', '/solutions', '/contact.vcf']

    urlset_items = []
    for lang in langs:
        for p in paths:
            loc = f"{host}{p}"
            # keep language param to provide alternates per language
            sep = '&' if '?' in loc else '?'
            loc_lang = f"{loc}{sep}lang={lang}"
            urlset_items.append(f"    <url>\n        <loc>{loc_lang}</loc>\n        <changefreq>weekly</changefreq>\n        <priority>0.8</priority>\n    </url>")

    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
""".format(items='\n'.join(urlset_items))

    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return response

@app.route('/robots.txt')
def robots_txt():
    host = 'https://nurefexc.com'
    content = f"""User-agent: *
Allow: /
Sitemap: {host}/sitemap.xml
"""
    return Response(content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
