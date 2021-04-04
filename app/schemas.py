from typing import List, Optional

from pydantic import BaseModel, PositiveInt


class Base(BaseModel):
    class Config:
        orm_mode = True


class DeckBase(Base):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class DeckCreate(DeckBase):
    pass


class Deck(DeckBase):
    id: PositiveInt


class Decks(Base):
    decks: List[Deck]


class CardBase(Base):
    front: str
    back: Optional[str] = None
    hint: Optional[str] = None

    class Config:
        orm_mode = True


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: PositiveInt
    deck_id: Optional[PositiveInt] = None


class Cards(Base):
    cards: List[Card]
