# myweb（Hugo + PaperMod）

这是 yan 的个人博客站点，使用 Hugo 静态站点生成器与 PaperMod 主题。

🌐 **网站地址**：https://luoziyan100.github.io/myweb/

## 快速开始

- 主题子模块（首次克隆后）：
  ```bash
  git submodule update --init --recursive
  ```
- 本地预览：
  ```bash
  hugo server -D
  # 浏览器访问 http://localhost:1313
  ```

## 写作约定

- 文章存放：`content/posts/<年份>/<月份(中文)>/YYYY-MM-DD-标题.md`
- Front matter 示例：
  ```yaml
  ---
  title: "文章标题"
  date: 2025-09-01T10:00:00+08:00
  author: "yan"
  tags: ["AI", "实践"]
  image: "/images/image-1.png"  # 存在于 static/images/
  excerpt: "文章简介..."
  ---
  ```
- 图片放置：`static/images/`，文内引用以 `/images/xxx` 开头。

## 部署

通过 GitHub Actions 自动部署到 GitHub Pages。
- 将内容提交到 `main` 分支：
  ```bash
  git add . && git commit -m "post: 新文章" && git push
  ```
- GitHub Actions 会自动构建并发布，无需手动操作。

> 💡 **自动化流程**：推送到 `main` 分支后，CI 会使用 Hugo 0.149.0 构建静态文件并部署到 GitHub Pages。

## 目录说明
- `content/`：文章与页面
- `static/`：静态资源（图片、图标等）
- `themes/PaperMod`：主题子模块
- `hugo.toml`：站点配置

## 常见问题
- 未来日期文章默认可见（`buildFuture=true`）；如不需要可在 `hugo.toml` 关闭。
- 如果 `hugo server` 报主题缺失，执行子模块初始化命令。
