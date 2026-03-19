# 🤖 Agent Team 可视化管理面板

## ✅ 部署完成！

**访问地址**: http://localhost:5000

---

## 📋 功能特性

### 1. Dashboard 首页
- 📊 实时统计（Agent 数、Skills 数、任务数）
- 👥 Agent 团队列表
- 📦 已安装 Skills 列表
- 📋 最近任务
- 📝 系统日志

### 2. Agent 管理
- 查看 Agent 配置
- 管理 Agent 状态
- 分配任务角色

### 3. 任务管理
- 创建新任务
- 分配给多个 Agent
- 跟踪任务进度
- 查看任务结果

### 4. 配置管理
- Codex API 配置
- 团队配置
- 系统设置

---

## 🏗️ 项目结构

```
agent-team/
├── team_config.json          # 团队配置
└── dashboard/
    ├── app.py                # Flask 主应用
    ├── requirements.txt      # Python 依赖
    ├── templates/
    │   ├── index.html        # 首页
    │   ├── dashboard.html    # Dashboard
    │   ├── agents.html       # Agent 管理
    │   ├── tasks.html        # 任务管理
    │   └── settings.html     # 配置管理
    └── static/
        ├── css/
        │   └── style.css     # 样式文件
        └── js/
            └── main.js       # 前端 JavaScript
```

---

## 🚀 启动方法

### 方法 1: 直接启动（已启动）

```bash
cd /home/jerry/.openclaw/workspace/agent-team/dashboard
python3 app.py
```

### 方法 2: 后台启动

```bash
cd /home/jerry/.openclaw/workspace/agent-team/dashboard
nohup python3 app.py > dashboard.log 2>&1 &
```

### 访问

打开浏览器访问：http://localhost:5000

---

## 📊 API 接口

### 团队相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/team` | GET | 获取团队配置 |

### Skills 相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/skills` | GET | 获取已安装 Skills |

### 任务相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tasks` | GET | 获取任务列表 |
| `/api/tasks` | POST | 创建新任务 |
| `/api/tasks/<id>` | PUT | 更新任务状态 |

### Codex API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/codex` | POST | 调用 Codex API |

### 日志相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/logs` | GET | 获取系统日志 |

---

## 💡 使用示例

### 创建任务

```javascript
// 使用前端 JavaScript
const task = await window.AgentTeam.createTask(
    '代码审查',
    '审查 QQ 转发插件的代码质量',
    ['architect', 'tester']
);
console.log('Task created:', task);
```

### 调用 Codex API

```javascript
// 代码生成
const result = await window.AgentTeam.callCodex(
    '帮我写一个 Python 快速排序函数',
    'gpt-5.3-codex-high'
);
console.log('Codex result:', result);
```

### 更新 Agent 状态

```javascript
// 设置 Agent 为活跃状态
await window.AgentTeam.updateAgentStatus(
    'architect',
    'active',
    '开始代码审查'
);
```

---

## 🎨 界面预览

### Dashboard
- 6 个统计卡片（Agent 数、Skills 数、任务数等）
- Agent 团队列表
- Skills 列表
- 最近任务表格
- 系统日志

### 响应式设计
- 支持桌面端和移动端
- 自适应布局
- 现代化 UI 设计

---

## 🔧 配置说明

### team_config.json

```json
{
  "team_name": "Codex Development Team",
  "version": "1.0.0",
  "agents": [
    {
      "id": "architect",
      "name": "系统架构师",
      "role": "system_architect",
      "model": "gpt-5.3-codex-high"
    },
    {
      "id": "developer",
      "name": "高级开发工程师",
      "role": "senior_developer",
      "model": "gpt-5.3-codex"
    }
  ]
}
```

### Codex API 配置

在 `app.py` 中修改：

```python
CODEX_CONFIG = {
    'api_url': 'https://api.1ip.icu/v1',
    'api_key': 'sk-NUNjhC98UGDC2aVdZIbPVwp9EbGfBFh79fdz0cQJRhRzdfKj',
    'default_model': 'gpt-5.3-codex-high'
}
```

---

## 📝 开发日志

### v1.0.0 (2026-03-19)

**功能**:
- ✅ Dashboard 首页
- ✅ Agent 管理
- ✅ 任务管理
- ✅ Codex API 集成
- ✅ 系统日志
- ✅ 响应式设计

**技术栈**:
- Flask 2.3+
- HTML5/CSS3
- JavaScript (ES6+)
- aiohttp (异步 HTTP)

---

## 🐛 已知问题

暂无

---

## 📞 反馈与支持

- **GitHub**: https://github.com/jry21223/langbot-forward-plugin
- **作者**: Jerry
- **License**: MIT

---

**部署时间**: 2026-03-19 19:50  
**版本**: 1.0.0  
**状态**: ✅ 运行中  
**访问地址**: http://localhost:5000
