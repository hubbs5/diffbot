# https://docs.diffbot.com/kgapi
# https://docs.diffbot.com/docs/en/dql-quickstart
KG_BASE_URL = "https://kg.diffbot.com/kg/v3/dql"
ARTICLE_BASE_URL = "https://api.diffbot.com/v3/article"
ENHANCE_BASE_URL = "https://kg.diffbot.com/kg/v3/enhance_endpoint"

def _buildKnowledgeGraphQuery(_filter: str, token: str, type: str="query", size: int=50):
    url = f"{KG_BASE_URL}?type={type}&token={token}&query={_filter}&size={size}"
    return url


def buildOrganizationQuery(_filter: str, token: str, type: str="query", size: int=50):
    _filter = "type:Organization " + _filter
    return _buildKnowledgeGraphQuery(_filter, token, type, size)


def buildArticleQuery(_filter: str, token: str, type: str="query", size: int=50):
    _filter = "type:Article " + _filter
    return _buildKnowledgeGraphQuery(_filter, token, type, size)


def buildExtractArticleQuery(_filter: str, token: str, type: str="query"):
    raise NotImplementedError("buildExtractArticleQuery not yet implemented.")