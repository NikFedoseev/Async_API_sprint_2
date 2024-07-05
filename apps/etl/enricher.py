from typing import Literal

import psycopg2
from utils import BackoffQueryMixin, UUIDEscapingMixin


class PostgresEnricher(BackoffQueryMixin, UUIDEscapingMixin):
    related_tables = {"person": "person_film_work", "genre": "genre_film_work", "film_work": None}

    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self.conn = conn

    def _get_query(
        self,
        table_name: str,
        ids: list[str],
    ) -> str:
        return f"""
            SELECT fw.id
            FROM content.film_work fw
            LEFT JOIN content.{self.related_tables[table_name]} rt ON rt.film_work_id = fw.id
            WHERE rt.{table_name}_id IN ({self.escape_uuids(ids)})
            ORDER BY modified;
        """

    def enrich(self, table: Literal["film_work", "person", "genre"], entity_ids: list[str]) -> list[str]:
        if table == "film_work":
            return entity_ids

        if table in ("person", "genre"):
            rows_dict = self._execute_query(conn=self.conn, query=self._get_query(table_name=table, ids=entity_ids))
            return [row["id"] for row in rows_dict]
