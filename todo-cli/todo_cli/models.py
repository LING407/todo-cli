"""数据模型模块，定义 Todo 的核心数据结构。"""

from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """待办事项优先级。"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        """从字符串创建 Priority 实例。

        Args:
            value: 优先级字符串 ("low", "medium", "high")

        Returns:
            对应的 Priority 枚举值

        Raises:
            ValueError: 当传入无效的优先级字符串时
        """
        try:
            return cls(value.lower())
        except ValueError:
            valid = ", ".join(p.value for p in cls)
            raise ValueError(f"无效的优先级 '{value}'，可选值: {valid}") from None


class Todo:
    """待办事项数据模型。"""

    _next_id = 1

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        completed: bool = False,
        created_at: Optional[str] = None,
        completed_at: Optional[str] = None,
        todo_id: Optional[int] = None,
    ) -> None:
        self.id = todo_id if todo_id is not None else Todo._next_id
        if todo_id is None:
            Todo._next_id += 1
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at

    def mark_complete(self) -> None:
        """标记为已完成。"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def mark_incomplete(self) -> None:
        """标记为未完成。"""
        self.completed = False
        self.completed_at = None

    def to_dict(self) -> dict:
        """转换为字典，用于序列化。"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """从字典创建 Todo 实例，用于反序列化。"""
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority.from_string(data.get("priority", "medium")),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
            todo_id=data.get("id"),
        )

    def __str__(self) -> str:
        status = "[x]" if self.completed else "[ ]"
        markers = {"high": "!!!", "medium": "!!", "low": "!"}
        marker = markers[self.priority.value]
        return f"{self.id}. {status} {self.title} ({marker})"

    def __repr__(self) -> str:
        return (
            f"Todo(id={self.id}, title='{self.title}', "
            f"priority={self.priority.value}, completed={self.completed})"
        )
