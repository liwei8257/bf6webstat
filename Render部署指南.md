# 🎨 Render.com 免费部署指南

## ✨ 为什么选择Render？

- ✅ **完全免费** - 不需要信用卡
- ✅ **750小时/月** - 足够个人使用
- ✅ **自动HTTPS** - 免费SSL证书
- ✅ **从GitHub部署** - 代码更新自动部署
- ✅ **简单易用** - 比Railway更友好

## 📋 前置准备

### 1. 推送代码到GitHub

**方法A：使用GitHub Desktop（最简单）**

1. 下载安装：https://desktop.github.com/
2. 登录GitHub账号
3. File → Add Local Repository → 选择 `D:\bf6stat`
4. 如果提示"不是Git仓库"，点击"Create a repository"
5. 点击 "Publish repository"
   - 名称：`bf6stat`
   - 描述：BF6玩家数据统计系统
   - 取消勾选"Keep this code private"（或保持私有）
6. 完成！

**方法B：使用命令行**

```bash
cd D:\bf6stat

# 初始化Git
git init
git add .
git commit -m "Initial commit: BF6 Stats System"

# 在GitHub网页创建新仓库：https://github.com/new
# 仓库名：bf6stat

# 推送代码（替换你的用户名）
git remote add origin https://github.com/你的用户名/bf6stat.git
git branch -M main
git push -u origin main
```

---

## 🚀 在Render部署

### 步骤1：注册Render账号

1. 访问：https://render.com
2. 点击 "Get Started"
3. 使用GitHub账号登录（推荐）
4. 授权Render访问GitHub

### 步骤2：创建Web Service

1. 登录后，点击 "New +" → "Web Service"

2. **连接GitHub仓库**
   - 如果看不到仓库，点击 "Configure account"
   - 选择"All repositories"或手动选择 `bf6stat`
   - 返回后选择 `bf6stat` 仓库

3. **配置服务**（重要！）

   ```
   Name: bf6stat
   Region: Singapore (或选择离你最近的)
   Branch: main
   
   Runtime: Python 3
   
   Build Command:
   pip install -r requirements.txt
   
   Start Command:
   gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 180 --graceful-timeout 180 wsgi:app
   ```

4. **选择免费计划**
   - Instance Type: **Free**
   - 向下滚动，确认是Free tier

5. **高级设置（可选）**
   - 点击 "Advanced"
   - 添加环境变量：
     ```
     FLASK_ENV=production
     ```

6. **创建服务**
   - 点击 "Create Web Service"
   - 等待构建（大约2-3分钟）

### 步骤3：访问你的应用

部署成功后：
- 你会得到一个URL：`https://bf6stat.onrender.com`
- 点击URL访问你的应用
- 完成！🎉

---

## ⚙️ 配置文件（已准备好）

### 确保这些文件存在：

#### requirements.txt
```
Flask==3.0.0
gunicorn==21.2.0
cloudscraper==1.2.71
requests==2.31.0
python-dotenv==1.0.0
```

#### wsgi.py
```python
from app import app

if __name__ == "__main__":
    app.run()
```

---

## 🔧 常见问题

### 1. 部署失败？

查看Logs标签，常见原因：
- `requirements.txt` 缺失或格式错误
- Start Command 配置错误
- Python版本不兼容

**解决方案**：
```bash
# 重新生成requirements.txt
pip freeze > requirements.txt
git add .
git commit -m "Fix requirements"
git push
```

### 2. 应用无法访问？

Render免费版有限制：
- ⏰ 15分钟无访问会休眠
- 🐌 首次唤醒需要30秒
- 这是正常的！

### 3. 域名太长？

可以绑定自己的域名：
- Settings → Custom Domain
- 添加你的域名
- 配置DNS记录

---

## 📊 监控和日志

### 查看日志
1. 点击你的服务
2. Logs 标签
3. 实时查看运行日志

### 查看部署状态
- Events 标签：查看部署历史
- Metrics 标签：查看流量和性能

---

## 🔄 更新应用

**超简单！** 只需推送到GitHub：

```bash
# 修改代码后
git add .
git commit -m "更新描述"
git push
```

Render会自动检测并重新部署！

---

## 💰 免费额度说明

Render Free Tier包括：
- ✅ 750小时/月运行时间
- ✅ 512MB RAM
- ✅ 自动HTTPS
- ✅ 自动休眠（15分钟不活动）
- ✅ 全球CDN
- ❌ 不支持自定义域名HTTPS（需付费）

对个人项目完全够用！

---

## 🎯 部署检查清单

在点击"Create Web Service"前确认：

- [x] GitHub仓库已推送
- [x] Runtime选择Python 3
- [x] Build Command: `pip install -r requirements.txt`
- [x] Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 wsgi:app`
- [x] Instance Type: Free
- [x] 环境变量FLASK_ENV=production（可选）

---

## 🆘 需要帮助？

- Render文档：https://render.com/docs
- 社区论坛：https://community.render.com
- 支持邮箱：support@render.com

祝部署顺利！🚀

