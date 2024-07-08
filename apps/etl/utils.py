from contextlib import closing
from typing import Any

import backoff
import psycopg2
import psycopg2.extras
from logger import logger

from settings import settings


class BackoffQueryMixin:
    @backoff.on_exception(backoff.expo, exception=(psycopg2.OperationalError, psycopg2.InterfaceError), logger=logger)
    def _execute_query(self, conn: psycopg2.extensions.connection, query: str) -> list[Any]:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


class UUIDEscapingMixin:
    def escape_uuids(self, uuids: list[str]):
        return ", ".join([f"'{uuid}'" for uuid in uuids])


@backoff.on_exception(backoff.expo, exception=(psycopg2.OperationalError, psycopg2.InterfaceError), logger=logger)
def get_postges_connection():
    dsl = {
        "dbname": settings.pg.DB,
        "user": settings.pg.USER,
        "password": settings.pg.PASSWORD,
        "host": settings.pg.HOST,
        "port": settings.pg.PORT,
    }
    return closing(psycopg2.connect(**dsl, cursor_factory=psycopg2.extras.DictCursor))  # type: ignore
