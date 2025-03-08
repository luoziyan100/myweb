#!/usr/bin/env python
"""
Editor for published blog posts.
Usage: python edit-post.py <html_file_path>

This script finds the original Markdown source for an HTML blog post,
opens it for editing, and then regenerates the HTML after editing is complete.
"""

import sys
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from bs4 import BeautifulSoup

# Directories
BLOG_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSTS_DIR = BLOG_ROOT / "blog-content" / "posts"
DRAFTS_DIR = BLOG_ROOT / "blog-content" / "drafts"
PUBLISHED_DIR = BLOG_ROOT / "blog-content" / "published"

def find_markdown_source(html_path):
    """Find the original Markdown source file for an HTML blog post."""
    try:
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML to extract title
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('h1', class_='blog-post-title')
        
        if not title_tag:
            title_tag = soup.find('title')
            
        if title_tag:
            title = title_tag.text.strip()
            print(f"Found blog post title: {title}")
            
            # Search for matching Markdown files
            for dir_path in [POSTS_DIR, DRAFTS_DIR]:
                for file in dir_path.glob("*.md"):
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check if title is in front matter
                    if f'title: "{title}"' in content or f"title: '{title}'" in content:
                        print(f"Found matching Markdown source: {file}")
                        return file
                        
                    # Also check if title is in the first few lines (# Title format)
                    first_lines = '\n'.join(content.split('\n')[:20])
                    if f"# {title}" in first_lines:
                        print(f"Found matching Markdown source: {file}")
                        return file
            
            # If not found by title, try by filename pattern
            html_filename = Path(html_path).name
            if html_filename.endswith('.html'):
                base_name = html_filename[:-5]  # Remove .html
                
                # Check for date pattern like YYYY-MM-DD
                if re.match(r'^\d{4}-\d{2}-\d{2}', base_name):
                    for dir_path in [POSTS_DIR, DRAFTS_DIR]:
                        for file in dir_path.glob(f"{base_name}*.md"):
                            print(f"Found matching Markdown source by filename: {file}")
                            return file
                            
                # For blog-post1.html type patterns, search by content comparison
                elif re.match(r'^blog-post\d+$', base_name):
                    # Read the HTML content (stripping tags)
                    plain_text = re.sub(r'<[^>]+>', '', html_content)
                    plain_text = plain_text.strip()[:500]  # First 500 chars
                    
                    # Check all md files for content similarity
                    for dir_path in [POSTS_DIR, DRAFTS_DIR]:
                        for file in dir_path.glob("*.md"):
                            with open(file, 'r', encoding='utf-8') as f:
                                md_content = f.read()
                            
                            # Strip YAML front matter
                            md_content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', md_content, flags=re.DOTALL)
                            md_plain = md_content.strip()[:500]  # First 500 chars
                            
                            # Simple similarity check - could be improved
                            common_words = set(plain_text.split()) & set(md_plain.split())
                            if len(common_words) > 20:  # If enough common words
                                print(f"Found likely matching Markdown source: {file}")
                                return file
        
        print("Could not find matching Markdown source file.")
        return None
        
    except Exception as e:
        print(f"Error finding Markdown source: {e}")
        return None

def open_editor(file_path):
    """Open a file in the default editor."""
    try:
        if sys.platform == 'win32':
            os.startfile(file_path)
        elif sys.platform == 'darwin':  # macOS
            subprocess.call(['open', file_path])
        else:  # Linux and other Unix-like
            subprocess.call(['xdg-open', file_path])
        
        print(f"\nOpened {file_path} in your default editor.")
        print("Edit the file, save it, and then return to this terminal.")
        input("Press Enter when you've finished editing to regenerate the HTML... ")
        
        return True
    except Exception as e:
        print(f"Error opening editor: {e}")
        return False

def regenerate_html(md_path, html_path):
    """Regenerate HTML from Markdown and update the published file."""
    try:
        # First check if the file is in drafts and should be moved to posts
        if DRAFTS_DIR in str(md_path):
            move_to_posts = input("This file is in drafts. Move it to posts? (y/n): ").lower().strip()
            if move_to_posts == 'y':
                new_path = POSTS_DIR / md_path.name
                md_path.rename(new_path)
                md_path = new_path
                print(f"Moved to {md_path}")
        
        # Generate a temporary HTML file first
        temp_html = PUBLISHED_DIR / f"temp_{int(time.time())}.html"
        
        # Run the md-to-html.py script
        md_to_html_script = BLOG_ROOT / "blog-content" / "md-to-html.py"
        cmd = [sys.executable, str(md_to_html_script), str(md_path), str(temp_html)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running md-to-html.py: {result.stderr}")
            return False
        
        print(f"Successfully regenerated HTML to {temp_html}")
        
        # Copy to the actual HTML blog post
        with open(temp_html, 'r', encoding='utf-8') as f:
            new_html_content = f.read()
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)
        
        # Clean up the temp file
        os.remove(temp_html)
        
        print(f"Successfully updated {html_path}")
        return True
        
    except Exception as e:
        print(f"Error regenerating HTML: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python edit-post.py <html_file_path>")
        sys.exit(1)
    
    html_path = sys.argv[1]
    if not os.path.exists(html_path):
        print(f"Error: File {html_path} does not exist")
        sys.exit(1)
    
    print(f"Looking for Markdown source for {html_path}...")
    md_path = find_markdown_source(html_path)
    
    if not md_path:
        create_new = input("No existing Markdown source found. Create a new one? (y/n): ").lower().strip()
        if create_new == 'y':
            # Extract content from HTML and create a new Markdown file
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract title
                title_tag = soup.find('h1', class_='blog-post-title')
                title = title_tag.text.strip() if title_tag else "Blog Post"
                
                # Extract date
                date_tag = soup.select('.blog-post-meta span:first-child')
                date_text = date_tag[0].text.strip() if date_tag else ""
                # Convert Chinese date format to YYYY-MM-DD
                date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_text)
                if date_match:
                    year, month, day = date_match.groups()
                    date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                else:
                    date = time.strftime("%Y-%m-%d")
                
                # Extract author
                author_tag = soup.select('.blog-post-meta span:nth-child(2)')
                author = author_tag[0].text.strip() if author_tag else "yan"
                
                # Extract tags
                tags = []
                tag_spans = soup.select('.blog-post-tag')
                for span in tag_spans:
                    tags.append(span.text.strip())
                
                # Extract content
                content_div = soup.find('article', class_='blog-post-content')
                if content_div:
                    # This is a very basic HTML to Markdown conversion
                    # For better results, consider using html2text or similar libraries
                    content = content_div.get_text('\n\n')
                else:
                    content = ""
                
                # Create Markdown content with front matter
                md_content = f"""---
title: "{title}"
date: {date}
author: "{author}"
tags: {tags}
excerpt: "{title}"
---

{content}
"""
                
                # Create filename
                filename = f"{date}-{re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-')}.md"
                md_path = POSTS_DIR / filename
                
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                
                print(f"Created new Markdown file: {md_path}")
                
            except Exception as e:
                print(f"Error creating new Markdown file: {e}")
                sys.exit(1)
        else:
            print("Exiting without editing.")
            sys.exit(0)
    
    # Open the Markdown file for editing
    if open_editor(md_path):
        # After editing, regenerate the HTML
        if regenerate_html(md_path, html_path):
            print("Successfully updated the blog post!")
        else:
            print("Failed to update the blog post.")
    else:
        print("Failed to open editor.")

if __name__ == "__main__":
    main() 