# https://docs.diffbot.com/kgapi
KG_BASE_URL = "https://kg.diffbot.com/kg/v3/dql"
ARTICLE_BASE_URL = "https://api.diffbot.com/v3/article"
ENHANCE_BASE_URL = "https://kg.diffbot.com/kg/v3/enhance_endpoint"

def _buildKnowledgeGraphQuery(filter: str, token: str, type: str="query", size: int=50):
    url = f"{KG_BASE_URL}?type={type}&token={token}&query={filter}&size={size}"
    return url