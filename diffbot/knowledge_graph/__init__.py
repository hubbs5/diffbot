import urllib.parse

# https://docs.diffbot.com/kgapi
# https://docs.diffbot.com/docs/en/dql-quickstart
KG_BASE_URL = "https://kg.diffbot.com/kg/v3/dql"
ARTICLE_BASE_URL = "https://api.diffbot.com/v3/article"
ENHANCE_BASE_URL = "https://kg.diffbot.com/kg/v3/enhance_endpoint"

def build_knowledge_graph_query(
    _filter: str, token: str, size: int = 50
    ):
    _url = f"?token={token}&query={urllib.parse.quote(_filter)}"
    if size is not None or size > 0:
        _url += f"&size={size}"
    url = f"{KG_BASE_URL}{_url}"
    return url


def build_knowledge_graph_post_query(
    _filter: str, token: str, type: str = "query", size: int = 50
):
    url = f"{KG_BASE_URL}?token={token}"
    payload = {
        "query": _filter,
        "type": type,
        "size": size,
    }
    return url, payload


def build_organization_query(
    _filter: str, token: str, type: str = "query", size: int = 50
):
    _filter = "type:Organization " + _filter
    return build_knowledge_graph_query(_filter, token, type, size)

def build_article_query(_filter: str, token: str, type: str = "query", size: int = 50):
    _filter = "type:Article " + _filter
    return build_knowledge_graph_query(_filter, token, type, size)

def build_extract_article_query(_filter: str, token: str, type: str = "query"):
    raise NotImplementedError("build_extract_article_query not yet implemented.")