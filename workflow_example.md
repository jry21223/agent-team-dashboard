# Agent Team 协作流程示例

## 场景：代码审查 + 修复 + 测试

### 团队配置

```json
{
  "orchestrator": {
    "id": "orchestrator",
    "name": "协调员",
    "model": "gpt-5.3-codex-high",
    "role": "Orchestrator"
  },
  "builder": {
    "id": "developer",
    "name": "开发工程师",
    "model": "gpt-5.3-codex",
    "role": "Builder"
  },
  "reviewer": {
    "id": "tester",
    "name": "测试工程师",
    "model": "gpt-5.3-codex-high",
    "role": "Reviewer"
  }
}
```

### 任务流程

```
1. Orchestrator 收到任务："审查并修复 QQ 转发插件"
   ↓
2. 创建任务记录
   - Task ID: #001
   - 描述：审查 QQ 转发插件代码质量
   - 输出路径：/workspace/review-results/
   ↓
3. 分配给 Reviewer 进行审查
   - 输入：插件代码
   - 输出：审查报告
   ↓
4. Reviewer 提交审查报告
   - 发现 10 个问题（3 个严重，4 个中等，3 个轻微）
   - 交接给 Builder 修复
   ↓
5. Builder 修复问题
   - 修复所有严重和中等问题
   - 提交修复后的代码
   - 交接给 Reviewer 验证
   ↓
6. Reviewer 验证修复
   - 确认所有问题已修复
   - 运行测试通过
   ↓
7. Orchestrator 标记任务完成
   - 状态：Done
   - 产出：修复后的代码 + 审查报告 + 测试结果
```

### 交接消息模板

```markdown
## 任务交接

**任务 ID**: #001
**从**: Reviewer
**到**: Builder

### 已完成
- 完成代码审查
- 识别 10 个问题

### 产物位置
- 审查报告：/workspace/review-results/report-001.md
- 问题列表：/workspace/review-results/issues-001.json

### 如何验证
```bash
cd /workspace/langbot-forward-plugin
python3 -m py_compile main.py
```

### 已知问题
- 3 个严重问题需要立即修复
- 4 个中等问题建议修复
- 3 个轻微问题可选修复

### 下一步
1. 修复所有严重问题
2. 修复所有中等问题
3. 运行代码检查
4. 交接回 Reviewer 验证
```

### 状态更新规则

```python
# Orchestrator 更新任务状态
async def update_task_status(task_id, new_status, comment):
    task = get_task(task_id)
    task.status = new_status
    task.comments.append({
        'timestamp': datetime.now(),
        'status': new_status,
        'comment': comment,
        'agent': current_agent_id
    })
    save_task(task)
    
    # 通知相关 Agent
    if new_status == 'Review':
        notify_agent('reviewer', f'Task #{task_id} ready for review')
    elif new_status == 'Done':
        notify_orchestrator(f'Task #{task_id} completed')
```

### 使用 sessions_spawn 实现

```python
# Orchestrator  spawn Reviewer
reviewer_result = await sessions_spawn(
    task='审查 QQ 转发插件代码，生成审查报告',
    agentId='tester',
    attachments=[
        {'name': 'main.py', 'content': plugin_code}
    ],
    mode='session'
)

# 等待 Reviewer 完成
review_report = await reviewer_result

# spawn Builder 修复
builder_result = await sessions_spawn(
    task=f'根据审查报告修复代码：{review_report}',
    agentId='developer',
    mode='session'
)

# 等待 Builder 完成
fixed_code = await builder_result

# 再次 spawn Reviewer 验证
verification = await sessions_spawn(
    task=f'验证修复后的代码：{fixed_code}',
    agentId='tester',
    mode='session'
)
```

---

**创建时间**: 2026-03-19  
**参考**: agent-team-orchestration Skill
