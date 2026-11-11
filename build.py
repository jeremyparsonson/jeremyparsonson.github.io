#!/usr/bin/env python3
"""Static site generator for jeremyparsonson portfolio.

Usage:  python3 build.py

Drop images/videos for each project into  assets/projects/<slug>/  (sorted by
filename, so 01-..., 02-... works well). Put a file named  thumb.jpg  (or .png /
.webp) in the same folder to get a hover preview on the home page. Re-run this
script, commit, push.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
ASSETS = ROOT / "assets" / "projects"
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"}
VID_EXT = {".mp4", ".webm", ".mov"}

SITE = {
    "name": "Jeremy Parsonson",
    "role": "Senior Designer",
    "email": "jeparsonson@gmail.com",
    "phone": "+44 7733 787278",
    "linkedin": "https://www.linkedin.com/in/jeremy-parsonson-223013231/",
    "description": "Jeremy Parsonson, Senior Designer. Brand identity, campaigns, digital and motion.",
    "updated": "25.11.11",
}
SERVICES = ["Graphic Design", "Web Design", "Illustration", "Animation", "Brand Identity"]
CLIENTS = [
    "Land Rover", "Jaguar", "Rae Morris", "Volkswagen", "BYD", "Hastings Deering",
    "Wahl", "Toyota", "MG", "Mercedes-Benz CV (2017-today)",
]
EXPERIENCE = ["REP. Agency, Brisbane", "Soak Creative, Brisbane", "VALD, Brisbane", "Eagers Automotive, Brisbane"]

e = html.escape


def head(title, depth, desc=None):
    p = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc or SITE['description'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc or SITE['description'])}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{p}site.css">
</head>
<body>
"""


def header(depth, current):
    p = "../" * depth
    def cur(k):
        return ' aria-current="page"' if k == current else ""
    return f"""<header class="site-header">
  <a class="name" href="{p}index.html">{e(SITE['name'])}, {e(SITE['role'])}</a>
  <nav>
    <a href="{p}index.html#work"{cur('work')}>Projects</a>
    <a href="{p}information.html"{cur('info')}>Info</a>
  </nav>
  <nav>
    <a href="mailto:{SITE['email']}">Email</a>
    <a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a>
  </nav>
</header>
<main>
"""


def footer(depth):
    return f"""</main>
<footer class="site-footer">
  <a href="#">&uarr; Top</a>
  <span>Updated {SITE['updated']}</span>
</footer>
"""


def media_for(slug):
    folder = ASSETS / slug
    if not folder.is_dir():
        return [], None
    files = sorted(f for f in folder.iterdir() if f.is_file())
    thumb = None
    items = []
    for f in files:
        if f.stem.lower() == "thumb" and f.suffix.lower() in IMG_EXT:
            thumb = f"assets/projects/{slug}/{f.name}"
            continue
        if f.suffix.lower() in IMG_EXT | VID_EXT:
            items.append(f)
    return items, thumb


def build_home(projects):
    rows = []
    thumbs = {}
    for i, pr in enumerate(projects, 1):
        _, thumb = media_for(pr["slug"])
        attr = f' data-thumb="{e(thumb)}"' if thumb else ""
        rows.append(
            f'    <li><a href="projects/{e(pr["slug"])}.html"{attr}>'
            f'<span>{e(pr["title"])}</span><span class="idx">{i:02d}</span></a></li>'
        )
    out = head(SITE["name"], 0)
    out += header(0, "work")
    out += f"""<h1 class="hero">I work with clients and agencies to shape desirable brands and exciting creative</h1>
<a class="cta" href="mailto:{SITE['email']}">Get in touch</a>
<h2 class="section-label" id="work">A collection of work</h2>
<ul class="work-list">
{chr(10).join(rows)}
</ul>
<img class="preview" alt="" aria-hidden="true">
<script>
(function () {{
  var img = document.querySelector('.preview');
  document.querySelectorAll('.work-list a[data-thumb]').forEach(function (a) {{
    a.addEventListener('mouseenter', function () {{ img.src = a.dataset.thumb; img.classList.add('on'); }});
    a.addEventListener('mouseleave', function () {{ img.classList.remove('on'); }});
    a.addEventListener('mousemove', function (ev) {{ img.style.left = ev.clientX + 'px'; img.style.top = ev.clientY + 'px'; }});
  }});
}})();
</script>
"""
    out += footer(0) + "</body>\n</html>\n"
    (ROOT / "index.html").write_text(out, encoding="utf-8")


def build_info():
    lis = lambda xs: "\n".join(f"      <li>{e(x)}</li>" for x in xs)
    out = head("Information — " + SITE["name"], 0)
    out += header(0, "info")
    out += f"""<section class="info">
  <p class="lede">I’m always excited about new opportunities. Let’s talk!</p>
  <div class="col contact">
    <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a><br>
    <a href="tel:{SITE['phone'].replace(' ', '')}">{e(SITE['phone'])}</a>
  </div>
  <div class="col"><h2>Services</h2><ul>
{lis(SERVICES)}
  </ul></div>
  <div class="col"><h2>Clients</h2><ul>
{lis(CLIENTS)}
  </ul></div>
  <div class="col"><h2>Experience</h2><ul>
{lis(EXPERIENCE)}
  </ul></div>
</section>
"""
    out += footer(0) + "</body>\n</html>\n"
    (ROOT / "information.html").write_text(out, encoding="utf-8")


def build_project(i, pr, projects):
    slug = pr["slug"]
    items, _ = media_for(slug)
    blocks = []
    for f in items:
        src = f"../assets/projects/{slug}/{f.name}"
        if f.suffix.lower() in VID_EXT:
            blocks.append(f'  <video src="{e(src)}" autoplay muted loop playsinline></video>')
        else:
            blocks.append(f'  <img src="{e(src)}" alt="{e(pr["title"])}" loading="lazy">')
    if not blocks:
        blocks.append(f'  <div class="empty">Add images to assets/projects/{e(slug)}/ and re-run build.py</div>')
    prev_p = projects[i - 1]
    next_p = projects[(i + 1) % len(projects)]
    desc = f'<p class="desc">{e(pr["description"])}</p>' if pr.get("description") else ""
    out = head(f'{pr["title"]} — {SITE["name"]}', 1)
    out += header(1, "work")
    out += f"""<article class="project">
  <h1>{e(pr['title'])}</h1>
  {desc}
  <div class="gallery">
{chr(10).join(blocks)}
  </div>
  <div class="pager">
    <a href="{e(prev_p['slug'])}.html">&larr; {e(prev_p['title'])}</a>
    <a href="{e(next_p['slug'])}.html">{e(next_p['title'])} &rarr;</a>
  </div>
</article>
"""
    out += footer(1) + "</body>\n</html>\n"
    (ROOT / "projects").mkdir(exist_ok=True)
    (ROOT / "projects" / f"{slug}.html").write_text(out, encoding="utf-8")


def build_404():
    out = head("Not found — " + SITE["name"], 0)
    out = out.replace('href="site.css"', 'href="/site.css"')
    out += header(0, None).replace('href="index.html', 'href="/index.html').replace('href="information.html', 'href="/information.html')
    out += '<h1 class="hero">Page not found</h1>\n<a class="cta" href="/index.html">Back home</a>\n'
    out += footer(0) + "</body>\n</html>\n"
    (ROOT / "404.html").write_text(out, encoding="utf-8")


def main():
    projects = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    for pr in projects:
        (ASSETS / pr["slug"]).mkdir(parents=True, exist_ok=True)
    build_home(projects)
    build_info()
    for i, pr in enumerate(projects):
        build_project(i, pr, projects)
    build_404()
    print(f"Built {len(projects)} project pages + home, info, 404.")


if __name__ == "__main__":
    main()
