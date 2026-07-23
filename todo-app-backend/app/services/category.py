from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


class CategoryNotFound(Exception):
    """Категория не найдна."""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories_orm]

    def create_category(
        self,
        category_create: CategoryCreateSchema,
    ) -> CategorySchema:
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(
        self,
        category_id: str,
        category_update: CategoryUpdateSchema,
    ) -> CategorySchema:
        category_orm = self.category_repository.get_by_id(category_id)

        if category_orm is None:
            raise CategoryNotFound

        if category_update.name is not None:
            category_orm.name = category_update.name

        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repository.get_by_id(
            category_id=category_id
        )

        if category_for_delete is None:
            raise CategoryNotFound

        self.category_repository.delete(category_for_delete)
        self.db.commit()
