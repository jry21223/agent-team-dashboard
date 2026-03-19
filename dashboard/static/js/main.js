// Agent Team Dashboard JavaScript

console.log('🤖 Agent Team Dashboard Loaded');

// 自动刷新 Dashboard 数据
function refreshDashboard() {
    fetch('/api/team')
        .then(r => r.json())
        .then(team => {
            console.log('Team config loaded:', team);
        });

    fetch('/api/skills')
        .then(r => r.json())
        .then(skills => {
            console.log('Skills loaded:', skills.length);
        });
}

// 创建新任务
async function createTask(title, description, assignedTo = []) {
    const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title,
            description,
            assigned_to: assignedTo
        })
    });
    return await response.json();
}

// 更新任务状态
async function updateTaskStatus(taskId, status, result = null) {
    const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            status,
            result
        })
    });
    return await response.json();
}

// 调用 Codex API
async function callCodex(prompt, model = 'gpt-5.3-codex-high') {
    const response = await fetch('/api/codex', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt,
            model
        })
    });
    return await response.json();
}

// 更新 Agent 状态
async function updateAgentStatus(agentId, status, message = '') {
    const response = await fetch(`/api/agents/${agentId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            status,
            message,
            updated_at: new Date().toISOString()
        })
    });
    return await response.json();
}

// 实时日志更新
function setupLogPolling() {
    setInterval(async () => {
        const response = await fetch('/api/logs');
        const logs = await response.json();
        // 更新日志显示
        console.log('Latest logs:', logs.slice(-5));
    }, 5000); // 每 5 秒刷新一次
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard initialized');
    refreshDashboard();
    setupLogPolling();
});

// 导出函数供其他模块使用
window.AgentTeam = {
    createTask,
    updateTaskStatus,
    callCodex,
    updateAgentStatus,
    refreshDashboard
};
