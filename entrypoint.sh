#!/bin/bash

echo "==================================="
echo "Starting Podcast Feed Generation Action"
echo "==================================="

# Configure Git with the committer's name and email
# GITHUB_ACTOR is the username of the person or app that triggered the workflow
# INPUT_EMAIL and INPUT_NAME are inputs defined in action.yml
git config --global user.name "${INPUT_NAME}" # Use INPUT_NAME from action.yml
git config --global user.email "${INPUT_EMAIL}" # Use INPUT_EMAIL from action.yml

# Add the workspace directory to Git's safe directories list
# This is important for security in GitHub Actions environments
git config --global --add safe.directory /github/workspace

# Execute the Python script to generate the podcast feed
# The script is copied to /usr/bin/feed.py in the Dockerfile
echo "Running Python script to generate podcast.xml..."
python3 /usr/bin/feed.py

# Check the exit status of the Python script
# If the script exited with a non-zero status (indicating an error),
# print an error message and exit the shell script with an error.
if [ $? -ne 0 ]; then
    echo "Error: Python script failed to generate 'podcast.xml'. Please check feed.yaml and script logs."
    exit 1 # Exit with an error code
fi

# Check if there are any changes to 'podcast.xml'
# 'git diff --quiet --exit-code' returns 0 if no differences, 1 if differences.
# We use '!' to invert the exit code, so the 'if' block runs if there ARE changes.
if ! git diff --quiet --exit-code podcast.xml; then
    echo "Changes detected in podcast.xml. Committing and pushing updates..."

    # Stage all changes in the repository (including podcast.xml)
    git add -A

    # Commit the changes with a descriptive message
    git commit -m "chore(feed): Update podcast feed [skip ci]"
    # "[skip ci]" is added to prevent an infinite loop of workflow runs
    # if this action is triggered by a push and then pushes back to the same branch.

    # Push the committed changes to the 'main' branch
    # '--set-upstream origin main' is used the first time to link local branch to remote
    git push --set-upstream origin main
    echo "Successfully committed and pushed 'podcast.xml' changes."
else
    echo "No changes detected in 'podcast.xml'. Skipping commit and push."
fi

echo "==================================="
echo "Podcast Feed Generation Action Finished"
echo "==================================="
