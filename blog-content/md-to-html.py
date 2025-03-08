"""
Markdown to HTML converter for blog posts
使用方法: python md-to-html.py <markdown_file> [output_html_file]
"""

import sys
import os
import re
import markdown2
import yaml

def extract_front_matter(content):
    """Extract YAML front matter from markdown content"""
    front_matter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    match = front_matter_pattern.match(content)
    
    if match:
        front_matter_yaml = match.group(1)
        content_without_front_matter = content[match.end():]
        try:
            front_matter = yaml.safe_load(front_matter_yaml)
            return front_matter, content_without_front_matter
        except yaml.YAMLError as e:
            print(f"Error parsing YAML front matter: {e}")
            return {}, content
    
    return {}, content

def format_date(date_str):
    """Format date string to Chinese format (YYYY年MM月DD日)"""
    if not date_str:
        return ""
    try:
        date_parts = str(date_str).split('-')
        if len(date_parts) == 3:
            year, month, day = date_parts
            return f"{year}年{month}月{day}日"
        return date_str
    except Exception as e:
        print(f"Error formatting date: {e}")
        return date_str

def convert_markdown_to_html(markdown_file, output_html=None):
    """Convert markdown file to HTML"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract front matter and markdown content
    front_matter, markdown_content = extract_front_matter(content)
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=['fenced-code-blocks', 'code-friendly', 'tables', 'header-ids', 'toc']
    )
    
    # Transform math code blocks
    html_content = transform_math_code_blocks(html_content)
    
    # Get title, date and tags from front matter
    title = front_matter.get('title', 'Blog Post')
    date_str = front_matter.get('date', '')
    formatted_date = format_date(date_str)
    tags = front_matter.get('tags', [])
    author = front_matter.get('author', 'yan')
    
    # Create tags HTML
    tags_html = ""
    for tag in tags:
        tags_html += f'<span class="blog-post-tag">{tag}</span> '
    
    # Read the base of the markdown file (without extension) for the output filename
    if output_html is None:
        base_name = os.path.splitext(os.path.basename(markdown_file))[0]
        output_dir = os.path.join(os.path.dirname(os.path.dirname(markdown_file)), "published")
        os.makedirs(output_dir, exist_ok=True)
        output_html = os.path.join(output_dir, f"{base_name}.html")
    
    # Create HTML template
    html_template = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AIyan</title>
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* 博客文章页面特有样式 */
        body {{
            background-color: #121224;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-header {{
            background: linear-gradient(135deg, #0c1445 0%, #1e2c91 100%);
            padding: 100px 0 60px;
            color: #fff;
        }}
        
        .blog-post-header-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .blog-post-title {{
            font-size: 2.5rem;
            margin-bottom: 20px;
        }}
        
        .blog-post-meta {{
            display: flex;
            align-items: center;
            gap: 20px;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 30px;
        }}
        
        .blog-post-meta span {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .blog-post-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 20px;
            line-height: 1.8;
            background-color: #121224;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-content p {{
            margin-bottom: 1.5rem;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-content h1, .blog-post-content h2 {{
            margin: 2.5rem 0 1rem;
            font-size: 1.8rem;
            color: #fff;
        }}
        
        .blog-post-content h3 {{
            margin: 2rem 0 1rem;
            font-size: 1.4rem;
            color: #fff;
        }}
        
        .blog-post-content ul, .blog-post-content ol {{
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-content li {{
            margin-bottom: 0.5rem;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-content pre {{
            background: rgba(30, 30, 50, 0.7);
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-content code {{
            background: rgba(30, 30, 50, 0.7);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-content pre code {{
            padding: 0;
            background: transparent;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .blog-post-tags {{
            margin-top: 3rem;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .blog-post-tag {{
            background: rgba(76, 169, 255, 0.2);
            color: #4ca9ff;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .formula {{
            background: rgba(50, 50, 70, 0.7);
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            overflow-x: auto;
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        /* MathJax Styling */
        .MathJax {{
            color: rgba(255, 255, 255, 0.9) !important;
        }}
        
        .mjx-chtml {{
            background: transparent !important;
        }}
    </style>
    <script type="text/javascript" id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    <script>
    window.MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
            processEscapes: true,
            processEnvironments: true
        }},
        options: {{
            ignoreHtmlClass: 'tex2jax_ignore',
            processHtmlClass: 'tex2jax_process'
        }}
    }};
    </script>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">
                <a href="index.html">AI<span>yan</span></a>
            </div>
            <div class="menu-btn">
                <div class="menu-btn__burger"></div>
            </div>
            <ul class="nav-links">
                <li><a href="index.html">首页</a></li>
                <li><a href="blog.html" class="active">博客</a></li>
                <li><a href="github.html">GitHub</a></li>
                <li><a href="xiaohongshu.html">小红书</a></li>
                <li><a href="https://sspai.com/u/deeplearning" target="_blank">少数派</a></li>
            </ul>
        </div>
    </nav>

    <!-- 博客文章头部 -->
    <header class="blog-post-header">
        <div class="blog-post-header-content">
            <h1 class="blog-post-title">{title}</h1>
            <div class="blog-post-meta">
                <span><i class="far fa-calendar-alt"></i> {formatted_date}</span>
                <span><i class="far fa-user"></i> {author}</span>
            </div>
        </div>
    </header>

    <!-- 博客文章内容 -->
    <article class="blog-post-content">
        {html_content}
        
        <div class="blog-post-tags">
            {tags_html}
        </div>
    </article>

    <!-- 页脚 -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="copyright">
                    <p>&copy; 2025 AI训练师. 保留所有权利。</p>
                </div>
                <div class="contact-info">
                    <p>邮箱: 1017075076@qq.com</p>
                </div>
                <div class="social-links">
                    <a href="https://github.com/luoziyan100" target="_blank" aria-label="GitHub 资料"><i class="fab fa-github"></i></a>
                    <a href="https://www.xiaohongshu.com/user/profile/66ab7e91000000001d0221ce" target="_blank" aria-label="小红书资料"><i class="fas fa-book-open"></i></a>
                    <a href="https://sspai.com/u/deeplearning" target="_blank" aria-label="少数派资料"><i class="fas fa-pen-nib"></i></a>
                </div>
            </div>
            <div class="back-to-top">
                <a href="#" id="back-to-top-btn" aria-label="回到顶部"><i class="fas fa-arrow-up"></i></a>
            </div>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
    """
    
    # Write HTML to output file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Markdown converted to HTML and saved to {output_html}")
    
    return output_html

def transform_math_code_blocks(html_content):
    """Transform code blocks that look like math formulas into MathJax compatible divs"""
    # Pattern for finding code blocks
    code_pattern = re.compile(r'<pre><code>(.*?)</code></pre>', re.DOTALL)
    
    def is_math_formula(code):
        # Heuristic to identify math formulas - contains math symbols like ^, _, sqrt, or equations
        math_indicators = ['^', '_', '/', r'\sqrt', r'\frac', '×', '÷', '=', 'sum', 'prod', 'lim', 'int', 'alpha', 'beta', 'gamma', 'sigma', '\\begin{align}', '\\end{align}']
        return any(indicator in code for indicator in math_indicators)
    
    def replace_code_with_formula(match):
        code = match.group(1)
        if is_math_formula(code):
            # Check if contains LaTeX environments that should be kept intact
            if '\\begin{' in code or '\\end{' in code or '&=' in code or '\\\\' in code:
                # Keep the entire block as one formula
                code = code.strip()
                return f'<div class="formula">$${code}$$</div>'
            
            # Split multi-line formulas that are NOT part of an environment
            elif '\n' in code.strip():
                lines = [line.strip() for line in code.strip().split('\n') if line.strip()]
                # Check if any line is a continuation of previous line (ends with \\)
                if any('\\\\' in line for line in lines):
                    # This appears to be a multi-line equation that should stay together
                    code = code.strip()
                    return f'<div class="formula">$${code}$$</div>'
                else:
                    # Separate formulas
                    result = ""
                    for line in lines:
                        result += f'<div class="formula">$${line}$$</div>\n'
                    return result
            else:
                # Inline mode for single line equations
                code = code.strip()
                return f'<div class="formula">$${code}$$</div>'
        return match.group(0)  # Return the original if not a formula
    
    # Replace code blocks that look like formulas
    html_content = code_pattern.sub(replace_code_with_formula, html_content)
    
    return html_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python md-to-html.py <markdown_file> [output_html_file]")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_markdown_to_html(markdown_file, output_html) 