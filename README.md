# 🎙️ Podcast Feed Generator

This GitHub Action generates an **iTunes-compatible podcast RSS feed** (`podcast.xml`) from a human-readable YAML configuration file (`feed.yaml`). It's designed to automate the creation and update of podcast feeds directly within your repository.

---

## ✨ Features

- ✅ Parses structured podcast metadata from `feed.yaml`
- 📄 Generates `podcast.xml` RSS feed using iTunes standards
- 🔁 Automatically commits and pushes feed updates to the repository
- 🐳 Dockerized and GitHub Actions compatible
- 🔒 Safe Git configuration with user-supplied name and email

---

## 📂 Usage

```yaml
# .github/workflows/generate-podcast.yml
name: Generate Podcast Feed

on:
  push:
    paths:
      - feed.yaml
      - .github/workflows/generate-podcast.yml

jobs:
  generate-feed:
    runs-on: ubuntu-latest
    name: Generate & Commit podcast.xml
    steps:
      - uses: actions/checkout@v3

      - name: Run Podcast Generator
        uses: your-username/podcast-generator@main
        with:
          email: ${{ github.actor }}@users.noreply.github.com
          name: ${{ github.actor }}
