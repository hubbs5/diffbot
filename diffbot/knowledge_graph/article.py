import re
import numpy as np
from datetime import datetime

def buildArticleQuery():
    pass

def _parseTitle(data: dict):
    try:
        return data['title']
    except KeyError:
        return None

def _parseDate(data: dict):
    format = "%Y-%m-%d %H:%M:%S"
    try:
        date = data['estimatedDate']['timestamp'] / 1000
        return datetime.utcfromtimestamp(date).strftime(format)
    except KeyError:
        return None

def _parseAuthor(data: dict):
    try:
        return data['author']
    except KeyError:
        return None

def _parseSiteName(data: dict):
    try:
        return data['siteName']
    except KeyError:
        return None

def _parseLanguage(data: dict):
    try:
        return data['language']
    except KeyError:
        return None

def _parseSentiment(data: dict):
    try:
        return data['sentiment']
    except KeyError:
        return None

def _parseType(data: dict):
    try:
        return data['type']
    except KeyError:
        return None

def _parseHTML(data: dict):
    # TODO: this one is a bit of a misnomer because it returns all the html.
    try:
        return data['html']
    except KeyError:
        return None

def _parseText(data: dict):
    try:
        return data['text']
    except KeyError:
        return None

def _parseURL(data: dict):
    try:
        return data['pageUrl']
    except KeyError:
        return None

def _parseCategories(data: dict, 
    target='Acquisitions, Mergers and Takeovers', _min: int=10):
    # Target values taken from Diffbot category list: 
    # https://docs.diffbot.com/docs/en/kg-article-categories-list#docsNav
    try:
        categories = data['categories']
        names = np.array([v['name'] for v in categories])
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
        return {f"cat{i}": names[j] if j is not None else None 
                for i, j in enumerate(idx)}
    except KeyError:
        return {f"cat{i}": None for i in np.arange(_min)}

def _parseTags(article, _min: int=10):
    tag_dict = {}
    try:
        tags = article['tags']
        tag_labels = {f"tagLabel{i}": j['label'] 
                      for i, j in enumerate(tags) if i < _min}
        tag_labels = _padTags(tag_labels, _min)
        
        tag_scores = {f"tagScore{i}": j['score'] 
                      for i, j in enumerate(tags) if i < _min}
        tag_scores = _padTags(tag_scores, _min)
        
        tag_sentiment = {f"tagSentiment{i}": j['sentiment'] 
                        for i, j in enumerate(tags) if i < _min}
        tag_sentiment = _padTags(tag_sentiment, _min)
        
        tag_type = {f"tagType{i}": j['types'][0].split('/')[-1]
                    for i, j in enumerate(tags) if i < _min}
        tag_type = _padTags(tag_type, _min)
        
        tag_uri = {f"tagURI{i}": j['uri'] 
                for i, j in enumerate(tags) if i < _min}
        tag_uri = _padTags(tag_uri, _min)
        
        tag_count = {'tag_count': len(tags)}
    except KeyError:
        tag_labels = {f'tagLabel{i}': None for i in range(_min)}
        tag_scores = tag_labels
        tag_sentiment = tag_labels
        tag_type = tag_labels
        tag_uri = tag_labels
        tag_count = {'tag_count': 0}
        
    tag_dict.update(tag_labels)
    tag_dict.update(tag_scores)
    tag_dict.update(tag_sentiment)
    tag_dict.update(tag_type)
    tag_dict.update(tag_uri)
    tag_dict.update(tag_count)
    
    return tag_dict

def _padTags(tag_dict, N):
    # Adds None entries if not enough entries
    n = len(tag_dict)
    k = list(tag_dict.keys())[0][:-1]
    if n < N:
        _ = [tag_dict.update({f'{k}{n+i}': None}) for i in range(N-n)]
        
    return tag_dict

def parseArticle(article):
    data = {}
    data['title'] = _parseTitle(article)
    data['date'] = _parseDate(article)
    data['author'] = _parseAuthor(article)
    data['siteName'] = _parseSiteName(article)
    data['language'] = _parseLanguage(article)
    data['sentiment'] = _parseSentiment(article)
    data['type'] = _parseType(article)
    data['html'] = _parseHTML(article)
    data['text'] = _parseText(article)
    data['url'] = _parseURL(article)
    data.update(_parseTags(article))
    # data.update(_parseCategories(article))

    return data