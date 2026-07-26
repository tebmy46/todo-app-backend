from unittest.mock import Mock

import pytest
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from sqlalchemy.orm import Session


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД для каждого теста."""
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    """Создаём мок репозитория для каждого теста."""
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    """Создаём сервис с поддельными зависимостями."""
    task_service = TaskService(db_mock)
    task_service.task_repository = repository_mock
    return task_service
