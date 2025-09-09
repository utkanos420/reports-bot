from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from database.core import User, Report, db_helper


class DBMethods:
    def __init__(self):
        self.session_factory = db_helper.session_factory

    async def get_user(self, user_id: int) -> User | None:
        async with self.session_factory() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            return result.scalars().first()

    async def create_user(self, user_id: int, username: str) -> User:
        async with self.session_factory() as session:
            user = User(user_id=user_id, user_username=username, users_reports_count=0)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_data(self, user_id: int):
        user = await self.get_user(user_id)
        # profile = await self.get_profile(user_id)  # если есть профиль
        return user  # , profile

    async def create_user_report(
        self,
        user_id: int,
        report_floor: int,
        report_cabinet: int,
        report_reason: str,
        report_description: str = None
    ) -> Report:
        async with self.session_factory() as session:
            new_report = Report(
                user_id=user_id,
                report_floor=report_floor,
                report_cabinet=report_cabinet,
                report_reason=report_reason,
                report_description=report_description,
            )

            session.add(new_report)
            await session.commit()
            await session.refresh(new_report)
            return new_report

    async def get_user_report_by_id(self, report_id: int) -> Report | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(Report)
                .options(joinedload(Report.user))
                .filter_by(id=report_id)
            )
            return result.scalars().first()

    async def mute_user_by_id(self, user_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            user = result.scalars().first()
            if not user:
                return False
            user.is_muted = True
            await session.commit()
            return True

    async def unmute_user_by_id(self, user_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            user = result.scalars().first()
            if not user:
                return False
            user.is_muted = False
            await session.commit()
            return True

    async def user_is_muted(self, user_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(User.is_muted).filter_by(user_id=user_id))
            return bool(result.scalar())
