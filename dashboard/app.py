"""
Agent Team 可视化管理面板
Flask Web Application

版本：1.0.0
作者：Jerry (Codex AI Team)
"""

import os
import json
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
import aiohttp

app = Flask(__name__)

# 配置
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'team_config.json')
SKILLS_FILE = os.path.expanduser('~/.openclaw/workspace/skills/list.json')
CODEX_CONFIG = {
    'api_url': 'https://api.1ip.icu/v1',
    'api_key': 'sk-NUNjhC98UGDC2aVdZIbPVwp9EbGfBFh79fdz0cQJRhRzdfKj',
    'default_model': 'gpt-5.3-codex-high'
}

# 内存存储（生产环境应使用数据库）
tasks = []
logs = []
agent_status = {
    'architect': {'status': 'active', 'message': 'Ready', 'updated_at': datetime.now().isoformat()},
    'developer': {'status': 'active', 'message': 'Ready', 'updated_at': datetime.now().isoformat()},
    'tester': {'status': 'active', 'message': 'Ready', 'updated_at': datetime.now().isoformat()},
    'devops': {'status': 'active', 'message': 'Ready', 'updated_at': datetime.now().isoformat()}
}

def load_team_config():
    """加载团队配置"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {'error': str(e)}

def load_skills():
    """加载已安装的 Skills"""
    skills_dir = os.path.expanduser('~/.openclaw/workspace/skills')
    skills = []
    if os.path.exists(skills_dir):
        for item in os.listdir(skills_dir):
            item_path = os.path.join(skills_dir, item)
            if os.path.isdir(item_path):
                skills.append({
                    'name': item,
                    'path': item_path,
                    'installed_at': datetime.fromtimestamp(os.path.getctime(item_path)).strftime('%Y-%m-%d %H:%M:%S')
                })
    return skills

async def call_codex_api(prompt, model='gpt-5.3-codex-high'):
    """调用 Codex API"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{CODEX_CONFIG['api_url']}/chat/completions",
            headers={
                'Authorization': f"Bearer {CODEX_CONFIG['api_key']}",
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': [
                    {'role': 'system', 'content': '你是一位专业的 AI 助手'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 4000,
                'temperature': 0.3
            }
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error: {response.status}"

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard 页面"""
    team_config = load_team_config()
    skills = load_skills()
    
    stats = {
        'total_agents': len(team_config.get('agents', [])),
        'total_skills': len(skills),
        'total_tasks': len(tasks),
        'completed_tasks': len([t for t in tasks if t.get('status') == 'completed']),
        'active_agents': len([a for a in agent_status.values() if a.get('status') == 'active']),
        'api_calls_today': len([l for l in logs if l.get('type') == 'api_call' and l.get('timestamp', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    }
    
    return render_template('dashboard.html', team=team_config, skills=skills, stats=stats)

@app.route('/agents')
def agents():
    """Agent 管理页面"""
    team_config = load_team_config()
    return render_template('agents.html', team=team_config, agent_status=agent_status)

@app.route('/tasks')
def tasks_page():
    """任务管理页面"""
    return render_template('tasks.html', tasks=tasks)

@app.route('/settings')
def settings():
    """配置页面"""
    return render_template('settings.html', codex_config=CODEX_CONFIG)

@app.route('/api/team')
def api_team():
    """获取团队信息 API"""
    return jsonify(load_team_config())

@app.route('/api/skills')
def api_skills():
    """获取 Skills 列表 API"""
    return jsonify(load_skills())

@app.route('/api/tasks', methods=['GET'])
def api_tasks():
    """获取任务列表 API"""
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """创建新任务 API"""
    data = request.json
    task = {
        'id': len(tasks) + 1,
        'title': data.get('title', 'Untitled Task'),
        'description': data.get('description', ''),
        'assigned_to': data.get('assigned_to', []),
        'status': 'pending',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'result': None
    }
    tasks.append(task)
    logs.append({
        'type': 'task_created',
        'message': f"Task created: {task['title']}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """更新任务 API"""
    data = request.json
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)
            task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logs.append({
                'type': 'task_updated',
                'message': f"Task updated: {task['title']}",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/codex', methods=['POST'])
async def api_codex():
    """调用 Codex API"""
    data = request.json
    prompt = data.get('prompt', '')
    model = data.get('model', CODEX_CONFIG['default_model'])
    
    logs.append({
        'type': 'api_call',
        'message': f"Codex API call: {model}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    result = await call_codex_api(prompt, model)
    return jsonify({'result': result})

@app.route('/api/logs')
def api_logs():
    """获取日志 API"""
    return jsonify(logs[-100:])  # 返回最近 100 条日志

@app.route('/api/agents/<agent_id>/status', methods=['PUT'])
def api_update_agent_status(agent_id):
    """更新 Agent 状态 API"""
    data = request.json
    agent_status[agent_id] = data
    logs.append({
        'type': 'agent_status',
        'message': f"Agent {agent_id} status updated: {data.get('status')}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    return jsonify(agent_status[agent_id])

@app.route('/api/orchestrate', methods=['POST'])
async def api_orchestrate():
    """使用 agent-team-orchestration 技能编排任务"""
    data = request.json
    task_description = data.get('task', '')
    team_config = data.get('team', ['architect', 'developer', 'tester'])
    
    logs.append({
        'type': 'orchestration',
        'message': f"Starting multi-agent task: {task_description[:50]}...",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # 模拟多 Agent 协作流程
    workflow_steps = []
    
    # 步骤 1: Architect 设计
    workflow_steps.append({
        'step': 1,
        'agent': 'architect',
        'action': 'design',
        'status': 'pending'
    })
    
    # 步骤 2: Developer 实现
    workflow_steps.append({
        'step': 2,
        'agent': 'developer',
        'action': 'implement',
        'status': 'pending'
    })
    
    # 步骤 3: Tester 测试
    workflow_steps.append({
        'step': 3,
        'agent': 'tester',
        'action': 'test',
        'status': 'pending'
    })
    
    return jsonify({
        'task_id': len(tasks) + 1,
        'description': task_description,
        'workflow': workflow_steps,
        'status': 'orchestrating'
    })

if __name__ == '__main__':
    print("🚀 Agent Team Dashboard Starting...")
    print(f"📊 Dashboard URL: http://localhost:5000")
    print(f"📁 Config File: {CONFIG_FILE}")
    app.run(host='0.0.0.0', port=5000, debug=True)
