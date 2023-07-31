from nntplib import ArticleInfo
import re
import numpy as np
from datetime import datetime


def build_article_query():
    raise NotImplementedError("build_article_query is not yet implemented.")


def _parse_title(data: dict):
    try:
        return data["title"]
    except KeyError:
        return None


def _parse_date(data: dict):
    # format = "%Y-%m-%d %H:%M:%S"
    format = "%Y-%m-%d"
    try:
        date = data["estimatedDate"]["timestamp"] / 1000
        return datetime.utcfromtimestamp(date).strftime(format)
    except KeyError:
        return None


def _parse_author(data: dict):
    try:
        return data["author"]
    except KeyError:
        return None


def _parse_site_name(data: dict):
    try:
        return data["siteName"]
    except KeyError:
        return None


def _parse_language(data: dict):
    try:
        return data["language"]
    except KeyError:
        return None


def _parse_sentiment(data: dict):
    try:
        return data["sentiment"]
    except KeyError:
        return None


def _parse_type(data: dict):
    try:
        return data["type"]
    except KeyError:
        return None


def _parse_html(data: dict):
    # TODO: this one is a bit of a misnomer because it returns all the html.
    try:
        return data["html"]
    except KeyError:
        return None


def _parse_text(data: dict):
    try:
        return data["text"]
    except KeyError:
        return None


def _parse_url(data: dict):
    try:
        return data["pageUrl"]
    except KeyError:
        return None


def _parse_categories(
    data: dict, target="Acquisitions, Mergers and Takeovers", _min: int = 10
):
    # Target values taken from Diffbot category list:
    # https://docs.diffbot.com/docs/en/kg-article-categories-list#docsNav
    try:
        categories = data["categories"]
        names = np.array([v["name"] for v in categories])
        targets = [target in i for i in names]
        idx = []
        if np.any(targets):
            [idx.append(i) for i in np.where(targets)[0]]

        # Add names if not in index
        cat_idx = [i for i, j in enumerate(names) if i not in idx]
        idx = np.hstack([idx, cat_idx])
        if len(idx) < _min:
            _n = np.array([None] * (_min - len(idx)))
            idx = np.hstack([idx, _n])
        return {
            f"cat{i}": names[j] if j is not None else None for i, j in enumerate(idx)
        }
    except KeyError:
        return {f"cat{i}": None for i in np.arange(_min)}


def _parse_tags(article, _min: int = 10):
    tag_dict = {}
    try:
        tags = article["tags"]
        tag_labels = {
            f"tagLabel{i}": j["label"] for i, j in enumerate(tags) if i < _min
        }
        tag_labels = _parse_tads(tag_labels, _min)
    except:
        tag_labels = {f"tagLabel{i}": None for i in range(_min)}

    try:
        tag_scores = {
            f"tagScore{i}": j["score"] for i, j in enumerate(tags) if i < _min
        }
        tag_scores = _parse_tads(tag_scores, _min)
    except:
        tag_scores = {f"tagScore{i}": None for i in range(_min)}

    try:
        tag_sentiment = {
            f"tagSentiment{i}": j["sentiment"] for i, j in enumerate(tags) if i < _min
        }
        tag_sentiment = _parse_tads(tag_sentiment, _min)
    except:
        tag_sentiment = {f"tagSentiment{i}": None for i in range(_min)}

    try:
        tag_type = {
            f"tagType{i}": j["types"] if "types" in j.keys() and i < _min else None
            for i, j in enumerate(tags)
        }
        tag_type = _parse_tads(tag_type, _min)
    except:
        tag_type = {f"tagType{i}": None for i in range(_min)}

    try:
        tag_uri = {f"tagURI{i}": j["uri"] for i, j in enumerate(tags) if i < _min}
        tag_uri = _parse_tads(tag_uri, _min)
    except:
        tag_uri = {f"tagURI{i}": None for i in range(_min)}

    try:
        tag_count = {"tag_count": len(tags)}
    except:
        tag_count = {"tag_count": 0}

    tag_dict.update(tag_labels)
    tag_dict.update(tag_scores)
    tag_dict.update(tag_sentiment)
    tag_dict.update(tag_type)
    tag_dict.update(tag_uri)
    tag_dict.update(tag_count)

    return tag_dict


def _parse_tads(tag_dict, N):
    # Adds None entries if not enough entries
    n = len(tag_dict)
    k = list(tag_dict.keys())[0][:-1]  # WTF
    if n < N:
        _ = [tag_dict.update({f"{k}{n+i}": None}) for i in range(N - n)]

    return tag_dict


def parse_article(article):
    data = {}
    data["title"] = _parse_title(article)
    data["date"] = _parse_date(article)
    data["author"] = _parse_author(article)
    data["siteName"] = _parse_site_name(article)
    data["language"] = _parse_language(article)
    data["sentiment"] = _parse_sentiment(article)
    data["type"] = _parse_type(article)
    data["html"] = _parse_html(article)
    data["text"] = _parse_text(article)
    data["url"] = _parse_url(article)
    data.update(_parse_tags(article))
    # data.update(_parse_categories(article))

    return data


def parse_articles(data_dict: dict) -> dict:
    data = {}
    for k0, v0 in data_dict.items():
        if k0 == "data":
            for d in v0:
                article = d["entity"]
                id = article["id"]
                data[id] = parse_article(article)

    return data