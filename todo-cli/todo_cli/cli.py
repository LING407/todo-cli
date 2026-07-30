"""命令行接口模块。"""

import argparse
import sys
from typing import List, Optional

from .models import Priority, Todo
from .storage import TodoStorage


class TodoCLI:
    """待办事项命令行工具。"""

    def __init__(self, storage: Optional[TodoStorage] = None) -> None:
        self.storage = storage or TodoStorage()
        self.todos: List[Todo] = self.storage.load()

    def add(self, title: str, description: str = "", priority: str = "medium") -> Todo:
        """添加新待办事项。"""
        todo = Todo(
            title=title,
            description=description,
            priority=Priority.from_string(priority),
        )
        self.todos.append(todo)
        self.storage.save(self.todos)
        return todo

    def list_todos(self, show_all: bool = True) -> List[Todo]:
        """列出待办事项。

        Args:
            show_all: True 显示全部，False 仅显示未完成
        """
        if show_all:
            return self.todos
        return [t for t in self.todos if not t.completed]

    def complete(self, todo_id: int) -> Optional[Todo]:
        """标记待办事项为已完成。"""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.mark_complete()
                self.storage.save(self.todos)
                return todo
        return None

    def uncomplete(self, todo_id: int) -> Optional[Todo]:
        """标记待办事项为未完成。"""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.mark_incomplete()
                self.storage.save(self.todos)
                return todo
        return None

    def delete(self, todo_id: int) -> bool:
        """删除待办事项。"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos.pop(i)
                self.storage.save(self.todos)
                return True
        return False

    def clear_completed(self) -> int:
        """清除所有已完成的待办事项。

        Returns:
            被清除的数量
        """
        before = len(self.todos)
        self.todos = [t for t in self.todos if not t.completed]
        removed = before - len(self.todos)
        self.storage.save(self.todos)
        return removed


def format_todos(todos: List[Todo]) -> str:
    """格式化待办事项列表输出。"""
    if not todos:
        return "没有待办事项。使用 'add' 命令添加一个吧！"

    lines = ["待办事项列表:", "-" * 40]
    for todo in todos:
        lines.append(str(todo))
        if todo.description:
            lines.append(f"     描述: {todo.description}")
    lines.append("-" * 40)

    completed = sum(1 for t in todos if t.completed)
    total = len(todos)
    lines.append(f"总计: {total} | 已完成: {completed} | 未完成: {total - completed}")
    return "\n".join(lines)


def main() -> None:
    """主入口函数。"""
    parser = argparse.ArgumentParser(
        prog="todo-cli",
        description="一个简洁的命令行待办事项管理工具",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新待办事项")
    add_parser.add_argument("title", help="待办事项标题")
    add_parser.add_argument("-d", "--description", default="", help="待办事项描述")
    add_parser.add_argument(
        "-p",
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="优先级 (默认: medium)",
    )

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出待办事项")
    list_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="显示所有待办事项（包括已完成的）",
    )

    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="标记待办事项为已完成")
    complete_parser.add_argument("id", type=int, help="待办事项 ID")

    # uncomplete 命令
    uncomplete_parser = subparsers.add_parser("uncomplete", help="标记待办事项为未完成")
    uncomplete_parser.add_argument("id", type=int, help="待办事项 ID")

    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除待办事项")
    delete_parser.add_argument("id", type=int, help="待办事项 ID")

    # clear 命令
    subparsers.add_parser("clear", help="清除所有已完成的待办事项")

    args = parser.parse_args()
    cli = TodoCLI()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "add":
        todo = cli.add(args.title, args.description, args.priority)
        print(f"已添加: {todo}")

    elif args.command == "list":
        todos = cli.list_todos(show_all=args.all)
        print(format_todos(todos))

    elif args.command == "complete":
        todo = cli.complete(args.id)
        if todo:
            print(f"已完成: {todo}")
        else:
            print(f"未找到 ID 为 {args.id} 的待办事项")
            sys.exit(1)

    elif args.command == "uncomplete":
        todo = cli.uncomplete(args.id)
        if todo:
            print(f"已取消完成: {todo}")
        else:
            print(f"未找到 ID 为 {args.id} 的待办事项")
            sys.exit(1)

    elif args.command == "delete":
        if cli.delete(args.id):
            print(f"已删除 ID 为 {args.id} 的待办事项")
        else:
            print(f"未找到 ID 为 {args.id} 的待办事项")
            sys.exit(1)

    elif args.command == "clear":
        removed = cli.clear_completed()
        print(f"已清除 {removed} 个已完成的待办事项")


if __name__ == "__main__":
    main()
