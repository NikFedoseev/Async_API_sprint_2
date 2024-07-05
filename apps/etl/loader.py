import json

import backoff
import httpx
from indices.genre import genre_index_config
from indices.movie import movie_index_config
from indices.person import person_index_config
from logger import logger
from models import Genre, Movie, Person


class ElasticsearchLoader:
    indices_config = {
        "movies": movie_index_config,
        "persons": person_index_config,
        "genres": genre_index_config,
    }

    def __init__(self, host: str, port: str) -> None:
        self.client = httpx.Client()
        self.service_url = f"http://{host}:{port}"

    @backoff.on_exception(backoff.expo, exception=(httpx.ConnectError, httpx.ConnectTimeout))
    def _check_index_exists(self, index_name: str) -> bool:
        response = self.client.head(f"{self.service_url}/{index_name}")
        return response.status_code == 200

    @backoff.on_exception(backoff.expo, exception=(httpx.ConnectError, httpx.ConnectTimeout))
    def _create_index(self, index_name: str) -> None:
        index_config = self.indices_config[index_name]
        self.client.put(f"{self.service_url}/{index_name}", json=index_config)

    @backoff.on_exception(backoff.expo, exception=(httpx.ConnectError, httpx.ConnectTimeout), logger=logger)
    def upload(self, index_name: str, entities: list[Movie | Person | Genre]) -> None:
        if not self._check_index_exists(index_name):
            self._create_index(index_name)

        request_content = []

        for entity in entities:
            request_content.append(json.dumps({"index": {"_index": index_name, "_id": entity.id}}))
            request_content.append(entity.model_dump_json())

        request_content = "\n".join(request_content)
        request_content += "\n"

        self.client.post(
            f"{self.service_url}/_bulk", headers={"Content-Type": "application/x-ndjson"}, content=request_content
        )
