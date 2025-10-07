# Python modules
from typing import Any
from random import choice, choices
from datetime import datetime

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import QuerySet

# Project modules
from apps.tasks.models import Task, Project, UserTask


class Command(BaseCommand):
    help = "Generate tasks data for testing purposes"

    EMAIL_DOMAINS = (
        "example.com",
        "test.com",
        "sample.org",
        "demo.net",
        "mail.com",
    )
    SOME_WORDS = (
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "sed",
        "do",
        "eiusmod",
        "tempor",
        "incididunt",
        "ut",
        "labore",
        "et",
        "dolore",
        "magna",
        "aliqua",
    )

    def __generate_users(self, user_count: int = 100) -> None:
        """
        Generates users for testing purposes.
        """

        USER_PASSWORD = make_password(password="12345")
        created_users: list[User] = []
        users_before: int = User.objects.count()
        i: int
        for i in range(user_count):
            username: str = f"user {i+1}"
            email: str = f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_users.append(
                User(
                    username=username,
                    email=email,
                    password=USER_PASSWORD,
                )
            )

        User.objects.bulk_create(created_users, ignore_conflicts=True)
        users_after: int = User.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {users_after - users_before} users."
            )
        )

    def __generate_projects(self, project_count: int = 100) -> None:
        """
        Generates projects for testing purposes.
        """

        create_projects: list[Project] = []
        projects_before: int = Project.objects.count()
        existed_users: QuerySet[User] = User.objects.all()

        i: int
        for i in range(project_count):
            name: str = " ".join(choices(self.SOME_WORDS, k=4)).capitalize()
            author: User = choice(existed_users)
            create_projects.append(
                Project(
                    name=name,
                    author=author
                )
            )
        Project.objects.bulk_create(create_projects, ignore_conflicts=True)

        project: Project
        for project in Project.objects.all():
            project.users.add(*choices(existed_users, k=10))

        projects_after: int = Project.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {projects_after - projects_before} projects."
            )
        )

    def __generate_tasks(self, task_count:int = 20) -> None:
        """
        generate tasksk 
        """
        created_tasks: list[Task] = []
        tasks_before: int = Task.objects.count()
        existed_projects: QuerySet[Project] = Project.objects.all()

        for i in range(task_count):
            name: str = " ".join(choices(self.SOME_WORDS, k=3)).capitalize()
            description: str = " ".join(choices(self.SOME_WORDS, k=10)).capitalize()
            status: int = choice([
                Task.STATUS_TODO,
                Task.STATUS_IN_PROGRESS,
                Task.STATUS_DONE
            ])
            project: Project = choice(existed_projects)
            created_tasks.append(
                Task(
                    name=name,
                    description=description,
                    status=status,
                    project=project,
                )
            )
        Task.objects.bulk_create(created_tasks, ignore_conflicts=True)

        tasks_after: int = Task.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {tasks_after - tasks_before} tasks."
            )
        )

    def __generate_user_tasks(self, user_task_count:int = 20) -> None:
        """
        generate user_tasks
        """
        created_user_tasks: list[UserTask] = []
        usertasks_before: int = UserTask.objects.count()
        existed_tasks: QuerySet[Task] = Task.objects.all()
        existed_users :QuerySet[User] = User.objects.all()

        for i in range(user_task_count):
            user : User = choice(existed_users)
            task: Task = choice(existed_tasks)
            created_user_tasks.append(
                UserTask(
                    user = user,
                    task = task,
                )
            )
        
        UserTask.objects.bulk_create(created_user_tasks, ignore_conflicts=True)

        usertasks_after: int = UserTask.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {usertasks_after - usertasks_before} users."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        start_time: datetime = datetime.now()

        self.__generate_users(user_count=500)
        self.__generate_projects(project_count=200)
        self.__generate_tasks(task_count=20)
        self.__generate_user_tasks(user_task_count=20)
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time).total_seconds()
            )
        )