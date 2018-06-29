#!/usr/bin/env python
from typing import Dict
from typing import TypeVar
from sqlalchemy.orm import Session
from helpers import id_helper
from models import user
from models import board
from models import board_label
from models import board_list
from models import board_user
from models import card
from models import card_label
from models import card_list


SessionType = TypeVar("SessionType", bound=Session)

LOG_CLASS_MAPPING = {
    user.User: user.UserLog,
    board.Board: board.BoardLog,
    board_label.BoardLabel: board_label.BoardLabelLog,
    board_list.BoardList: board_list.BoardListLog,
    board_user.BoardUser: board_user.BoardUserLog,
    card.Card: card.CardLog,
    card_label.CardLabel: card_label.CardLabelLog,
    card_list.CardList: card_list.CardListLog
}


def _log(
        session: SessionType, model_cls, entity_id, current_state: Dict,
        previous_state: Dict = None):

    log_cls = LOG_CLASS_MAPPING[model_cls]
    obj = log_cls(
        id=id_helper.generate_id(), entity_id=entity_id,
        current_state=str(current_state),
        created_by_id=current_state["created_by_id"]
    )

    if previous_state:
        obj.previous_state = str(previous_state)

    session.add(obj)


def log_insert(
        session: SessionType, model_cls, entity_id, current_state: Dict):
    _log(session, model_cls, entity_id, current_state)


def log_update(
        session: SessionType, model_cls, entity_id, current_state: Dict,
        previous_state: Dict):
    _log(session, model_cls, entity_id, current_state, previous_state)
