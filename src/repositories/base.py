from abc import ABC, abstractmethod
from datetime import date

from sqlalchemy import and_, asc, desc, func, insert, select, delete, update
from settings.database import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, filters):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data) -> int:
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            new_id = res.scalar_one()  # Извлечение результата до коммита
            await session.commit()
            return new_id

    async def get_all(
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
        async with async_session() as session:
            stmt = select(self.model)
            if filters:
                filter_conditions = []
                for attr, value in filters.items():
                    column = getattr(self.model, attr, None)
                    if column is not None:
                        if isinstance(value, list):
                            filter_conditions.append(column.in_(value))
                        else:
                            filter_conditions.append(column == value)
                if filter_conditions:
                    stmt = stmt.where(and_(*filter_conditions))
            if order_by:
                order_column = getattr(self.model, order_by)
                if order_desc:
                    stmt = stmt.order_by(desc(order_column))
                else:
                    stmt = stmt.order_by(asc(order_column))
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)
            if start_date and end_date:
                stmt = stmt.filter(
                    getattr(self.model, date_filter).between(start_date, end_date)
                )
            res = await session.execute(stmt)
            return res.all()

    async def get_one(self, **filters):
        async with async_session() as session:
            stmt = select(self.model).filter_by(**filters)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_count(self, **filters):
        async with async_session() as session:
            stmt = select(func.count()).select_from(self.model)
            if filters:
                filter_conditions = []
                for attr, value in filters.items():
                    column = getattr(self.model, attr, None)
                    if column is not None:
                        if isinstance(value, list):
                            filter_conditions.append(column.in_(value))
                        else:
                            filter_conditions.append(column == value)
                if filter_conditions:
                    stmt = stmt.where(and_(*filter_conditions))
            res = await session.execute(stmt)
            return res.scalar()

    async def delete_one(self, **filters):
        async with async_session() as session:
            stmt = delete(self.model).filter_by(**filters)
            result = await session.execute(stmt)
            await session.commit()
            return bool(result.rowcount)

    async def edit_one(self, data, **filters):
        async with async_session() as session:
            stmt = (
                update(self.model)
                .filter_by(**filters)
                .values(**data)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
