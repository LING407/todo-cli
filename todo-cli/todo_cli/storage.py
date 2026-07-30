"""存储模块，负责将待办事项持久化到 JSON 文件。"""

import json
import os
from typing import List, Optional

from .models import Todo


class TodoStorage:
    """基于 JSON 文件的待办事项存储。"""

    DEFAULT_PATH = os.path.join(os.path.expanduser("~"), ".todo-cli", "todos.json")

    def __init__(self, file_path: Optional[str] = None) -> None:
        self.file_path = file_path or self.DEFAULT_PATH
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """确保存储目录存在。"""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def load(self) -> List[Todo]:
        """从文件加载所有待办事项。

        Returns:
            Todo 对象列表，文件不存在时返回空列表

        Raises:
            RuntimeError: 当文件内容无法解析时
        """
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            todos = [Todo.from_dict(item) for item in data]
            self._update_id_counter(todos)
            return todos
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"无法解析存储文件: {e}") from e

    def save(self, todos: List[Todo]) -> None:
        """保存所有待办事项到文件。"""
        data = [todo.to_dict() for todo in todos]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _update_id_counter(todos: List[Todo]) -> None:
        """更新 ID 计数器，避免 ID 冲突。"""
        if todos:
            max_id = max(todo.id for todo in todos)
            Todo._next_id = max_id + 1
