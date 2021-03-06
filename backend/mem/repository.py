from typing import Type

from sqlalchemy import and_, func, select
from sqlalchemy.orm import with_expression

from backend.core.repository import BaseRepository
from backend.mem import schemas, models
from backend.mem.models import LikeOfMem, SkipOfMem


class MemRepository(
    BaseRepository[
        models.Mem,
        schemas.MemPydantic,
        schemas.MemInCreatePydantic,
        schemas.MemInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Mem]:
        return models.Mem

    async def get_next_for_user(self, user):
        q = await self.session.execute(
            self.get_query().
            outerjoin(LikeOfMem, and_(self._model.id == LikeOfMem.mem_id,
                                      LikeOfMem.user_id == user.id)).
            outerjoin(SkipOfMem, and_(self._model.id == SkipOfMem.mem_id,
                                      SkipOfMem.user_id == user.id)).
            where(LikeOfMem.id.is_(None)).
            where(SkipOfMem.id.is_(None)).
            order_by(self._model.id.desc())
        )
        return q.scalars().first()

    async def get_stat(self):
        q = await self.session.execute(
            self.get_query().
            join(LikeOfMem, isouter=True).
            options(with_expression(models.Mem.likes_count, func.count(LikeOfMem.id))).
            join(SkipOfMem, isouter=True).
            options(with_expression(models.Mem.skips_count, func.count(SkipOfMem.id))).
            group_by(self._model.id).
            order_by(func.count(LikeOfMem.id).desc()).
            limit(5)
        )
        return q.scalars().all()


class LikeOfMemRepository(
    BaseRepository[
        models.LikeOfMem,
        schemas.LikeOfMemPydantic,
        schemas.LikeOfMemInCreatePydantic,
        schemas.LikeOfMemInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.LikeOfMem]:
        return models.LikeOfMem

    async def get(self, mem_id, user_id):
        q = await self.session.execute(self.get_query().filter(self._model.mem_id == mem_id).
                                       filter(self._model.user_id == user_id))
        return q.scalars().first()


class SkipOfMemRepository(
    BaseRepository[
        models.SkipOfMem,
        schemas.SkipOfMemPydantic,
        schemas.SkipOfMemInCreatePydantic,
        schemas.SkipOfMemInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.SkipOfMem]:
        return models.SkipOfMem

    async def get(self, mem_id, user_id):
        q = await self.session.execute(self.get_query().filter(self._model.mem_id == mem_id).
                                       filter(self._model.user_id == user_id))
        return q.scalars().first()
