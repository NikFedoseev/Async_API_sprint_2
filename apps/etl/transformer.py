from models import Genre, Movie, Person


class Transformer:
    def _transform_persons(self, persons: list[dict]) -> dict[str, list]:
        processed_person_ids = set()
        res = {
            "directors_names": [],
            "actors_names": [],
            "writers_names": [],
            "directors": [],
            "actors": [],
            "writers": [],
        }

        for person in persons:
            person_id = person["person_id"]
            person_role = person["person_role"]
            person_full_name = person["person_full_name"]

            if person_id in processed_person_ids:
                continue

            if person_role == "actor":
                res["actors"].append({"id": person_id, "name": person_full_name})
                res["actors_names"].append(person_full_name)
            if person_role == "director":
                res["directors"].append({"id": person_id, "name": person_full_name})
                res["directors_names"].append(person_full_name)
            if person_role == "writer":
                res["writers"].append({"id": person_id, "name": person_full_name})
                res["writers_names"].append(person_full_name)
            processed_person_ids.add(person_id)

        return res

    def transform_for_movie_index(self, data):
        res = []

        for item in data:
            transformed_persons = self._transform_persons(item["persons"])

            model = Movie(
                id=item["id"],
                imdb_rating=item["rating"],
                title=item["title"],
                description=item["description"],
                genres=item["genres"],
                directors_names=transformed_persons["directors_names"],
                actors_names=transformed_persons["actors_names"],
                writers_names=transformed_persons["writers_names"],
                actors=transformed_persons["actors"],
                directors=transformed_persons["directors"],
                writers=transformed_persons["writers"],
            )

            res.append(model)

        return res

    def transform_for_person_index(self, data):
        res = []
        for item in data:
            model = Person(id=item["id"], full_name=item["full_name"], films=item["films"])
            res.append(model)
        return res

    def transform_for_genre_index(self, data):
        res = []
        for item in data:
            model = Genre(id=item["id"], name=item["name"], description=item["description"], films=item["films"])
            res.append(model)
        return res
