# Blog maintenance

The website is a static GitHub Pages site. The blog is generated ahead of time; reading articles requires no JavaScript, community login, or runtime service.

## Content and rendering

- `content/posts.json` owns public titles, source URLs, date labels, descriptions and source-file paths.
- `content/*.md` owns the article bodies. The migrated bodies retain the original wording, including original spelling and section numbering.
- `scripts/build_blog.py` renders the two imported articles, `/blog/` and `sitemap.xml` using only Python's standard library.
- The source format supports paragraphs, `##` / `###` headings, simple lists, inline HTTPS links, local PNG images (`![alt](/assets/path.png)`) and YouTube video blocks (`[视频：title](https://www.youtube.com/watch?v=VIDEO_ID)`). Other text is escaped literally. This is a small importer, not a complete Markdown engine.
- `blog.css` extends the existing site styles. Source links appear directly below every article title.

```sh
python3 scripts/build_blog.py
python3 scripts/build_blog.py --check
```

For another article, extend the post registry and the current two-post count / related-article selection in the generator. Rebuild and check the complete source text, internal links, attribution, mobile layout and sitemap before publishing.

## Provenance

Both articles were originally published by Jerry Zhou on Superlinear Academy. The initial import used full-text archives saved on 2026-07-18. On 2026-10-02 the real-estate article was checked against the signed-in original: its text matched, four original-resolution PNGs were copied to `assets/blog/us-real-estate-investing/`, the original introduction link was restored, and the original public YouTube video was embedded in place. The development retrospective remains based on the stored text archive; its current media inventory has not been checked.

The real-estate article's original date is confirmed as 2024-08-15. The development retrospective's original page displayed `Jan 11`; its year is unconfirmed and is omitted from structured `datePublished` metadata. The current republication date is distinct from the original publication date.

Only public article content and public source metadata belong in this repository. Keep private archive frontmatter, local paths, credentials, community comments and session exports out of the generated site.
