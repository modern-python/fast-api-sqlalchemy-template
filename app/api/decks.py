import typing

import fastapi
from starlette import status

from app import ioc, models, schemas
from app.db.session_context import session_context
from app.repositories.decks import CardsRepository, DecksRepository


ROUTER: typing.Final = fastapi.APIRouter()


@ROUTER.get("/decks/")
@session_context()
async def list_decks(
    decks_repo: DecksRepository = fastapi.Depends(ioc.IOCContainer.decks_repo),
) -> schemas.Decks:
    objects = await decks_repo.all()
    return typing.cast(schemas.Decks, {"items": objects})


@ROUTER.get("/decks/{deck_id}/")
@session_context()
async def get_deck(
    deck_id: int,
    decks_repo: DecksRepository = fastapi.Depends(ioc.IOCContainer.decks_repo),
) -> schemas.Deck:
    instance = await decks_repo.get_by_id(deck_id, prefetch=("cards",))
    if not instance:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck is not found")

    return typing.cast(schemas.Deck, instance)


@ROUTER.put("/decks/{deck_id}/")
@session_context()
async def update_deck(
    deck_id: int,
    data: schemas.DeckCreate,
    decks_repo: DecksRepository = fastapi.Depends(ioc.IOCContainer.decks_repo),
) -> schemas.Deck:
    instance = await decks_repo.get_by_id(deck_id)
    if not instance:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck is not found")

    await decks_repo.update_attrs(instance, **data.dict())
    await decks_repo.save(instance)
    return typing.cast(schemas.Deck, instance)


@ROUTER.post("/decks/")
@session_context()
async def create_deck(
    data: schemas.DeckCreate,
    decks_repo: DecksRepository = fastapi.Depends(ioc.IOCContainer.decks_repo),
) -> schemas.Deck:
    instance = models.Deck(**data.dict())
    await decks_repo.save(instance)
    return typing.cast(schemas.Deck, instance)


@ROUTER.get("/decks/{deck_id}/cards/")
@session_context()
async def list_cards(
    deck_id: int,
    cards_repo: CardsRepository = fastapi.Depends(ioc.IOCContainer.cards_repo),
) -> schemas.Cards:
    objects = await cards_repo.filter({"deck_id": deck_id})
    return typing.cast(schemas.Cards, {"items": objects})


@ROUTER.get("/cards/{card_id}/")
@session_context()
async def get_card(
    card_id: int,
    cards_repo: CardsRepository = fastapi.Depends(ioc.IOCContainer.cards_repo),
) -> schemas.Card:
    instance = await cards_repo.get_by_id(card_id)
    if not instance:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card is not found")
    return typing.cast(schemas.Card, instance)


@ROUTER.post("/decks/{deck_id}/cards/")
@session_context()
async def create_cards(
    deck_id: int,
    data: list[schemas.CardCreate],
    cards_repo: CardsRepository = fastapi.Depends(ioc.IOCContainer.cards_repo),
) -> schemas.Cards:
    objects = await cards_repo.bulk_create(
        [models.Card(**card.dict(), deck_id=deck_id) for card in data],
    )
    return typing.cast(schemas.Cards, {"items": objects})


@ROUTER.put("/decks/{deck_id}/cards/")
@session_context()
async def update_cards(
    deck_id: int,
    data: list[schemas.Card],
    cards_repo: CardsRepository = fastapi.Depends(ioc.IOCContainer.cards_repo),
) -> schemas.Cards:
    objects = await cards_repo.bulk_update(
        [models.Card(**card.dict(exclude={"deck_id"}), deck_id=deck_id) for card in data],
    )
    return typing.cast(schemas.Cards, {"items": objects})
