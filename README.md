name: "Podcast Generator"
author: "Ray Villalobos"
description: "Generates a podcast feed from a YAML file"
runs:
  using: "docker"
  image: "Dockerfile"
branding:
  icon: "git-branch" # You can choose from available Octicons (e.g., 'git-branch', 'rss', 'file-code')
  color: "red" # Choose a color: 'blue', 'green', 'orange', 'purple', 'red', 'yellow'
inputs:
  email:
    description: "The committer's email address for Git operations."
    required: true
    default: ${{ github.actor }}@users.noreply.github.com # Standard GitHub Actions email
  name:
    description: "The committer's name for Git operations."
    required: true
    default: ${{ github.actor }} # The GitHub actor (username)
