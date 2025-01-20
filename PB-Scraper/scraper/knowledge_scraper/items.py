# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
#from scrapy.loader import ItemLoader
#from itemloaders import processors
        
class ScientistItem(Item):
    first_name = Field()
    last_name = Field()
    academic_title = Field()
    position = Field()
    email = Field()
    organizations = Field() #list of pairs (int - org importance, str - org id) university should have highest importance, department - lowest
    profile_url = Field()
    identifier  = Field() #str
    research_areas = Field() #list of str
    bibliometrics_item = Field(as_item=True)

class BibliometricsItem(Item):
    scientist_ref = Field(dont_export=True) #weak reference to ScientistItem
    h_index_wos = Field()
    h_index_scopus = Field()
    publication_count = Field()
    ministerial_score = Field()

class PublicationItem(Item):
    scientist_ids = Field() #list of str
    identifier = Field() #str
    journal_type = Field()
    publication_year = Field()
    title = Field()
    journal = Field()
    publisher = Field()
    ministerial_score = Field()

class OrganizationItem(Item):
    organization_type = Field()
    name = Field()
    identifier = Field() #str
    parent_id = Field() #str
