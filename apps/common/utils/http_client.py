import json
from dataclasses import dataclass, asdict, Field, field
from enum import Enum
from typing import Literal, List
import requests
from pydantic import BaseModel
class HttpMethod(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

class GraphQueryResult(BaseModel):
    concept:list[str] = []
    triple:list[str] = []
    retrieval_content:list[str] = []

class GraphQueryResponse(BaseModel):
    code: int
    message: str
    message_key: str | None =None
    data: GraphQueryResult | None = None

JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list['JsonValue'] | dict[str, 'JsonValue']

@dataclass(frozen=True)
class HttpRequest:
    method: HttpMethod
    url: str
    headers: dict[str, str] | None = None
    query_params: dict[str, str] | None = None
    json_body: JsonValue | None = None
    data: str | bytes | None = None
    timeout: float = 10.0
    verify_tls: bool = True

@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    text: str
    headers: dict[str, str]

    def json(self) -> JsonValue:
        return json.loads(self.text)


class HttpClient:
    @staticmethod
    def send(request: HttpRequest) -> HttpResponse:
        try:
            response = requests.request(
                method=request.method.value,
                url=request.url,
                headers=request.headers,
                params=request.query_params,
                json=request.json_body,
                data=request.data,
                timeout=request.timeout,
                verify=request.verify_tls,
            )
        except requests.RequestException as e:
            raise e
        return HttpResponse(
            status_code=int(response.status_code),
            text=str(response.text),
            headers={str(k): str(v) for k, v in response.headers.items()},
        )

    @staticmethod
    def send_or_raise(request: HttpRequest, error_code: int = 500) -> HttpResponse:
        response = HttpClient.send(request)
        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(error_code, f'HTTP request failed, status_code={response.status_code}')
        return response

@dataclass
class KagConfig:
    llmConfigId: int = 15
    maxPaths: int = 5
    searchType: Literal['both', 'concept', 'relation'] = 'both'
    conceptTopK: int = 5
    conceptSimilarity: float = 0.8
    relationTopK: int = 5
    relationSimilarity: float = 0.8
    useKeywords: bool = False
    useRag: bool = False
    useGraphRag: bool = True
    retrievalTopK: int = 10
    keyRagWeight: int = 5
    instanceIds: list[str] = field(default_factory=list)
    analysisPromptId: str = 'f02d6f5d-64a2-45bf-af20-cff5eaa03329'
    resultGenerationPromptId: str = 'a7a5b476-934a-46ff-96a7-4bfe84ed86bd'
    maxHops: int = 10
    maxVisited: int = 100
    scoreLimit: float = 0.5
    cutLimit: int = 5


@dataclass(frozen=True)
class Neo4jTestQueryRequest:
    query: str
    kagConfig: KagConfig

def neo4j_test_query(query: str,instance_ids:List[str]) -> GraphQueryResponse:
    kag_config:KagConfig = KagConfig()
    kag_config.instanceIds = instance_ids
    request = HttpRequest(
        method=HttpMethod.POST,
        url='https://kag-test.felizai.cn/api/v1/neo4j/query',
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        json_body=asdict(Neo4jTestQueryRequest(query=query, kagConfig=kag_config)),
        timeout=30.0,
        verify_tls=True,
    )
    response:HttpResponse = HttpClient.send_or_raise(request)
    return GraphQueryResponse.model_validate(response.json())
if __name__ == '__main__':
    gqr:GraphQueryResponse = neo4j_test_query('如果一家元宇宙企业和一家生成式人工智能企业都获得了最高上市配套补贴',['40884ba6-a7b2-4858-b31a-beee86dc4364'])
    print(gqr.data.concept)
    print(gqr.data.triple)
    print(gqr.data.retrieval_content)