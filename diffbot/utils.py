import urllib.parse
import warnings

# https://docs.diffbot.com/kgapi
# https://docs.diffbot.com/docs/en/dql-quickstart
KG_BASE_URL = "https://kg.diffbot.com/kg/v3/dql"
ARTICLE_BASE_URL = "https://api.diffbot.com/v3/article"
ENHANCE_BASE_URL = "https://kg.diffbot.com/kg/v3/enhance_endpoint"

def _buildKnowledgeGraphQuery(_filter: str, token: str, type: str="query", size: int=50):
    warnings.warn("This function is deprecated. Use build_knowledge_graph_query instead.")
    url = build_knowledge_graph_query(_filter, token, type, size)
    return url

def build_knowledge_graph_query(_filter: str, token: str, type: str="query", size: int=50):
    _url = urllib.parse.quote(f"?type={type}&token={token}&query={_filter}&size={size}")
    url = f"{KG_BASE_URL}{_url}"
    return url

def build_knowledge_graph_post_query(_filter: str, token: str, type: str="query", size: int=50):
    url = f"{KG_BASE_URL}?token={token}"
    payload = {
        "query": _filter,
        "type": type,
        "size": size,
    }
    return url, payload

def buildOrganizationQuery(_filter: str, token: str, type: str="query", size: int=50):
    _filter = "type:Organization " + _filter
    return build_knowledge_graph_query(_filter, token, type, size)


def buildArticleQuery(_filter: str, token: str, type: str="query", size: int=50):
    _filter = "type:Article " + _filter
    return build_knowledge_graph_query(_filter, token, type, size)


def buildExtractArticleQuery(_filter: str, token: str, type: str="query"):
    raise NotImplementedError("buildExtractArticleQuery not yet implemented.")