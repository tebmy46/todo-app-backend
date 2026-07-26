from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFound, CategoryService


def test_list_categories_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="Category-1", name="Food"),
        CategoryORM(id="Category-2", name="Games"),
    ]

    result = category_service.list_categories()

    assert result == [
        CategorySchema(id="Category-1", name="Food"),
        CategorySchema(id="Category-2", name="Games"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    created_category = CategoryORM(id="category-1", name="Работа")
    category_repository_mock.create.return_value = created_category

    result = category_service.create_category(CategoryCreateSchema(name="Работа"))

    category_repository_mock.create.assert_called_once_with(name="Работа")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Работа",
    }


def test_update_category_changes_name(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category = CategoryORM(
        id="category-1",
        name="Старое имя",
    )
    category_repository_mock.get_by_id.return_value = category

    result = category_service.update_category(
        category_id="category-1", category_update=CategoryUpdateSchema(name="Новое имя")
    )

    category_repository_mock.get_by_id.assert_called_once_with("category-1")
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новое имя",
    }


def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.update_category(
            "missing-category", CategoryUpdateSchema(name="Не вышло")
        )

    category_repository_mock.get_by_id.assert_called_once_with("missing-category")
    db_mock.commit.assert_not_called()


def test_delete_category_deletes_and_commits(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category = CategoryORM(
        id="category-1",
        name="Работа",
    )
    category_repository_mock.get_by_id.return_value = category

    category_service.delete_category("category-1")

    category_repository_mock.get_by_id.assert_called_once_with(category_id="category-1")
    category_repository_mock.delete.assert_called_once_with(category)
    db_mock.commit.assert_called_once_with()


def test_delete_category_raises_when_category_not_found(
    category_service: CategoryService, db_mock: Mock, category_repository_mock: Mock
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.delete_category("missing-category")

    category_repository_mock.get_by_id.assert_called_once_with(
        category_id="missing-category"
    )
    category_repository_mock.delete.assert_not_called()
    db_mock.commit.assert_not_called()
