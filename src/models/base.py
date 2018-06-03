import src.prod_database as prod_database_controller
from peewee import Model


class BaseModel(Model):
    _manager = prod_database_controller.manager

    class Meta:
        database = prod_database_controller.database

    @classmethod
    async def async_select(cls, *args):
        if len(args) > 0:
            query = cls.select().where(*args)
        else:
            query = cls.select()
        return await cls._manager.execute(query)

    @classmethod
    async def async_get(cls, *args):
        return await cls._manager.get(cls.select().where(*args))

    @classmethod
    async def async_last(cls, order_by_column):
        return await cls._manager.get(cls.select().order_by(
            order_by_column.desc()))

    @classmethod
    async def async_create(cls, **kwargs):
        return await cls._manager.create(cls, **kwargs)

    @classmethod
    async def async_get_or_create(cls, **kwargs):
        return await cls._manager.get_or_create(cls, **kwargs)

    @classmethod
    async def async_create_or_get(cls, **kwargs):
        return await cls._manager.create_or_get(cls, **kwargs)

    @classmethod
    async def async_count(cls, condition=None):
        return await cls._manager.count(cls.select().where(condition))

    async def async_save(self):
        return await self._manager.update(self, only=self.dirty_fields)

    async def async_delete(self):
        return await self._manager.delete(self)

    @classmethod
    async def manage_data(cls, data):
        data = cls.format_from_response(data)
        obj, created = await cls.async_get_or_create(
            id=data["id"],
            defaults=data
        )
        if not created:
            await obj.update_from_data(data)

    async def update_from_data(self, data):
        for field in self._meta.fields.keys():
            setattr(self, field, data[field])
        await self.async_save()
