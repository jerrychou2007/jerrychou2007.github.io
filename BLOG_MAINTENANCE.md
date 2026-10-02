# Blog maintenance

The website is a static GitHub Pages site. The blog is generated ahead of time; reading articles requires no JavaScript, community login, or runtime service.

## Content and rendering

- `content/posts.json` owns public titles, source URLs, date labels, descriptions and source-file paths.
- `content/*.md` owns the article bodies. The migrated bodies retain the original wording, including original spelling and section numbering.
- `scripts/build_blog.py` renders the two imported articles, `/blog/` and `sitemap.xml` using only Python's standard library.
- The source format supports paragraphs, `##` / `###` headings and simple ordered / unordered lists. Other text is escaped literally. This is a small importer, not a complete Markdown engine.
- `blog.css` extends the existing site styles. Source links appear directly below every article title.

```sh
python3 scripts/build_blog.py
python3 scripts/build_blog.py --check
```

For another article, extend the post registry and the current two-post count / related-article selection in the generator. Rebuild and check the complete source text, internal links, attribution, mobile layout and sitemap before publishing.

## Provenance

Both articles were originally published by Jerry Zhou on Superlinear Academy. This import uses full-text archives saved on 2026-07-18. The original platform currently requires sign-in, so this release does not claim a fresh media inventory or verification of current platform edits.

The real-estate article's original date is confirmed as 2024-08-15. The development retrospective's original page displayed `Jan 11`; its year is unconfirmed and is omitted from structured `datePublished` metadata. The current republication date is distinct from the original publication date.

Only public article content and public source metadata belong in this repository. Keep private archive frontmatter, local paths, credentials, community comments and session exports out of the generated site.
