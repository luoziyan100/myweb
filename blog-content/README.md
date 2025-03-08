# 博客内容管理系统

这个文件夹结构用于管理您的博客内容，支持使用Markdown格式编写博客文章。

## 文件夹结构

- **posts/**: 存放所有已完成的Markdown博客文章。
- **drafts/**: 存放尚未完成的博客草稿。
- **images/**: 存放博客文章中使用的所有图片和媒体文件。
- **published/**: 存放已发布的HTML版本文章（可选）。

## Markdown博客文章格式

每个博客文章应该是一个独立的`.md`文件，建议使用以下命名格式：

```
YYYY-MM-DD-article-title.md
```

例如：`2025-03-08-transformer-optimization.md`

## 文章前置信息

每篇Markdown文章的开头应包含如下前置信息（YAML格式）：

```markdown
---
title: "文章标题"
date: YYYY-MM-DD
author: "yan"
tags: ["标签1", "标签2", "标签3"]
image: "../images/featured-image.jpg"
excerpt: "文章摘要，简短描述文章内容。"
---

正文内容从这里开始...
```

## 图片引用

在Markdown中，您可以通过以下方式引用图片：

```markdown
![图片描述](../images/image-name.jpg)
```

## 发布工作流程

1. 在`drafts/`文件夹中创建新的Markdown文件，编写草稿。
2. 完成编辑后，将文件移动到`posts/`文件夹。
3. 使用Markdown转HTML工具（如提供的`md-to-html.py`脚本）将文章转换为HTML格式。
4. 将生成的HTML文件保存在`published/`文件夹中。
5. 将HTML内容复制到网站根目录，使用适当的文件名（如`blog-post6.html`）。
6. 更新`blog.html`页面，添加新博客文章的链接和摘要。

## 编辑已发布的文章

如果您需要修改已发布的文章，可以使用`edit-post.py`脚本：

1. 运行命令：`python blog-content/edit-post.py 要编辑的HTML文件路径`
   ```
   # 例如：
   python blog-content/edit-post.py blog-post1.html
   ```

2. 脚本会自动找到对应的Markdown源文件并在您的默认编辑器中打开它。
3. 编辑完成后，保存并关闭编辑器。
4. 按下回车键，脚本会自动重新生成HTML并更新网站。

这个流程可以确保您的Markdown源文件和发布的HTML文件保持同步，同时保留所有样式和格式。

## 样式注意事项

本网站使用深色主题，因此所有博客文章也应保持一致的样式。`md-to-html.py`脚本已配置为：

1. 确保生成的HTML文件使用与网站匹配的深色背景（#121224）。
2. 文本使用浅色（rgba(255, 255, 255, 0.9)）以保证在深色背景上易于阅读。
3. 自动处理数学公式，将其转换为格式良好的HTML。
4. 保持导航链接和路径的正确性。

如果您手动编辑HTML，请确保保持这些样式设置，以维持网站的一致性和可读性。

## Markdown转HTML工具推荐

- **推荐首选**: 使用项目中提供的`md-to-html.py`脚本，它已针对本网站的样式进行了优化：
  ```
  python blog-content/md-to-html.py blog-content/posts/您的文章.md
  ```

- [Pandoc](https://pandoc.org/): 强大的文档转换工具（需手动调整样式）
- [Markdown-it](https://github.com/markdown-it/markdown-it): JavaScript的Markdown解析器
- [Visual Studio Code](https://code.visualstudio.com/): 使用Markdown预览和导出插件

## 使用示例

1. 创建新的博客文章：`blog-content/drafts/2025-03-08-new-blog-post.md`
2. 添加图片到：`blog-content/images/featured-image.jpg`
3. 在文章中引用图片：`![特色图片](../images/featured-image.jpg)`
4. 完成编辑后，将文件移动到：`blog-content/posts/2025-03-08-new-blog-post.md`
5. 转换为HTML格式，保存至：`blog-content/published/2025-03-08-new-blog-post.html` 