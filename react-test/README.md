# React Test Project

这是一个使用 pnpm + Vite + React 创建的测试项目。

## 项目信息

- **包管理器**: pnpm
- **构建工具**: Vite
- **React 版本**: 19.2.3
- **开发服务器**: http://localhost:5173
- **热重载**: 已启用

## 项目结构

```
react-test/
├── public/              # 静态资源
├── src/                 # 源代码
│   ├── assets/          # 图片等资源
│   ├── App.css          # 应用样式
│   ├── App.jsx          # 主应用组件
│   ├── index.css        # 全局样式
│   └── main.jsx         # 应用入口
├── index.html           # HTML模板
├── package.json         # 项目配置
├── vite.config.js       # Vite配置
├── eslint.config.js     # ESLint配置
└── README.md            # 项目说明
```

## 可用命令

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev

# 构建生产版本
pnpm build

# 预览生产版本
pnpm preview

# 代码检查
pnpm lint
```

## 功能特性

1. **计数器应用**: 包含增加、减少、重置功能
2. **响应式设计**: 适配移动端和桌面端
3. **热重载**: 修改代码后自动刷新
4. **现代化工具链**: 使用最新的 React 和构建工具

## 访问应用

开发服务器运行在: http://localhost:5173

## 技术栈

- React 19.2.3
- Vite 7.3.0
- pnpm 10.26.0
- ESLint 9.39.2