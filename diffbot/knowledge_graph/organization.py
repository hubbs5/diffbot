import numpy as np
from datetime import datetime


# Knowledge Graph Functions
def _parseRevenue(data: dict, base_currency="USD"):
    try:
        rev = data["revenue"]["value"]
    except KeyError:
        return None
    currency = data["revenue"]["currency"]
    if currency != base_currency:
        # TODO: Add conversion call
        pass

    return rev


def _parseLogo(data: dict):
    try:
        return data["logo"]
    except KeyError:
        return None


def _parseHomepageURI(data: dict):
    try:
        return data["homepageUri"]
    except KeyError:
        return None


def _parseNumEmployees(data: dict):
    try:
        return data["nbEmployees"]
    except KeyError:
        return None


def _parseDescription(data: dict):
    try:
        return data["description"]
    except KeyError:
        return None


def _parseDescriptors(data: dict):
    try:
        return data["description"]
    except KeyError:
        return None


def _parseTwitterURI(data: dict):
    try:
        return data["twitterUri"]
    except KeyError:
        return None


def _parseFacebookURI(data: dict):
    try:
        return data["facebookUri"]
    except KeyError:
        return None


def _parseDiffbotURI(data: dict):
    try:
        uri = data["diffbotUri"]
        id = uri.split("/")[-1]
        type = uri.split("/")[-2]
        return uri, id, type
    except KeyError:
        return None, None, None


def _parseIncomingEdges(data: dict):
    try:
        return data["nbIncomingEdges"]
    except KeyError:
        return None


def _parseParentCompany(data: dict):
    # TODO: parse this better, still a JSON
    try:
        return data["parentCompany"]
    except KeyError:
        return None


def _parseSimilarityScore(data: dict):
    try:
        return data["similarity_score"]
    except KeyError:
        return None


def _parseImportanceScore(data: dict):
    try:
        return data["importance"]
    except KeyError:
        return None


def _parseCustomers(data: dict):
    # TODO: This can have multiple entries so a flat table isn't the best representation
    try:
        return data["customers"]
    except KeyError:
        return None


def _parseCrawlTimestamp(data: dict):
    # TODO: Convert to TS
    format = "%Y-%m-%d %H:%M:%S"
    try:
        return datetime.utcfromtimestamp(data["crawlTimestamp"]).strftime(format)
    except KeyError:
        return None


def _parseLocations(data: dict):
    # TODO: This can have multiple entries so a flat table isn't the best representation
    try:
        return data["locations"]
    except KeyError:
        return None


def _parseCategories(data: dict, target="Packaging Companies", _min: int = 10):
    # Target values taken from Diffbot category list:
    # https://docs.diffbot.com/docs/en/kg-ont-organization#categories
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


def _parseClassificationCodes(
    data: dict, class_abbrv: str, target: str = "plastic", _min: int = 3
):
    ccode = f"{class_abbrv}Code"
    cdesc = f"{class_abbrv}Desc"
    cclf = f"{class_abbrv}Classification"
    ccount = f"{class_abbrv}Count"
    keysCode = np.array([f"{ccode}{i}" for i in range(_min)])
    keysDesc = np.array([f"{cdesc}{i}" for i in range(_min)])
    clf = {}
    try:
        classes = data[cclf]
        codes = np.array([i["code"] for i in classes]).astype(int)
        desc = np.array([i["name"] for i in classes])
        primaries = np.array([i["isPrimary"] for i in classes])
        targets = np.array([target in i["name"].lower() for i in classes])
        count = len(classes)
        idx = []
        if np.any(primaries):
            [idx.append(i) for i in np.where(primaries)[0]]

        if np.any(targets):
            [idx.append(i) for i, j in enumerate(targets) if j == True and i not in idx]

        if len(idx) < _min:
            _n = [None] * (_min - len(idx))
            [idx.append(_) for _ in _n]

        # Put everything into a dictionary
        clfCodes = {
            k: codes[v] if v is not None else None for k, v in zip(keysCode, idx)
        }
        clfDesc = {k: desc[v] if v is not None else None for k, v in zip(keysDesc, idx)}

    except KeyError:
        clfCodes = {k: None for k in keysCode}
        clfDesc = {k: None for k in keysDesc}
        count = None

    clf.update(clfCodes)
    clf.update(clfDesc)
    clf[ccount] = count
    return clf


def _parseNAICSClassification(
    data: dict, class_abbrv: str = "naics", target: str = "plastic", _min: int = 3
):
    return _parseClassificationCodes(data, class_abbrv, target, _min)


def _parseSICClassification(
    data: dict, class_abbrv: str = "sic", target: str = "plastic", _min: int = 3
):
    return _parseClassificationCodes(data, class_abbrv, target, _min)


def _parseISICClassification(
    data: dict, class_abbrv: str = "isic", target: str = "plastic", _min: int = 3
):
    return _parseClassificationCodes(data, class_abbrv, target, _min)


def _parseNACEClassification(
    data: dict, class_abbrv: str = "nace", target: str = "plastic", _min: int = 3
):
    return _parseClassificationCodes(data, class_abbrv, target, _min)


def parseOrganization(data_dict):
    # Parse JSON response according to values above and compute summary stats
    data = {}
    for k0, v0 in data_dict.items():
        # Parse entry
        if k0 == "data":
            for d in v0:
                d0 = d["entity"]
                name = d0["name"]
                data[name] = {}
                data[name]["score"] = d["score"]
                data[name]["revenue"] = _parseRevenue(d0)
                data[name]["logo"] = _parseLogo(d0)
                data[name]["homepageURI"] = _parseHomepageURI(d0)
                diffbot_data = _parseDiffbotURI(d0)
                data[name]["diffbotURI"] = diffbot_data[0]
                data[name]["diffbotID"] = diffbot_data[1]
                data[name]["diffbotType"] = diffbot_data[2]
                data[name]["twitterURI"] = _parseTwitterURI(d0)
                data[name]["facebookURI"] = _parseFacebookURI(d0)
                data[name]["edges"] = _parseIncomingEdges(d0)
                data[name]["numEmployees"] = _parseNumEmployees(d0)
                data[name]["parentCompany"] = _parseParentCompany(d0)
                data[name]["similarityScore"] = _parseSimilarityScore(d0)
                data[name]["importanceScore"] = _parseImportanceScore(d0)
                data[name]["customers"] = _parseCustomers(d0)
                data[name]["lastUpdated"] = _parseCrawlTimestamp(d0)
                data[name]["locations"] = _parseLocations(d0)
                data[name]["description"] = _parseDescription(d0)
                data[name]["descriptors"] = _parseDescriptors(d0)
                data[name].update(_parseNACEClassification(d0))
                data[name].update(_parseNAICSClassification(d0))
                data[name].update(_parseSICClassification(d0))
                data[name].update(_parseISICClassification(d0))

    return data
