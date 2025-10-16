# shihuaidexianyu.github.io

个人知识库和技术文档站点，使用 [mdBook](https://rust-lang.github.io/mdBook/) 构建。

## 在线访问

📖 访问地址：[https://shihuaidexianyu.github.io](https://shihuaidexianyu.github.io)

## 本地开发

### 前置要求

需要安装 [mdBook](https://rust-lang.github.io/mdBook/):

```bash
# 使用 cargo 安装
cargo install mdbook

# 或者使用包管理器（macOS）
brew install mdbook

# 或者从 GitHub 下载预编译版本
# https://github.com/rust-lang/mdBook/releases
```

### 本地预览

```bash
# 克隆仓库
git clone https://github.com/shihuaidexianyu/shihuaidexianyu.github.io.git
cd shihuaidexianyu.github.io

# 启动本地服务器（支持热重载）
mdbook serve

# 在浏览器中访问 http://localhost:3000
```

### 构建

```bash
# 构建静态文件到 book 目录
mdbook build
```

## 项目结构

```text
.
├── book.toml           # mdBook 配置文件
├── src/                # 源文件目录
│   ├── SUMMARY.md      # 目录结构
│   ├── chapter_1.md    # 内容页面
│   └── ...
├── book/               # 构建输出目录（被 git 忽略）
└── .github/
    └── workflows/
        └── mdbook.yml  # GitHub Actions 自动部署配置
```

## 添加内容

1. 在 `src/` 目录下创建或编辑 Markdown 文件
2. 在 `src/SUMMARY.md` 中添加页面链接
3. 提交并推送到 `main` 分支
4. GitHub Actions 会自动构建并部署到 GitHub Pages

## 部署说明

本项目使用 GitHub Actions 自动部署：

- 推送到 `main` 分支时自动触发构建
- 构建成功后自动部署到 GitHub Pages
- 需要在仓库设置中启用 GitHub Pages（Source: GitHub Actions）

### 启用 GitHub Pages

1. 进入仓库设置：`Settings` → `Pages`
2. 在 `Build and deployment` 部分
3. `Source` 选择：**GitHub Actions**
4. 保存后，推送代码即可自动部署

## 技术栈

- **mdBook**: Rust 实现的静态站点生成器
- **GitHub Actions**: 自动化构建和部署
- **GitHub Pages**: 静态网站托管

## 许可

本项目内容采用 [MIT License](LICENSE) 许可。
