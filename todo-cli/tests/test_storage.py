"""存储模块单元测试。"""

import json

import pytest

from todo_cli.models import Priority, Todo
from todo_cli.storage import TodoStorage


@pytest.fixture
def temp_storage(tmp_path):
    """创建临时存储实例。"""
    file_path = tmp_path / "test_todos.json"
    return TodoStorage(str(file_path))


class TestTodoStorage:
    """TodoStorage 测试。"""

    def test_load_empty_file(self, temp_storage):
        todos = temp_storage.load()
        assert todos == []

    def test_save_and_load(self, temp_storage):
        todo1 = Todo(title="任务1", priority=Priority.HIGH)
        todo2 = Todo(title="任务2", priority=Priority.LOW)
        temp_storage.save([todo1, todo2])

        loaded = temp_storage.load()
        assert len(loaded) == 2
        assert loaded[0].title == "任务1"
        assert loaded[1].title == "任务2"

    def test_save_preserves_data(self, temp_storage):
        todo = Todo(title="保留数据", description="描述内容", priority=Priority.HIGH)
        todo.mark_complete()
        temp_storage.save([todo])

        loaded = temp_storage.load()
        assert loaded[0].title == "保留数据"
        assert loaded[0].description == "描述内容"
        assert loaded[0].priority == Priority.HIGH
        assert loaded[0].completed is True
        assert loaded[0].completed_at is not None

    def test_creates_directory(self, tmp_path):
        nested_path = tmp_path / "nested" / "dir" / "todos.json"
        storage = TodoStorage(str(nested_path))
        storage.save([Todo(title="测试")])
        assert nested_path.exists()

    def test_file_is_valid_json(self, temp_storage):
        todo = Todo(title="JSON 格式测试")
        temp_storage.save([todo])

        with open(temp_storage.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 1

    def test_id_counter_updated_on_load(self, temp_storage):
        Todo._next_id = 1
        todos = [
            Todo(title="任务1", todo_id=1),
            Todo(title="任务2", todo_id=5),
        ]
        temp_storage.save(todos)
        temp_storage.load()
        assert Todo._next_id == 6
