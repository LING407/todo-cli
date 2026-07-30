"""Todo 数据模型单元测试。"""

import pytest

from todo_cli.models import Priority, Todo


class TestPriority:
    """Priority 枚举测试。"""

    def test_from_string_valid(self):
        assert Priority.from_string("low") == Priority.LOW
        assert Priority.from_string("medium") == Priority.MEDIUM
        assert Priority.from_string("high") == Priority.HIGH

    def test_from_string_uppercase(self):
        assert Priority.from_string("HIGH") == Priority.HIGH

    def test_from_string_invalid(self):
        with pytest.raises(ValueError):
            Priority.from_string("urgent")


class TestTodo:
    """Todo 模型测试。"""

    def setup_method(self):
        Todo._next_id = 1

    def test_creation_defaults(self):
        todo = Todo(title="测试任务")
        assert todo.title == "测试任务"
        assert todo.description == ""
        assert todo.priority == Priority.MEDIUM
        assert todo.completed is False
        assert todo.id == 1

    def test_creation_with_all_fields(self):
        todo = Todo(
            title="完整任务",
            description="这是一个描述",
            priority=Priority.HIGH,
        )
        assert todo.title == "完整任务"
        assert todo.description == "这是一个描述"
        assert todo.priority == Priority.HIGH

    def test_mark_complete(self):
        todo = Todo(title="完成任务")
        todo.mark_complete()
        assert todo.completed is True
        assert todo.completed_at is not None

    def test_mark_incomplete(self):
        todo = Todo(title="取消完成")
        todo.mark_complete()
        todo.mark_incomplete()
        assert todo.completed is False
        assert todo.completed_at is None

    def test_to_dict(self):
        todo = Todo(title="字典测试", description="描述", priority=Priority.HIGH)
        data = todo.to_dict()
        assert data["title"] == "字典测试"
        assert data["description"] == "描述"
        assert data["priority"] == "high"
        assert data["completed"] is False

    def test_from_dict(self):
        data = {
            "id": 5,
            "title": "从字典创建",
            "description": "测试",
            "priority": "low",
            "completed": True,
            "created_at": "2024-01-01T00:00:00",
            "completed_at": "2024-01-02T00:00:00",
        }
        todo = Todo.from_dict(data)
        assert todo.id == 5
        assert todo.title == "从字典创建"
        assert todo.priority == Priority.LOW
        assert todo.completed is True

    def test_str_representation(self):
        todo = Todo(title="字符串测试")
        result = str(todo)
        assert "字符串测试" in result
        assert "[ ]" in result

    def test_str_completed(self):
        todo = Todo(title="已完成任务")
        todo.mark_complete()
        result = str(todo)
        assert "[x]" in result

    def test_id_increments(self):
        todo1 = Todo(title="任务1")
        todo2 = Todo(title="任务2")
        assert todo2.id == todo1.id + 1
