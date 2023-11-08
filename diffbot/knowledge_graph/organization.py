import numpy as np
from datetime import datetime
from warnings import warn


# Knowledge Graph Functions
def _parse_revenue(data: dict, base_currency="USD"):
    rev = data.get("revenue", None)
    if rev is None:
        return None
    revenue = rev.get("value", None)
    currency = rev.get("currency", None)

    if currency != base_currency:
        # TODO: Add conversion call
        pass

    return revenue #, currency


def _parseRevenue(data: dict, base_currency="USD"):
    warn("This function is deprecated. Use _parse_revenue instead.")
    return _parse_revenue(data, base_currency)


def _parse_logo(data: dict):
    return data.get("logo", None)


def _parseLogo(data: dict):
    warn("This function is deprecated. Use _parse_logo instead.")
    return _parse_logo(data)


def _parse_homepage_uri(data: dict):
    return data.get("homepageUri", None)

def _parseHomepageURI(data: dict):
    warn("This function is deprecated. Use _parse_homepage_uri instead.")
    return _parse_homepage_uri(data)


def _parse_num_employees(data: dict):
    return data.get("nbEmployees", None)


def _parseNumEmployees(data: dict):
    warn("This function is deprecated. Use _parse_num_employees instead.")
    return _parse_num_employees(data)


def _parse_description(data: dict):
    return data.get("description", None)


def _parseDescription(data: dict):
    warn("This function is deprecated. Use _parse_description instead.")
    return _parse_description(data)


def _parse_descriptors(data: dict):
    return data.get("description", None)


def _parseDescriptors(data: dict):
    warn("This function is deprecated. Use _parse_descriptors instead.")
    return _parse_descriptors(data)


def _parse_twitter_uri(data: dict):
    return data.get("twitterUri", None)


def _parseTwitterURI(data: dict):
    warn("This function is deprecated. Use _parse_twitter_uri instead.")
    return _parse_twitter_uri(data)


def _parse_facebook_uri(data: dict):
    return data.get("facebookUri", None)


def _parseFacebookURI(data: dict):
    warn("This function is deprecated. Use _parse_facebook_uri instead.")
    return _parse_facebook_uri(data)


def _parse_diffbot_uri(data: dict):
    uri = data.get("diffbotUri", None)
    if uri is None:
        return None, None, None
    id = uri.split("/")[-1]
    type = uri.split("/")[-2]
    return uri, id, type


def _parseDiffbotURI(data: dict):
    warn("This function is deprecated. Use _parse_diffbot_uri instead.")
    return _parse_diffbot_uri(data)


def _parse_incoming_edges(data: dict):
    return data.get("nbIncomingEdges", None)


def _parseIncomingEdges(data: dict):
    warn("This function is deprecated. Use _parse_incoming_edges instead.")
    return _parse_incoming_edges(data)


def _parse_parent_company(data: dict):
    # TODO: parse this better, still a JSON
    return data.get("parentCompany", None)


def _parseParentCompany(data: dict):
    warn("This function is deprecated. Use _parse_parent_company instead.")
    return _parse_parent_company(data)


def _parse_similarity_score(data: dict):
    return data.get("similarity_score", None)

def _parseSimilarityScore(data: dict):
    warn("This function is deprecated. Use _parse_similarity_score instead.")
    return _parse_similarity_score(data)


def _parse_importance_score(data: dict):
    return data.get("importance", None)


def _parseImportanceScore(data: dict):
    warn("This function is deprecated. Use _parse_importance_score instead.")
    return _parse_importance_score(data)


def _parse_customers(data: dict):
    # TODO: This can have multiple entries so a flat table isn't the best representation
    return data.get("customers", None)


def _parseCustomers(data: dict):
    warn("This function is deprecated. Use _parse_customers instead.")
    return _parse_customers(data)


def _parse_crawl_timestamp(data: dict, format="%Y-%m-%d %H:%M:%S"):
    timestamp = data.get("crawlTimestamp", None)
    if timestamp is None:
        return None
    return datetime.utcfromtimestamp(data["crawlTimestamp"]).strftime(format)


def _parseCrawlTimestamp(data: dict, format="%Y-%m-%d %H:%M:%S"):
    warn("This function is deprecated. Use _parse_crawl_timestamp instead.")
    return _parse_crawl_timestamp(data, format)


def _parse_is_public(data: dict) -> bool:
    return data.get("isPublic", None)


def _parse_isPublic(data: dict) -> bool:
    warn("This function is deprecated. Use _parse_is_public instead.")
    return _parse_is_public(data)


def _parse_sec_central_index_keys(data, _min=10):
    keys = {}
    ciks = data.get("secCentralIndexKeys", [])
    
    keys = {f"secCentralIndexKey{i}": k for i, k in enumerate(ciks) if i < _min}
    # Add padding, if necessary
    if len(keys) < _min:
        keys.update({f"secCentralIndexKey{i}": "" for i in range(len(keys), _min)})
    return keys


def _parse_secCentralIndexKeys(data, _min=10):
    warn("This function is deprecated. Use _parse_sec_central_index_keys instead.")
    return _parse_sec_central_index_keys(data, _min)


def _parse_locations(data: dict):
    # TODO: This can have multiple entries so a flat table isn't the best representation
    return data.get("locations", None)


def _parseLocations(data: dict):
    warn("This function is deprecated. Use _parse_locations instead.")
    return _parse_locations(data)


def _parse_categories(data: dict, target="", _min: int = 10):
    # TODO: Update based on new API behavior
    # Target values taken from Diffbot category list:
    # https://docs.diffbot.com/docs/en/kg-ont-organization#categories
    categories = data.get("categories", [])
    if len(categories) == 0:
        return {f"cat{i}": None for i in np.arange(_min)}
    
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


def _parseCategories(data: dict, target="", _min: int = 10):
    warn("This function is deprecated. Use _parse_categories instead.")
    return _parse_categories(data, target, _min)


def _parse_classification_codes(
    data: dict, class_abbrv: str, target: str = "plastic", _min: int = 3
):
    ccode = f"{class_abbrv}Code"
    cdesc = f"{class_abbrv}Desc"
    cclf = f"{class_abbrv}Classification"
    ccount = f"{class_abbrv}Count"
    keysCode = np.array([f"{ccode}{i}" for i in range(_min)])
    keysDesc = np.array([f"{cdesc}{i}" for i in range(_min)])
    clf = {}
    classes = data.get(cclf, [])
    if len(classes) == 0:
        clfCodes = {k: None for k in keysCode}
        clfDesc = {k: None for k in keysDesc}
        count = None
    else:
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


    clf.update(clfCodes)
    clf.update(clfDesc)
    clf[ccount] = count
    return clf


def _parseClassificationCodes(
        data: dict, class_abbrv: str, target: str = "plastic", _min: int = 3
):
    warn("This function is deprecated. Use _parse_classification_codes instead.")
    return _parse_classification_codes(data, class_abbrv, target, _min)


def _parse_naics_classification(
    data: dict, class_abbrv: str = "naics", target: str = "plastic", _min: int = 3
):
    return _parse_classification_codes(data, class_abbrv, target, _min)


def _parseNAICSClassification(
    data: dict, class_abbrv: str = "naics", target: str = "plastic", _min: int = 3
):
    warn("This function is deprecated. Use _parse_naics_classification instead.")
    return _parse_naics_classification(data, class_abbrv, target, _min)


def _parse_sic_classification(
    data: dict, class_abbrv: str = "sic", target: str = "plastic", _min: int = 3
):
    return _parse_classification_codes(data, class_abbrv, target, _min)


def _parseSICClassification(
    data: dict, class_abbrv: str = "sic", target: str = "plastic", _min: int = 3
):
    warn("This function is deprecated. Use _parse_sic_classification instead.")
    return _parse_sic_classification(data, class_abbrv, target, _min)


def _parse_isic_classification(
    data: dict, class_abbrv: str = "isic", target: str = "plastic", _min: int = 3
):
    return _parse_classification_codes(data, class_abbrv, target, _min)


def _parseISICClassification(
    data: dict, class_abbrv: str = "isic", target: str = "plastic", _min: int = 3
):
    warn("This function is deprecated. Use _parse_isic_classification instead.")
    return _parse_isic_classification(data, class_abbrv, target, _min)


def _parse_nace_classification(
    data: dict, class_abbrv: str = "nace", target: str = "plastic", _min: int = 3
):
    return _parse_classification_codes(data, class_abbrv, target, _min)


def _parseNACEClassification(
    data: dict, class_abbrv: str = "nace", target: str = "plastic", _min: int = 3
):
    warn("This function is deprecated. Use _parse_nace_classification instead.")
    return _parse_nace_classification(data, class_abbrv, target, _min)


def parse_organization_json(data_dict):
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
                data[name]["revenue"] = _parse_revenue(d0)
                data[name]["logo"] = _parse_logo(d0)
                data[name]["homepageURI"] = _parse_homepage_uri(d0)
                diffbot_data = _parse_diffbot_uri(d0)
                data[name]["diffbotURI"] = diffbot_data[0]
                data[name]["diffbotID"] = diffbot_data[1]
                data[name]["diffbotType"] = diffbot_data[2]
                data[name]["twitterURI"] = _parse_twitter_uri(d0)
                data[name]["facebookURI"] = _parse_facebook_uri(d0)
                data[name]["edges"] = _parse_incoming_edges(d0)
                data[name]["numEmployees"] = _parse_num_employees(d0)
                data[name]["parentCompany"] = _parse_parent_company(d0)
                data[name]["similarityScore"] = _parse_similarity_score(d0)
                data[name]["importanceScore"] = _parse_importance_score(d0)
                data[name]["customers"] = _parse_customers(d0)
                data[name]["lastUpdated"] = _parse_crawl_timestamp(d0)
                data[name]["locations"] = _parse_locations(d0)
                data[name]["description"] = _parse_description(d0)
                data[name]["descriptors"] = _parse_descriptors(d0)
                data[name]["isPublic"] = _parse_is_public(d0)
                data[name].update(_parse_sec_central_index_keys(d0))
                data[name].update(_parse_nace_classification(d0))
                data[name].update(_parse_naics_classification(d0))
                data[name].update(_parse_sic_classification(d0))
                data[name].update(_parse_isic_classification(d0))

    return data


def parseOrganization(data_dict):
    warn("This function is deprecated. Use parse_organization_json instead.")
    return parse_organization_json(data_dict)