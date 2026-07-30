Todo CLI

一个简洁、高效的命令行待办事项管理工具，帮助你在终端中轻松管理日常任务。

功能特性

- 添加、删除、完成/取消完成待办事项
- 支持任务优先级（高/中/低）
- 支持任务描述
- 数据持久化存储（JSON 格式）
- 清晰的终端输出格式
- 零运行时依赖（仅使用 Python 标准库）

安装

### 从源码安装

```bash
git clone https://github.com/LING407/todo-cli.git
cd todo-cli
pip install -e .
```

安装后可直接使用 `todo` 命令。

### 直接运行（无需安装）

```bash
python -m todo_cli
```

## 使用方法

### 添加待办事项

```bash
todo add "完成项目报告" -d "下周五前提交" -p high
```

输出示例：

```
已添加: 1. [ ] 完成项目报告 (!!!)
```

### 列出待办事项

```bash
todo list          # 仅显示未完成事项
todo list -a       # 显示所有事项（包括已完成）
```

输出示例：

```
待办事项列表:
----------------------------------------
1. [ ] 完成项目报告 (!!!)
     描述: 下周五前提交
2. [x] 买菜 (!)
----------------------------------------
总计: 2 | 已完成: 1 | 未完成: 1
```

### 标记为已完成

```bash
todo complete 1
```

### 取消完成

```bash
todo uncomplete 1
```

### 删除待办事项

```bash
todo delete 1
```

### 清除所有已完成事项

```bash
todo clear
```

## 项目结构

```
todo-cli/
├── todo_cli/
│   ├── __init__.py      # 包初始化
│   ├── __main__.py      # 模块入口（支持 python -m）
│   ├── cli.py           # 命令行接口与业务逻辑
│   ├── models.py        # 数据模型（Todo, Priority）
│   └── storage.py       # JSON 文件存储
├── tests/
│   ├── __init__.py
│   ├── test_models.py   # 模型单元测试
│   ├── test_storage.py  # 存储单元测试
│   └── test_cli.py      # CLI 单元测试
├── .gitignore
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
└── setup.py
```

## 开发

### 环境准备

```bash
git clone https://github.com/LING407/todo-cli.git
cd todo-cli
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 运行测试

```bash
pytest
```

### 运行测试并查看覆盖率

```bash
pytest --cov=todo_cli
```

## 技术栈

- **Python 3.8+** - 编程语言
- **argparse** - 命令行参数解析（标准库）
- **json** - 数据持久化（标准库）
- **pytest** - 测试框架

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
