from datetime import date
from src.repositories.base import AbstractRepository
from pydantic import BaseModel


class BaseService:
    def __init__(self, base_repo: AbstractRepository):
        self.base_repo: AbstractRepository = base_repo

    async def create_entity(self, entity):
        if isinstance(entity, BaseModel):
            entity = entity.model_dump()
        entity_id = await self.base_repo.add_one(data=entity)
        if entity_id:
            full_res = await self.get_entity(id=entity_id)
            return full_res
        return None

    async def get_entity(self, **filters):
        entity = await self.base_repo.get_one(**filters)
        if entity is None:
            return None
        return entity.to_read_model()

    async def get_entities(
        self,
        start_date: date = None,
        end_date: date = None,
        date_filter: str = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None,
        order_desc: bool = False,
        **filters
    ):
        entities = await self.base_repo.get_all(
            start_date=start_date,
            end_date=end_date,
            date_filter=date_filter,
            limit=limit,
            offset=offset,
            order_by=order_by,
            order_desc=order_desc,
            **filters
        )
        res = [row[0].to_read_model() for row in entities]
        return res

    async def get_count(self, **filters):
        return await self.base_repo.get_count(**filters)

    async def get_entities_in(self, **in_filters):
        entities = await self.base_repo.get_all_in(**in_filters)
        res = [row[0].to_read_model() for row in entities]
        return res

    async def update_entity(self, entity, **filters):
        if isinstance(entity, BaseModel):
            entity = entity.model_dump()
        updated_entity = await self.base_repo.edit_one(**filters, data=entity)
        return updated_entity.to_read_model()

    async def delete_entity(self, **filters):
        return await self.base_repo.delete_one(**filters)
