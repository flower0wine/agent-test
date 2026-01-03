# Simple API Service

一个使用uv作为包管理器的简单Python API服务，基于FastAPI框架。

## 快速开始

### 1. 安装依赖
```bash
uv pip install -r requirements.txt
```

### 2. 运行服务
```bash
python main.py
```

服务将在 http://localhost:8000 启动。

## API文档

服务启动后，访问以下地址：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## API端点

### 项目管理
- `GET /items` - 获取所有项目
- `GET /items/{id}` - 根据ID获取项目
- `POST /items` - 创建新项目
- `PUT /items/{id}` - 更新项目
- `DELETE /items/{id}` - 删除项目
- `GET /items/search/` - 搜索项目（支持按名称和最低价格筛选）

### 示例请求

创建项目：
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Item", "price": 29.99}'
```

获取所有项目：
```bash
curl "http://localhost:8000/items"
```

搜索项目：
```bash
curl "http://localhost:8000/items/search/?name=item&min_price=15.0"
```

## 项目结构

```
simple-api-service/
├── main.py              # 主应用文件
├── requirements.txt     # 依赖文件
├── README.md           # 说明文档
├── run.bat             # Windows启动脚本
├── Dockerfile          # Docker容器配置
├── docker-compose.yml  # Docker Compose配置
└── Makefile            # 常用命令集合
```

## 使用uv的优势

1. **快速安装** - uv比传统pip快很多
2. **确定性构建** - 确保依赖版本一致性
3. **跨平台** - 支持Windows、macOS和Linux
4. **现代工具** - 集成了包管理、虚拟环境管理等功能

## 开发说明

### 使用虚拟环境
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Unix/macOS:
source .venv/bin/activate

# 安装依赖
uv pip install -r requirements.txt
```

### 使用Docker
```bash
# 构建镜像
docker build -t simple-api-service .

# 运行容器
docker run -p 8000:8000 simple-api-service

# 使用Docker Compose
docker-compose up -d
```

## 许可证

MIT