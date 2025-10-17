# 🛡️ Cloudflare 403 错误修复指南

## 问题原因

Tracker.gg 使用了 Cloudflare 防护，从服务器直接访问API可能会被拦截。

## 🔧 解决方案（按推荐顺序）

### 方案1：更新代码（已完成）✅

我已经修改了代码：
- 移除了不存在的 `solve_cloudflare` 方法
- 增加了重试次数（3次）
- 添加了更完整的浏览器请求头
- 增加了延迟重试机制

**现在需要推送更新：**

```bash
# 方法A：使用Git命令
cd D:\bf6stat
git add api_handler.py config.py
git commit -m "Fix: 修复Cloudflare 403错误"
git push

# 方法B：使用GitHub Desktop
# 1. 打开GitHub Desktop
# 2. 看到修改的文件
# 3. 输入提交信息
# 4. Commit → Push
```

推送后，Render会**自动重新部署**！

---

### 方案2：获取Cloudflare Cookies（备用方案）

如果方案1还是遇到403错误，需要手动获取cookies：

#### 步骤：

1. **打开浏览器**，访问 https://tracker.gg/battlefield-6

2. **打开开发者工具**
   - Chrome: 按 `F12` 或 `Ctrl+Shift+I`
   - Firefox: 按 `F12`

3. **切换到 Network（网络）标签**

4. **刷新页面** (`F5`)

5. **找到 API 请求**
   - 在列表中找到 `api.tracker.gg` 开头的请求
   - 点击它

6. **查看 Cookies**
   - 切换到 "Headers"（标头）标签
   - 找到 "Cookie:" 部分
   - 复制 `cf_clearance` 的值
   - 复制 `__cf_bm` 的值

7. **在Render添加环境变量**
   
   进入你的服务 → Environment → Add Environment Variable:
   
   ```
   Key: CF_CLEARANCE
   Value: 粘贴你复制的cf_clearance值
   
   Key: CF_BM
   Value: 粘贴你复制的cf_bm值
   ```

8. **保存并重启**

**注意**：Cookies会过期，可能需要定期更新（通常几小时到几天）。

---

### 方案3：使用代理服务（高级）

如果上述方案都不行，可以考虑：

1. **使用代理API服务**
   - ScraperAPI
   - Bright Data
   - 这些服务会帮你绕过Cloudflare

2. **修改代码使用代理**

这个方案成本较高，不推荐个人项目使用。

---

## 🎯 推荐操作流程

### 第一步：推送代码更新

```bash
git add .
git commit -m "Fix Cloudflare error"
git push
```

### 第二步：等待Render自动部署

1. 在Render查看 "Logs" 标签
2. 等待部署完成（1-2分钟）

### 第三步：测试

1. 访问你的应用URL
2. 点击"刷新数据"
3. 查看是否成功

### 第四步：如果还是403错误

按照"方案2"获取Cloudflare cookies并添加到环境变量。

---

## 🔍 检查部署日志

在Render的Logs标签中，你应该看到：

**成功的日志：**
```
INFO:data_processor:正在搜索玩家: 石景山AT人 (steam)...
INFO:data_processor:找到玩家: 石景山AT人 (ID: 3116588130)
INFO:data_processor:✓ 成功获取玩家 石景山AT人 的数据
```

**如果还是失败：**
```
WARNING:bf6bot.trn:[TRN] 403 Cloudflare block (attempt 1/3)
WARNING:bf6bot.trn:[TRN] 403 Cloudflare block (attempt 2/3)
WARNING:bf6bot.trn:[TRN] 403 Cloudflare block (attempt 3/3)
ERROR:data_processor:搜索玩家失败
```

如果看到这个，需要使用方案2添加cookies。

---

## 💡 为什么本地可以但服务器不行？

- ✅ **本地**：你的IP看起来像普通用户
- ❌ **服务器**：Render的IP被识别为数据中心IP，容易被拦截

这是正常现象，很多网站都会这样防护。

---

## 🆘 需要帮助？

如果推送代码后还是不行，告诉我：

1. Render Logs中的完整错误信息
2. 是否添加了Cloudflare cookies
3. 我可以帮你进一步调试

---

现在先推送代码更新，看看能否解决！🚀

