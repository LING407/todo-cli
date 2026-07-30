# 贡献指南

感谢你对 Todo CLI 项目的关注！欢迎提交 Issue 和 Pull Request。

## 开发环境搭建

1. Fork 本仓库
2. 克隆到本地：

   ```bash
   git clone https://github.com/yourusername/todo-cli.git
   cd todo-cli
   ```

3. 创建虚拟环境并安装依赖：

   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

## 开发流程

1. 从 `main` 分支创建新分支：

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 编写代码并添加相应的单元测试
3. 确保所有测试通过：

   ```bash
   pytest
   ```

4. 提交代码，使用清晰的 commit message：

   ```bash
   git commit -m "feat: 添加导出功能"
   ```

5. 推送并创建 Pull Request

## Commit 规范

请使用以下前缀：

| 前缀 | 用途 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | 修复 bug |
| `docs:` | 文档更新 |
| `refactor:` | 代码重构 |
| `test:` | 测试相关 |
| `chore:` | 构建/工具相关 |

## 代码风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 规范
- 使用类型注解（Type Hints）
- 为所有公开函数/类添加文档字符串
- 保持函数单一职责
- 每个函数尽量不超过 30 行

## 报告问题

如果发现 bug 或有功能建议，请创建 Issue 并包含：

- 问题的清晰描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（Python 版本、操作系统）

## 行为准则

请保持友善和尊重，共同营造友好的开源社区氛围。
