
# queries.py

# Zapytanie do pobrania naukowców o danym nazwisku
def get_scientists_by_last_name(last_name):
    return f"SELECT * FROM scientists WHERE last_name = '{last_name}'"

# Zapytanie do pobrania organizacji o danym typie
def get_organizations_by_type(org_type):
    return f"SELECT * FROM organizations WHERE type = '{org_type}'"

# Zapytanie do pobrania publikacji z określoną liczbą cytowań
def get_publications_by_citation_count(min_citations):
    return f"SELECT * FROM publications WHERE citations_count >= {min_citations}"
