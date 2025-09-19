#!/bin/bash
echo "提示：已配置 GitHub Actions 自动部署，优先推送 master；本脚本为备选。"
echo "🚀 开始更新博客..."

# 激活虚拟环境
source venv/bin/activate

# 生成静态网站
echo "📝 生成静态网站..."
hugo --minify

# 进入public目录并部署
echo "🌐 部署到GitHub Pages..."
cd public
git add .
git commit -m "博客更新：$(date '+%Y-%m-%d %H:%M')"
git push -f origin master:gh-pages

echo "✅ 博客更新完成！"
echo "🔗 访问：https://luoziyan100.github.io/myweb/"

cd ..
