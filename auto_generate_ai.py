#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, datetime, subprocess, random, requests, re, time

GITHUB_USER = "1shisan"
GITHUB_TOKEN = "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"
YOUR_DOMAIN = "ai.chenqiwx.cn"
REPO_NAME = "1shisan.github.io"
ADSENSE_ID = "ca-pub-xxxxxxxxxxxxxxxx"
DEEPSEEK_API_KEY = "sk-71eebeb3498d4bde8c370f34573e4c81"

REPO_PATH = "/www/" + REPO_NAME
API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

ARTICLE_TOPICS = [
    "Best AI Tools for {niche} in 2026 - A Complete Review",
    "How {tool} Is Changing the Way {task} Works in 2026",
    "{tool} vs {competitor}: Which AI Tool Is Better in 2026?",
    "Is {tool} Worth It in 2026? An Honest Review",
    "Top 5 Features of {tool} That Make It Stand Out in 2026",
]

NICHES = [
    "Freelancers", "Small Business Owners", "Content Creators",
    "Software Developers", "Digital Marketers", "Data Analysts",
    "Graphic Designers", "Video Editors", "Writers", "Entrepreneurs",
    "Social Media Managers", "E-commerce Stores"
]

TOOLS = [
    ("ChatGPT", "conversational AI"),
    ("Midjourney", "AI image generation"),
    ("Claude", "AI writing and analysis"),
    ("GitHub Copilot", "AI programming"),
    ("Notion AI", "productivity"),
    ("Perplexity", "AI-powered research"),
    ("Runway", "AI video generation"),
    ("ElevenLabs", "AI voice generation"),
    ("Jasper", "AI content writing"),
    ("Canva AI", "AI-powered design"),
    ("Gamma", "AI presentation creation"),
    ("Suno", "AI music generation"),
]

COMPETITOR_PAIRS = [
    ("ChatGPT", "Claude"), ("Midjourney", "DALL-E 4"),
    ("GitHub Copilot", "Cursor"), ("Notion AI", "Motion"),
    ("Jasper", "Writesonic"), ("Perplexity", "Gemini"),
    ("Runway", "Pika"), ("ElevenLabs", "Murf"),
]

def pick_topic():
    pattern = random.choice(ARTICLE_TOPICS)
    if "{niche}" in pattern:
        return pattern.format(niche=random.choice(NICHES))
    elif "{competitor}" in pattern:
        t1, t2 = random.choice(COMPETITOR_PAIRS)
        return pattern.format(tool=t1, competitor=t2)
    elif "{tool}" in pattern and "{task}" in pattern:
        tool, task_desc = random.choice(TOOLS)
        return pattern.format(tool=tool, task=task_desc)
    else:
        tool, _ = random.choice(TOOLS)
        return pattern.replace("{tool}", tool)

def call_deepseek(prompt):
    headers = {
        "Authorization": "Bearer " + DEEPSEEK_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert AI tools reviewer. Write in English. Use professional tone. Include data points. Use ## headings and bullet points. Write 500-600 words. No code blocks. Do not mention being AI."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 3500
    }
    print("  Calling DeepSeek API...")
    resp = requests.post(API_URL, headers=headers, json=data, timeout=120)
    if resp.status_code != 200:
        raise Exception("API failed: " + str(resp.status_code))
    return resp.json()["choices"][0]["message"]["content"]

def extract_title_and_content(ai_text):
    lines = ai_text.strip().split('\n')
    title = None
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('## '):
            title = line.strip().replace('## ', '').strip()
            start = i + 1
            break
        if line.strip().startswith('# '):
            title = line.strip().replace('# ', '').strip()
            start = i + 1
            break
    if not title:
        for i, line in enumerate(lines):
            if line.strip():
                title = line.strip().rstrip('.')
                start = i + 1
                break
    if not title:
        title = "Latest AI Tool Review"
    body = '\n'.join(lines[start:]).strip()
    body = re.sub(r'^#\s+.*$', '', body, flags=re.MULTILINE).strip()
    return title, body

def text_to_html(title, body_text, now, filename):
    parts = []
    for line in body_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('## '):
            parts.append('<h2>' + line[3:] + '</h2>')
        elif line.startswith('- ') or line.startswith('* '):
            parts.append('<li>' + line[2:] + '</li>')
        else:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            parts.append('<p>' + line + '</p>')
    body_html = '\n                '.join(parts)
    kw = filename.replace(".html", "").replace("-", ", ")

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + title + ''' - AI Tool Scout</title>
    <meta name="description" content="Read our expert review of ''' + title + '''.">
    <meta name="keywords" content="''' + kw + '''">
    <link rel="canonical" href="https://''' + YOUR_DOMAIN + '/' + filename + '''">
    <link rel="stylesheet" href="style.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=''' + ADSENSE_ID + '''" crossorigin="anonymous"></script>
</head>
<body>
    <header class="site-header">
        <div class="container header-inner">
            <a href="/" class="logo">AI Tool Scout</a>
            <nav class="nav-links">
                <a href="/">Home</a>
                <a href="/top-ai-tools-2026.html" class="active">Reviews</a>
                <a href="/about.html">About</a>
                <a href="/contact.html">Contact</a>
                <a href="/privacy.html">Privacy</a>
            </nav>
        </div>
    </header>
    <section class="article-header-section">
        <div class="container article-header-content">
            <div class="article-meta-top">
                <span class="post-category">Reviews</span>
                <span class="post-date">''' + now + '''</span>
            </div>
            <h1>''' + title + '''</h1>
            <p class="article-subtitle">An in-depth, honest review based on real testing and analysis.</p>
            <div class="article-author">
                <div class="author-avatar">AS</div>
                <div><strong>By AI Tool Scout Team</strong> <span class="post-date">''' + now + '''</span></div>
            </div>
        </div>
    </section>
    <div class="content-row container">
        <main class="main-content article-main">
            <article class="article-body">
                ''' + body_html + '''
            </article>
            <div class="article-footer-disclaimer">
                <p><strong>Disclosure:</strong> Some links are affiliate links. Opinions remain our own.</p>
            </div>
        </main>
        <aside class="sidebar">
            <div class="sidebar-card">
                <h3>About</h3>
                <p>Independent reviews since 2025.</p>
                <a href="/about.html" class="sidebar-link">Learn more</a>
            </div>
            <div class="sidebar-card">
                <h3>Top Picks 2026</h3>
                <ul class="sidebar-list">
                    <li><strong>ChatGPT Pro</strong> - Best All-Rounder</li>
                    <li><strong>Midjourney v7</strong> - Best Image Gen</li>
                    <li><strong>Claude 4</strong> - Best for Writing</li>
                    <li><strong>Copilot X</strong> - Best for Coding</li>
                </ul>
            </div>
            <div class="sidebar-ad">
                <ins class="adsbygoogle" style="display:block" data-ad-client="''' + ADSENSE_ID + '''" data-ad-slot="xxxxxxxxxx" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </aside>
    </div>
    <footer class="site-footer">
        <div class="container footer-grid">
            <div><h4>AI Tool Scout</h4><p>Independent reviews since 2025.</p></div>
            <div><h4>Links</h4><a href="/">Home</a><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/privacy.html">Privacy</a></div>
            <div><h4>Disclaimer</h4><p>Some links are affiliate links.</p></div>
        </div>
        <div class="container footer-bottom"><p>&copy; 2026 AI Tool Scout. All rights reserved.</p></div>
    </footer>
</body>
</html>'''
    return html

def generate():
    print("Generating article...")
    now = datetime.datetime.now().strftime("%B %d, %Y")
    topic = pick_topic()
    print("Topic: " + topic)
    prompt = ('Write a review article titled: "' + topic + '"\n\n'
              'Include: intro, overview, features, pricing, pros and cons, verdict.\n'
              'Use ## headings and bullet points. 500 words. Professional tone. No code blocks.')
    try:
        text = call_deepseek(prompt)
        print("  OK (" + str(len(text)) + " chars)")
    except Exception as e:
        print("  Failed: " + str(e))
        return
    title, body = extract_title_and_content(text)
    print("  Title: " + title)
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
    filename = slug + "-" + str(random.randint(10,99)) + ".html"
    html = text_to_html(title, body, now, filename)
    with open(os.path.join(REPO_PATH, filename), 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Saved")
    jp = os.path.join(REPO_PATH, 'articles.json')
    with open(jp, 'r', encoding='utf-8') as f:
        arts = json.load(f)
    excerpt = (body[:150].replace('\n', ' ').strip() + '...') if len(body) > 150 else body
    arts.insert(0, {"id": filename.replace(".html",""), "title": title, "excerpt": excerpt,
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=80",
        "url": "/" + filename, "date": now, "category": "Reviews", "featured": False,
        "keywords": slug.replace("-", ", ")})
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(arts, f, indent=4)
    print("  articles.json updated")
    try:
        os.chdir(REPO_PATH)
        subprocess.run(['git', 'add', filename], check=True)
        subprocess.run(['git', 'add', 'articles.json'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Auto: ' + title], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("  Pushed")
    except Exception as e:
        print("  Git error: " + str(e))
    print("Done! https://" + YOUR_DOMAIN + "/" + filename)

if __name__ == '__main__':
    generate()