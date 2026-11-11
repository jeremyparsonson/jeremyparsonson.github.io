# Jeremy Parsonson — portfolio

Plain static site (HTML/CSS, no framework). Hosted free on GitHub Pages.

## Add your work

1. Put each project's images/videos in `assets/projects/<slug>/` (slugs are in `projects.json`). Files display in filename order, so name them `01-...`, `02-...`.
2. Optional: add `thumb.jpg` to a project folder for the hover preview on the home page.
3. Optional: add a `description` for any project in `projects.json`.
4. Run `python3 build.py` to regenerate the pages.

Cargo has no clean export, so save your media from the live site (or use your originals).

## Add work without touching a terminal

Once the repo is on GitHub, open `assets/projects/<slug>/` in the repo, click Add file > Upload files, and drag your images in. A GitHub Action (`.github/workflows/build.yml`) rebuilds the pages automatically within a minute or so. Max 25MB per file and 100 files per upload.

## Publish on GitHub Pages

1. Create a new repo, e.g. `jeremyparsonson.github.io` (or any name).
2. Push this folder to it:
   ```
   git init && git add . && git commit -m "Rebuild portfolio"
   git branch -M main
   git remote add origin git@github.com:<you>/<repo>.git
   git push -u origin main
   ```
3. Repo Settings > Pages > Source: deploy from branch `main`, folder `/ (root)`.
4. Custom domain: add it under Pages settings and point DNS at GitHub (a `CNAME` file is created for you). Then cancel Cargo.

## Edit text

Name, contact details, services, clients and experience live at the top of `build.py`.
