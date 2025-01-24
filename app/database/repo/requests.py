from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from database.repo.users import UsersRepo

@dataclass
class RequestsRepo:
    session: AsyncSession

    @property
    def characters(self):
        return CharactersRepo(self.session)

    @property
    def user_characters(self):
        return UserCharactersRepo(self.session)

    @property
    def wallet(self):
        return WalletRepo(self.session)

    @property
    def wallet_history(self):
        return WalletHistoryRepo(self.session)

    @property
    def mining(self):
        return MiningRepo(self.session)

    @property
    def mining_boost(self):
        return MiningBoostRepo(self.session)

    @property
    def users(self):
        return UsersRepo(self.session)

    @property
    def user_login(self):
        return UserLoginRepo(self.session)

    @property
    def leaders_check(self):
        return LeadersCheckRepo(self.session)

    @property
    def mining_ref(self):
        return MiningRefRepo(self.session)

    @property
    def partners(self):
        return PartnersRepo(self.session)

    @property
    def user_partners(self):
        return UserPartnersRepo(self.session)

    @property
    def user_tickets(self):
        return UserTicketsRepo(self.session)

    @property
    def tasks(self):
        return TasksRepo(self.session)

    @property
    def spin_results(self):
        return SpinResultsRepo(self.session)

    @property
    def user_external_tasks(self):
        return UserExternalTasksRepo(self.session)

    @property
    def user_funnel(self):
        return UserFunnelRepo(self.session)

    @property
    def voucher(self):
        return VoucherRepo(self.session)

    @property
    def barza_responses(self):
        return BarzaResponsesRepo(self.session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()
