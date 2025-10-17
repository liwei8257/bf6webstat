# 🎮 BF6 玩家数据统计系统

一个基于 Flask 的 Web 应用，用于查询和展示多个 Battlefield 6 玩家的统计数据，支持实时刷新和多维度数据排序。

## ✨ 功能特性

- ✅ **多玩家查询**：同时查询多个玩家的战绩数据
- ✅ **实时数据**：从 tracker.gg 获取最新玩家统计
- ✅ **智能排序**：支持按任意数据维度升序/降序排序
- ✅ **数据缓存**：30秒内存缓存，减少API调用
- ✅ **现代界面**：美观的响应式Web界面
- ✅ **Cloudflare绕过**：自动处理Cloudflare防护

## 📊 数据指标

系统展示以下关键统计数据：

- 击杀/死亡数 & K/D比率
- 胜场/败场 & 胜率
- 分钟得分 & 分钟击杀
- 准确率 & 爆头率
- 游戏时长 & 比赛场数
- 伤害、复活等其他数据

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Windows/Linux/MacOS

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置玩家列表

编辑 `players.json` 文件。**推荐使用简化配置**：

#### 方式1：简化配置（推荐） ⭐

只需填写Steam用户名，程序会自动搜索：

```json
{
  "steam_usernames": [
    "石景山AT人",
    "Longbowchen",
    "Ammo117"
  ]
}
```

#### 方式2：完整配置（高级用户）

手动指定平台和ID：

```json
{
  "players": [
    {
      "name": "玩家1",
      "platform": "origin",
      "user_id": "OriginUsername"
    },
    {
      "name": "玩家2",
      "platform": "steam",
      "user_id": "3116588130"
    }
  ]
}
```

**支持的平台：**
- `origin` - Origin (EA)
- `steam` - Steam
- `psn` - PlayStation Network
- `xbl` - Xbox Live

### 4. 配置API密钥（可选）

如果你有 tracker.gg 的 API Key，可以设置环境变量：

**Windows PowerShell:**
```powershell
$env:TRN_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export TRN_API_KEY="your_api_key_here"
```

### 5. 运行应用

```bash
python app.py
```

### 6. 访问界面

打开浏览器访问：`http://localhost:5000`

## 📁 项目结构

```
bf6stat/
├── api_handler.py      # API请求处理（Cloudflare绕过 + 缓存）
├── data_processor.py   # 数据获取和处理逻辑
├── app.py             # Flask Web应用主程序
├── players.json       # 玩家配置文件
├── requirements.txt   # Python依赖
├── templates/
│   └── index.html    # 前端HTML页面
└── static/
    └── style.css     # CSS样式文件
```

## 🎯 使用说明

### 添加/修改玩家

**超简单模式（推荐）：**
1. 编辑 `players.json` 文件
2. 在 `steam_usernames` 数组中添加Steam用户名
3. 刷新网页并点击"刷新数据"
4. 程序会自动搜索并获取数据

**完整配置模式：**
1. 编辑 `players.json` 中的 `players` 数组
2. 手动填写 name, platform, user_id
3. 刷新网页

### ✨ 新特性：自动搜索

现在你**不需要手动查找玩家ID**了！

只需要在 `players.json` 中填写：
```json
{
  "steam_usernames": ["石景山AT人", "Longbowchen", "Ammo117"]
}
```

程序会自动：
1. 🔍 在tracker.gg搜索玩家
2. 📍 获取正确的玩家ID（如 `3116588130`）
3. 📊 拉取完整数据展示

### 数据排序

- 点击任意表头即可按该列排序
- 再次点击切换升序/降序
- 箭头指示当前排序方向（▼降序 ▲升序）

## ⚠️ 常见问题

### 遇到 403 错误

如果遇到 Cloudflare 403 错误：

1. 手动访问 tracker.gg 并完成人机验证
2. 使用浏览器开发者工具获取 Cookie
3. 设置环境变量：
   ```bash
   $env:CF_CLEARANCE="your_cookie_value"
   $env:CF_BM="your_cookie_value"
   ```

### 数据不准确或缺失

- 确保玩家ID正确
- 检查平台选择是否正确
- 某些新玩家可能数据未同步到tracker.gg

### 加载缓慢

- 首次加载会同时请求所有玩家数据
- 玩家数量越多，加载时间越长
- 30秒内再次刷新会使用缓存数据

## 🌐 服务器部署

本项目支持部署到服务器供外网访问！

### 快速部署选项

| 方案 | 难度 | 适用场景 |
|------|------|----------|
| **Docker** | ⭐ 简单 | 任何支持Docker的服务器 |
| **云平台PaaS** | ⭐ 最简单 | Railway/Render免费部署 |
| **Linux服务器** | ⭐⭐ 中等 | VPS/云服务器（最灵活）|
| **Windows服务器** | ⭐⭐ 中等 | Windows Server |

### Docker部署（推荐）

```bash
# 1. 构建并启动
docker-compose up -d

# 2. 访问
http://你的服务器IP:8000
```

### Linux生产环境

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 使用Gunicorn启动
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app

# 3. 配置Nginx反向代理（可选）
```

### Windows生产环境

```bash
# 1. 安装依赖
pip install waitress

# 2. 运行生产服务器
python run_production.py
```

📖 **详细部署指南**: 查看 `部署指南.md` 文件

## 🔧 高级配置

### 修改缓存时间

编辑 `api_handler.py` 第22行：

```python
_TTL = 30  # 秒数，可改为60、120等
```

### 修改并发数量

编辑 `api_handler.py` 第21行：

```python
_CONCURRENCY = asyncio.Semaphore(4)  # 改为更大或更小的数值
```

### 修改端口

编辑 `app.py` 最后一行：

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 修改port值
```

## 📝 开发说明

### 技术栈

- **后端**: Flask + asyncio
- **前端**: 原生HTML/CSS/JavaScript
- **API**: tracker.gg BF6 API
- **反爬虫**: cloudscraper

### 扩展功能建议

- [ ] 自动定时刷新
- [ ] 数据图表可视化
- [ ] 历史数据记录
- [ ] 玩家对比功能
- [ ] 导出Excel/CSV
- [ ] 武器统计详情

## 📄 许可证

MIT License

## 🙏 致谢

- 数据来源: [tracker.gg](https://tracker.gg)
- Cloudflare绕过: [cloudscraper](https://github.com/VeNoMouS/cloudscraper)

---

**注意**: 请遵守 tracker.gg 的服务条款，不要过度频繁请求API。

