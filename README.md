# 🎙️ Podcast Feed Generator GitHub Action

This project automates the generation of an iTunes-compatible podcast RSS feed (`podcast.xml`) from a human-readable `feed.yaml` file using GitHub Actions.

---

## ✨ Features

- ✅ **YAML-driven Configuration**: Define podcast metadata and episodes easily in `feed.yaml`
- ⚙️ **GitHub Actions Integration**: Automatically generates and commits `podcast.xml`
- 🔁 **Auto-Updates on Push**: Rebuilds RSS feed when you update `feed.yaml`
- 📡 **iTunes/Apple Podcasts Compatible**: Fully standards-compliant RSS output
- 🤖 **(Optional) LLM Integration**: Automatically summarize or tag episodes using AI

---

## 🚀 How to Use

### 1. Create Your `feed.yaml`

Example structure:

```yaml
title: Your Podcast Title
author: Your Name
email: you@example.com
link: https://yourwebsite.com/podcast/
description: A short description of your show.
image: cover.jpg
language: en-us
category: Technology
format: Podcast

item:
  - title: Episode 1 - Hello World
    description: Introduction to the show!
    duration: 00:10:00
    published: Mon, 01 Jan 2024 12:00:00 GMT
    file: audio/episode1.mp3
    length: 12345678
