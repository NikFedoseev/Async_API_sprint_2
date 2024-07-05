from itertools import groupby
from operator import itemgetter

import psycopg2
from utils import BackoffQueryMixin, UUIDEscapingMixin


class PostgresMerger(BackoffQueryMixin, UUIDEscapingMixin):
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self.conn = conn

    def _get_query_for_movie_index(self, film_work_ids: list[str]) -> str:
        return f"""
            SELECT
                fw.id,
                fw.title,
                fw.description,
                fw.rating,
                fw.type,
                fw.created,
                fw.modified,
                pfw.role as person_role,
                p.id as person_id,
                p.full_name as person_full_name,
                g.name as genre_name
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.id IN ({self.escape_uuids(film_work_ids)});
        """

    def _get_query_for_person_index(self, person_ids: list[str]) -> str:
        return f"""
            SELECT
                p.id,
                p.full_name,
                pfw.film_work_id as filmwork_id,
                fw.title,
                fw.rating,
                pfw.role
            FROM content.person p
            LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
            LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
            WHERE p.id IN ({self.escape_uuids(person_ids)});
        """

    def _get_query_for_genre_index(self, genre_ids: list[str]) -> str:
        return f"""
            SELECT
                g.id,
                g.name,
                g.description,
                gfw.film_work_id as filmwork_id,
                fw.title,
                fw.rating
            FROM content.genre g
            LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
            LEFT JOIN content.film_work fw ON fw.id = gfw.film_work_id
            WHERE g.id IN ({self.escape_uuids(genre_ids)});
        """

    def _collect_data_for_movie_index(self, data_by_id: dict[str, list[dict]]) -> list[dict]:
        res = []
        for entity_id, entity_data in data_by_id.items():
            genres = list(set(map(itemgetter("genre_name"), entity_data)))

            persons = [
                {
                    "person_id": entity["person_id"],
                    "person_role": entity["person_role"],
                    "person_full_name": entity["person_full_name"],
                }
                for entity in entity_data
            ]

            res.append(
                {
                    "id": entity_id,
                    "title": entity_data[0]["title"],
                    "description": entity_data[0]["description"],
                    "rating": entity_data[0]["rating"],
                    "type": entity_data[0]["type"],
                    "created": entity_data[0]["created"],
                    "modified": entity_data[0]["modified"],
                    "genres": genres,
                    "persons": persons,
                }
            )
        return res

    def collect_data_for_person_index(self, data_by_id: dict[str, list[dict]]) -> list[dict]:
        res = []
        for entity_id, entity_data in data_by_id.items():
            films = []
            for key, data in groupby(entity_data, itemgetter("filmwork_id")):
                data = list(data)
                films.append(
                    {
                        "id": key,
                        "title": data[0]["title"],
                        "rating": data[0]["rating"],
                        "roles": list(map(itemgetter("role"), data)),
                    }
                )
            res.append({"id": entity_id, "full_name": entity_data[0]["full_name"], "films": films})
        return res

    def collect_data_for_genre_index(self, data_by_id: dict[str, list[dict]]) -> list[dict]:
        res = []
        for entity_id, entity_data in data_by_id.items():
            films = [
                {
                    "id": entity["filmwork_id"],
                    "title": entity["title"],
                    "rating": entity["rating"],
                }
                for entity in entity_data
            ]
            res.append(
                {
                    "id": entity_id,
                    "name": entity_data[0]["name"],
                    "description": entity_data[0]["description"],
                    "films": films,
                }
            )
        return res

    def merge(self, data, for_index: str) -> list[dict]:
        if for_index == "movies":
            query = self._get_query_for_movie_index(data)
        elif for_index == "persons":
            query = self._get_query_for_person_index(data)
        elif for_index == "genres":
            query = self._get_query_for_genre_index(data)
        else:
            raise Exception("unknown index")

        raw_data = self._execute_query(conn=self.conn, query=query)

        data_by_id: dict[str, list[dict]] = {}

        for row in raw_data:
            if not data_by_id.get(row["id"]):
                data_by_id[row["id"]] = [row]
                continue
            data_by_id[row["id"]].append(row)

        if for_index == "movies":
            return self._collect_data_for_movie_index(data_by_id)
        if for_index == "persons":
            return self.collect_data_for_person_index(data_by_id)
        if for_index == "genres":
            return self.collect_data_for_genre_index(data_by_id)
