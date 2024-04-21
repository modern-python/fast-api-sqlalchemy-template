import typing

from sqlalchemy.ext.asyncio import AsyncEngine
from that_depends import BaseContainer, providers

from app.db.resource import create_sa_engine, create_session
from app.repositories.decks import CardsRepository, DecksRepository


class IOCContainer(BaseContainer):
    database_engine = providers.AsyncResource(create_sa_engine)
    session = providers.AsyncContextResource(create_session, engine=typing.cast(AsyncEngine, database_engine))

    decks_repo = providers.Factory(DecksRepository, session=session)
    cards_repo = providers.Factory(CardsRepository, session=session)
