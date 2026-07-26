from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.category import CategoryService
from app.services.task import TaskService


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


@pytest.fixture
def category_repository_mock() -> Mock:
    """Создаем мок репозитория для каждого теста категорий."""
    return Mock(spec=CategoryRepository)


@pytest.fixture
def category_service(
    db_mock: Mock,
    category_repository_mock: Mock,
) -> CategoryService:
    """Создаём сервис с поддельными зависимостями."""
    category_service = CategoryService(db_mock)
    category_service.category_repository = category_repository_mock
    return category_service
