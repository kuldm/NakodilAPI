from sqlalchemy import select

from repositories.mappers.base import DataMapper


class BaseRepository():
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        """Извлекает все записи"""
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
