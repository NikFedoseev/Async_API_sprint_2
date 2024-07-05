from collections.abc import Generator
from datetime import datetime
from typing import Any, Literal

import backoff
import psycopg2
from logger import logger


class PostgresProducer:
    def __init__(self, conn: psycopg2.extensions.connection, extract_size: int) -> None:
        self.conn = conn
        self.extract_size = extract_size

    def _get_query(
        self,
        table_name: str,
        modified_after: str,
    ) -> str:
        return f"""
            SELECT id, modified
            FROM content.{table_name}
            WHERE modified > '{modified_after}'
            ORDER BY modified;
        """

    @backoff.on_exception(backoff.expo, exception=(psycopg2.OperationalError, psycopg2.InterfaceError), logger=logger)
    def _iter_over_table(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)

        while True:
            rows = cursor.fetchmany(size=self.extract_size)
            if not rows:
                break
            yield [dict(row) for row in rows]

    def check_filmwork_updates(
        self, last_updated_time: str
    ) -> Generator[tuple[Literal["film_work", "person", "genre"], list[str], datetime], Any, None]:
        for table in ("film_work", "person", "genre"):
            query = self._get_query(table_name=table, modified_after=last_updated_time)

            for entity_pack in self._iter_over_table(query):
                entity_ids = [entity["id"] for entity in entity_pack]
                modified_date = entity_pack[-1]["modified"]

                yield table, entity_ids, modified_date

    def check_person_updates(self, last_updated_time: str) -> Generator[tuple[list[str], datetime], Any, None]:
        query = self._get_query(table_name="person", modified_after=last_updated_time)

        for entity_pack in self._iter_over_table(query):
            entity_ids = [entity["id"] for entity in entity_pack]
            modified_date = entity_pack[-1]["modified"]

            yield entity_ids, modified_date

    def check_genre_updates(self, last_updated_time: str) -> Generator[tuple[list[str], datetime], Any, None]:
        query = self._get_query(table_name="genre", modified_after=last_updated_time)

        for entity_pack in self._iter_over_table(query):
            entity_ids = [entity["id"] for entity in entity_pack]
            modified_date = entity_pack[-1]["modified"]

            yield entity_ids, modified_date
