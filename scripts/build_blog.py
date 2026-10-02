#!/usr/bin/env python3
"""Build the static blog using Python's standard library.

The source format supports paragraphs, Markdown headings and simple lists.
All other text is escaped verbatim; no raw HTML, plugins or network access.
"""
import argparse
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://jerryzhou.ai'
STYLE_VERSION = '20261002-blog'


def render_body(source):
    blocks = [b.strip() for b in re.split(r'\n\s*\n', source.strip()) if b.strip()]
    output, headings = [], []
    active_list = None
    for block in blocks:
        heading = re.fullmatch(r'(#{2,3}) (.+)', block)
        ordered = re.fullmatch(r'(\d+)\.\s+(.+)', block)
        unordered = re.fullmatch(r'-\s+(.+)', block)
        list_type = 'ol' if ordered else 'ul' if unordered else None
        if active_list and list_type != active_list:
            output.append(f'</{active_list}>')
            active_list = None
        if list_type:
            if active_list is None:
                output.append(f'<{list_type}>')
                active_list = list_type
            text = ordered.group(2) if ordered else unordered.group(1)
            output.append(f'<li>{escape(text)}</li>')
        elif heading:
            level = len(heading.group(1))
            text = heading.group(2)
            anchor = f'section-{len(headings) + 1}'
            output.append(f'<h{level} id="{anchor}">{escape(text)}</h{level}>')
            headings.append((anchor, text, level))
        else:
            output.append(f'<p>{escape(block).replace(chr(10), "<br>")}</p>')
    if active_list:
        output.append(f'</{active_list}>')
    return '\n'.join(output), headings


def site_header():
    return '''<a class="skip-link" href="#main">跳到正文</a>
<header class="site-header"><div class="container header-inner">
<a class="brand" href="/">Jerry Zhou<span>周洁瑞</span></a>
<nav aria-label="主要导航"><a href="/">首页</a><a href="/blog/" aria-current="page">文章</a><a href="/#about">关于我</a><a class="nav-contact" href="/#contact">联系与合作 <span aria-hidden="true">↗</span></a></nav>
</div></header>'''


def footer():
    return '''<footer class="container site-footer"><div><a class="footer-brand" href="/">Jerry Zhou</a><span>洛杉矶 · 实践与思考</span></div><p>这里分享个人经验，不代表所在机构。<br>历史文章保留写作时的观点，不构成税务、法律或投资建议。</p><span class="copyright">© 2026 Jerry Zhou</span></footer>'''


def document(title, description, path, content, schema):
    schema_text = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f8f6ef">
<title>{escape(title)} | Jerry Zhou</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{BASE}{path}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="stylesheet" href="/styles.css?v=20260928-ucla">
<link rel="stylesheet" href="/blog.css?v={STYLE_VERSION}">
<meta property="og:type" content="{'article' if path != '/blog/' else 'website'}">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/assets/jerry-zhou.jpeg">
<meta property="og:locale" content="zh_CN"><meta name="twitter:card" content="summary">
<script type="application/ld+json">{schema_text}</script>
</head><body class="blog-page">
{site_header()}
{content}
{footer()}
</body></html>
'''


def source_date(post):
    if post.get('published_date'):
        return f'原文发表于 <time datetime="{post["published_date"]}">{post["published_date"]}</time>'
    return escape(post['original_date_label'])


def article(post, other):
    path = f'/blog/{post["slug"]}/'
    body, headings = render_body((ROOT / 'content' / post['body_file']).read_text())
    toc = '\n'.join(f'<li class="toc-level-{level}"><a href="#{anchor}">{escape(title)}</a></li>' for anchor, title, level in headings)
    content = f'''<main id="main" class="post-wrap">
<a class="back-link" href="/blog/">← 全部文章</a>
<article aria-labelledby="post-title">
<header class="post-header">
<p class="eyebrow">{escape(post['category'])} / NOTES FROM PRACTICE</p>
<h1 id="post-title">{escape(post['title'])}</h1>
<p class="post-source">原文首发于 <a href="{escape(post['source_url'], quote=True)}" target="_blank" rel="noopener noreferrer">Superlinear Academy <span aria-hidden="true">↗</span></a></p>
<div class="post-meta"><a class="post-author" href="/#about"><img src="/assets/jerry-zhou.jpeg" width="32" height="32" alt="">Jerry Zhou 周洁瑞</a><span>{source_date(post)}</span><span>本站收录 <time datetime="{post['republished_date']}">{post['republished_date']}</time></span></div>
<p class="archive-note">{escape(post['archive_note'])}</p>
</header>
<details class="post-toc"><summary>文章目录</summary><ol>{toc}</ol></details>
<div id="post-body" class="prose">{body}</div>
<footer class="post-end"><p>原文来源：<a href="{escape(post['source_url'], quote=True)}" target="_blank" rel="noopener noreferrer">Superlinear Academy</a> · 作者 Jerry Zhou</p><a href="#post-title">回到文章顶部 ↑</a></footer>
</article>
<aside class="post-contact" aria-labelledby="post-contact-title"><p class="eyebrow">LET’S TALK</p><h2 id="post-contact-title">想继续聊这个话题？</h2><p>有自己的经历、一个具体问题，或想探讨相关项目，都欢迎联系我。</p><div class="post-contact-links"><a class="button button-primary" href="/#contact">联系与合作 <span aria-hidden="true">↗</span></a><a href="https://www.instagram.com/jerryzhouu/" target="_blank" rel="noopener noreferrer">Instagram @jerryzhouu ↗</a><a href="/#wechat-contact">微信 jerryjoo ↗</a></div></aside>
<a class="next-post" href="/blog/{other['slug']}/"><span>继续阅读</span><strong>{escape(other['title'])}</strong><span aria-hidden="true">→</span></a>
</main>'''
    schema = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': post['title'], 'description': post['description'], 'author': {'@type': 'Person', 'name': 'Jerry Zhou', 'url': BASE + '/'}, 'url': BASE + path, 'mainEntityOfPage': BASE + path, 'isBasedOn': post['source_url'], 'inLanguage': 'zh-CN'}
    if post.get('published_date'):
        schema['datePublished'] = post['published_date']
    return document(post['title'], post['description'], path, content, schema)


def index(posts):
    items = []
    for number, post in enumerate(posts, 1):
        items.append(f'''<article class="blog-entry"><span class="entry-number">0{number}</span><div><div class="entry-meta"><span>{escape(post['category'])}</span><span>{source_date(post)}</span></div><h2><a href="/blog/{post['slug']}/">{escape(post['title'])} <span aria-hidden="true">→</span></a></h2><p>{escape(post['description'])}</p><p class="entry-source">原文首发于 Superlinear Academy · 本站收录正文</p></div></article>''')
    content = f'''<main id="main" class="blog-index container"><header class="blog-index-header"><p class="eyebrow">WRITING / 实践笔记</p><h1>一些经历，<br>一些想明白的事。</h1><p>关于房产、经营和技术实践。这里收录完整正文，<br class="desktop-break">每篇文章都保留原发布平台与原文链接。</p></header><div class="blog-entries">{''.join(items)}</div><div class="blog-index-end"><p>读完之后，也欢迎聊聊你的经历。</p><a class="text-link" href="/#contact">联系我 ↗</a></div></main>'''
    schema = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Jerry Zhou 的实践笔记', 'url': BASE + '/blog/', 'inLanguage': 'zh-CN', 'author': {'@type': 'Person', 'name': 'Jerry Zhou', 'url': BASE + '/'}, 'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': BASE + '/blog/' + p['slug'] + '/'} for p in posts]}
    return document('文章与实践笔记', 'Jerry Zhou 的房产、经营与技术实践文章。在本站阅读全文，并查看原始发布来源。', '/blog/', content, schema)


def outputs():
    posts = json.loads((ROOT / 'content/posts.json').read_text())
    if len(posts) != 2:
        raise ValueError('This two-post migration expects exactly two source posts.')
    result = {Path('blog/index.html'): index(posts)}
    for i, post in enumerate(posts):
        result[Path('blog') / post['slug'] / 'index.html'] = article(post, posts[1 - i])
    urls = ['/', '/blog/'] + ['/blog/' + p['slug'] + '/' for p in posts]
    result[Path('sitemap.xml')] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(f'<url><loc>{BASE}{url}</loc><lastmod>2026-10-02</lastmod></url>' for url in urls) + '\n</urlset>\n'
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Check generated pages without writing files')
    args = parser.parse_args()
    stale = []
    for relative, content in outputs().items():
        target = ROOT / relative
        if args.check:
            if not target.is_file() or target.read_text() != content:
                stale.append(str(relative))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    if stale:
        raise SystemExit('Generated files are stale: ' + ', '.join(stale))
    print('Blog pages and sitemap are current.' if args.check else 'Built two articles, the blog index and sitemap.')


if __name__ == '__main__':
    main()
