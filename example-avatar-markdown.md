# 在Markdown中使用GitHub头像URL

## 方法1：标准Markdown图片语法

![GitHub头像](https://avatars.githubusercontent.com/u/199953103?s=96&v=4)

## 方法2：使用HTML标签控制尺寸

小尺寸：
<img src="https://avatars.githubusercontent.com/u/199953103?s=96&v=4" alt="GitHub头像" width="50">

中等尺寸：
<img src="https://avatars.githubusercontent.com/u/199953103?s=96&v=4" alt="GitHub头像" width="100">

大尺寸：
<img src="https://avatars.githubusercontent.com/u/199953103?s=96&v=4" alt="GitHub头像" width="200">

## 方法3：在博客文章YAML中使用

在Markdown博客文章的YAML前置信息中，您可以这样设置头图：

```yaml
---
title: "我的博客文章"
date: 2025-03-10
author: "yan"
tags: ["GitHub", "个人介绍"]
image: "https://avatars.githubusercontent.com/u/199953103?s=96&v=4"
excerpt: "这是一篇使用GitHub头像作为头图的博客文章"
---
```

**注意**：在正式博客中使用此方法时，请确保您的模板支持直接使用URL作为图片路径。 