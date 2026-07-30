"""命令行接口单元测试。"""

import pytest

from todo_cli.cli import TodoCLI, format_todos
from todo_cli.models import Priority, Todo
from todo_cli.storage import TodoStorage


@pytest.fixture
def cli(tmp_path):
    """创建使用临时存储的 CLI 实例。"""
    storage = TodoStorage(str(tmp_path / "test_todos.json"))
    return TodoCLI(storage=storage)


class TestTodoCLI:
    """TodoCLI 测试。"""

    def setup_method(self):
        Todo._next_id = 1

    def test_add(self, cli):
        todo = cli.add("新任务", "描述", "high")
        assert todo.title == "新任务"
        assert todo.priority == Priority.HIGH
        assert len(cli.todos) == 1

    def test_add_persists(self, cli):
        cli.add("持久化测试")
        new_cli = TodoCLI(storage=cli.storage)
        assert len(new_cli.todos) == 1
        assert new_cli.todos[0].title == "持久化测试"

    def test_list_all(self, cli):
        cli.add("任务1")
        cli.add("任务2")
        todos = cli.list_todos(show_all=True)
        assert len(todos) == 2

    def test_list_incomplete_only(self, cli):
        cli.add("未完成")
        cli.add("已完成")
        cli.complete(2)
        todos = cli.list_todos(show_all=False)
        assert len(todos) == 1
        assert todos[0].title == "未完成"

    def test_complete(self, cli):
        cli.add("完成任务")
        todo = cli.complete(1)
        assert todo is not None
        assert todo.completed is True

    def test_complete_not_found(self, cli):
        cli.add("任务")
        todo = cli.complete(999)
        assert todo is None

    def test_uncomplete(self, cli):
        cli.add("任务")
        cli.complete(1)
        todo = cli.uncomplete(1)
        assert todo is not None
        assert todo.completed is False

    def test_uncomplete_not_found(self, cli):
        todo = cli.uncomplete(999)
        assert todo is None

    def test_delete(self, cli):
        cli.add("删除我")
        result = cli.delete(1)
        assert result is True
        assert len(cli.todos) == 0

    def test_delete_not_found(self, cli):
        result = cli.delete(999)
        assert result is False

    def test_clear_completed(self, cli):
        cli.add("任务1")
        cli.add("任务2")
        cli.add("任务3")
        cli.complete(1)
        cli.complete(3)

        removed = cli.clear_completed()
        assert removed == 2
        assert len(cli.todos) == 1
        assert cli.todos[0].title == "任务2"

    def test_clear_completed_empty(self, cli):
        removed = cli.clear_completed()
        assert removed == 0


class TestFormatTodos:
    """format_todos 函数测试。"""

    def setup_method(self):
        Todo._next_id = 1

    def test_empty_list(self):
        result = format_todos([])
        assert "没有待办事项" in result

    def test_with_todos(self):
        todos = [Todo(title="测试任务")]
        result = format_todos(todos)
        assert "测试任务" in result
        assert "总计" in result

    def test_with_description(self):
        todo = Todo(title="有描述的任务", description="这是详细描述")
        result = format_todos([todo])
        assert "这是详细描述" in result

    def test_summary_counts(self):
        todo1 = Todo(title="已完成")
        todo1.mark_complete()
        todo2 = Todo(title="未完成")
        result = format_todos([todo1, todo2])
        assert "已完成: 1" in result
        assert "未完成: 1" in result
