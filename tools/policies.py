from typing import TypedDict


class PolicyFragment(TypedDict):
    source: str
    text: str
    score: float


class PolicySearchResult(TypedDict):
    results: list[PolicyFragment]


def search_policies(query: str) -> PolicySearchResult:
    query = query.strip()
    if not query:
        raise ValueError("Ingresá una consulta sobre las políticas logísticas.")

    from rag.search import search

    return {"results": search(query)}
