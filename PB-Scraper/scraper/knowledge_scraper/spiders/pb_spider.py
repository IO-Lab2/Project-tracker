from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Compose, MapCompose, Join, Identity
from scrapy_playwright.page import PageMethod

from knowledge_scraper.items import ScientistItem, OrganizationItem, BibliometricsItem, PublicationItem
from constants import ACADEMIC_TITLES, FULL_ACADEMIC_TITLES
from scripts.pb.urls import change_page_number, get_id, clean_but_url
from scripts.pb.misc import await_css_loaded, get_page_count, get_stopped_scraping_item, await_css_loaded
from utils.basic_validation import is_non_empty_str, is_non_negative_int
from utils import basic_conversion
from utils.log_messages import get_item_msg
from utils.misc import add_parenthesis
from other.read_js import get_expand_organizations

import  weakref


class PbSpider(Spider):
    #spider attributes
    name = "pb"
    allowed_domains = ["bazawiedzy.pb.edu.pl"]
    custom_settings = {
        "ITEM_PIPELINES" : {
            #"knowledge_scraper.pipelines.ValidationPipeline" : 100,
            "knowledge_scraper.pipelines.DbValidationPipeline" : 100,
            "knowledge_scraper.pipelines.DbStoragePipeline" : 300,
            "knowledge_scraper.pipelines.ExportPreparationPipeline" : 900,
        },
        'AUTOTHROTTLE_ENABLED' : True,
    }

    def __init__(self, *args, **kwargs):
        super(PbSpider, self).__init__(*args, **kwargs)

        #configurable

        #whether or not to scrape organizations page
        #bool
        self.SCRAPE_ORGANIZATIONS = True

        #maximum number of items that spider can process
        #should be an integer greater than or equal to 0 
        self.MAX_SCIENTISTS_PROCESSED = 1_000_000
        self.MAX_PUBLICATIONS_PROCESSED = 1_000_000


        #constants

        #requests pointing to "main" pages
        self.ORGANIZATIONS_REQUEST = Request(
            url="https://bazawiedzy.pb.edu.pl/globalResultList.seam?r=affiliation&tab=AFFILIATION&lang=en",
            callback = self.parse_organizations,
            meta={
                "playwright":True, 
                "playwright_page_methods":[ PageMethod(await_css_loaded), PageMethod("evaluate", get_expand_organizations()) ]
            }
        )
        self.PEOPLE_REQUEST = Request(
            url="https://bazawiedzy.pb.edu.pl/globalResultList.seam?r=author&tab=PEOPLE&lang=en", 
            callback=self.pre_parse_people, 
            meta={
                "playwright":True, 
                "playwright_page_methods":[ PageMethod(await_css_loaded) ]
            }
        )
        self.PUBLICATIONS_REQUEST = Request(
            url="https://bazawiedzy.pb.edu.pl/globalResultList.seam?r=publication&tab=PUBLICATION&lang=en",
            callback=self.pre_parse_publications, 
            meta= {
                "playwright":True,
                "playwright_page_methods":[ PageMethod(await_css_loaded) ],
            }
        )
 
        #dict mapping organization types present on pb website to organization types accepted by the database
        self.PB_TO_DB_ORG_TYPES = {
            "university" : "university", 
            "faculty" : "institute",
            "institute" : "institute", 
            "department" : "department"
        }
 
        #dict mapping organization types present on pb website to their importance
        self.PB_ORG_TYPES_TO_IMPORTANCE = {
            "university" : 200, 
            "faculty" : 150,
            "institute" : 100, 
            "department" : 50
        }


        #modified at runtime

        #a generator to get main requests in order
        #should be used next(MAIN_REQUESTS_GEN)
        self.MAIN_REQUESTS_GEN = self.generate_main_requests()

        #stores organization names and their identifiers
        #this will be used to assign scientists to organizations instead of quering the database for id
        self.cathedras = dict()

        #counters for processed items
        self.scientists_processed = 0
        self.publications_processed = 0
    #end of constructor

    #a generator function that organizes "main" requests
    #when requests run out will yield None indefinitely
    def generate_main_requests(self):
        order = [self.ORGANIZATIONS_REQUEST, self.PEOPLE_REQUEST, self.PUBLICATIONS_REQUEST]

        #organizations page
        if self.SCRAPE_ORGANIZATIONS:
            self.logger.info("generate_main_requests: yielding ORGANIZATIONS_REQUEST")
            yield self.ORGANIZATIONS_REQUEST
        else:
            self.logger.info(f"generate_main_requests: skipping ORGANIZATIONS_REQUEST. SCRAPE_ORGANIZATIONS set to {self.SCRAPE_ORGANIZATIONS}")

        #people page
        if not self.MAX_SCIENTISTS_PROCESSED == 0:
            self.logger.info("generate_main_requests: yielding PEOPLE_REQUEST")
            yield self.PEOPLE_REQUEST
        else:
            self.logger.info(f"generate_main_requests: skipping PEOPLE_REQUEST. MAX_SCIENTISTS_PROCESSED set to {self.MAX_SCIENTISTS_PROCESSED}")

        #publications page
        if not self.MAX_PUBLICATIONS_PROCESSED == 0:
            self.logger.info("generate_main_requests: yielding PUBLICATIONS_REQUEST")
            yield self.PUBLICATIONS_REQUEST
        else:
            self.logger.info(f"generate_main_requests: skipping PUBLICATIONS_REQUEST. MAX_PUBLICATIONS_PROCESSED set to {self.MAX_PUBLICATIONS_PROCESSED}")

        while True:
            self.logger.info(f"generate_main_requests: there are no main requests left to yield")
            yield None
    #end of method

    #deducts organization_type using its name
    #return org type as str or None
    def get_pb_organization_type(self, name:str|None):
        if not is_non_empty_str(name):
            return None

        banned_words = ["library", "archive", "laboratory"]
        for banned_word in banned_words: 
            if banned_word in name.lower(): 
                return None

        #iterating over pb organization types
        for keyword in self.PB_TO_DB_ORG_TYPES.keys():
            if keyword in name.lower():
                return keyword

        return None


    #needs to return something so if MAIN_REQUESTS_GEN returns None will load landing page
    def start_requests(self):
        rq = next(self.MAIN_REQUESTS_GEN)
        if rq is not None:
            yield rq
        else:
            yield Request(url="https://bazawiedzy.pb.edu.pl/index.seam")
    #end of start_requests

    #empty default
    def parse(self, response):
        return

    #parses organizations page
    async def parse_organizations(self, response):
        #use similar to anchor.css( css_path )
        #parent is the id of a parent organization
        #for parsing li elements with organizations inside an aria tree on the organizations page
        def parse_li_node(anchor, css_path, parent=None) -> OrganizationItem:
            organization = OrganizationItem( parent_id = parent )

            #scraping organization name
            name = anchor.css( css_path + " > div span.affiliationName::text").get()
            organization["name"] = name

            #deducing organization_type
            pb_org_type = self.get_pb_organization_type(name)
            organization["organization_type"] = self.PB_TO_DB_ORG_TYPES.get( pb_org_type )

            #generating organization id based on its url
            organization_url = anchor.css( css_path + " > div a.normal-link::attr(href)").get()
            if organization_url:
                organization["identifier"] = get_id(organization_url)
            
            #not adding an organization or its children if it isn't valid
            if not is_organization_valid( organization ):
                return

            yield organization
 
            css_path += " > ul > li"
            children_nodes = anchor.css( css_path )
            for i in range(len(children_nodes)):
                yield from parse_li_node( anchor, css_path+f":nth-child({i+1})", organization["identifier"] )
        
        #approximates the validity of an OrganizationItem
        def is_organization_valid(org:OrganizationItem) -> bool:
            if not org.get("identifier"):
                self.logger.warning( get_stopped_scraping_item(org, "no id was generated - probably url was not found"))
                return False

            if not org.get("name"):
                self.logger.warning(get_stopped_scraping_item(org, "no organization name found"))
                return False

            if not org.get("organization_type"):
                self.logger.info( get_stopped_scraping_item(org, "no valid organization_type found") )
                return False

            #checking parent_id
            parent_id = org.get("parent_id")
            is_university = org["organization_type"] == 'university'
            if is_university and parent_id is not None:
                self.logger.warning(get_stopped_scraping_item(org, "organization is a university and parent_id is not None"))
                return False
            elif not is_university and not parent_id:
                self.logger.warning(get_stopped_scraping_item(org, "no parent_id found and organization is not a university"))
                return False

            return True


        for organization in parse_li_node( response, "li#ttree\\:0"):
            #assuming that all departments have unique names which they should have
            self.cathedras[organization["name"]] = organization["identifier"]
            yield organization
        
        #go to next page
        yield next(self.MAIN_REQUESTS_GEN)

    #for starting to parse people pages
    async def pre_parse_people(self, response):
        self.logger.debug("started pre_parse_people")

        page_count = get_page_count(response)
        if page_count is None:
            self.logger.critical("parse_people: total number of people pages could not be determined - set to 1")
            page_count = 1
        #end of if

        async for r in self.parse_people(response, 1, page_count):
            yield r

    #for actually parsing people pages
    async def parse_people(self, response, page_num, page_count):
        self.logger.debug("parse_people started")
        self.logger.info((f"loaded people page {page_num} from {page_count} -> url: {add_parenthesis(response.url)}"))
                

        for author in response.css("div.authorGlobalSearchTemplateDescriptionPanel"):
            self.logger.debug("started parse_people")

            #restraining processed scientists
            self.scientists_processed += 1
            if not self.scientists_processed <= self.MAX_SCIENTISTS_PROCESSED:
                self.logger.info(f"Reached upper limit for scientists to process - {self.MAX_SCIENTISTS_PROCESSED}  - stopping parse_people")
                yield next(self.MAIN_REQUESTS_GEN)
                return

            sc = ScientistItem()

            #url first because it helps to identify issues
            #scraping profile_url
            relative_profile_url = author.css("a.authorNameLink::attr(href)").get()
            if not relative_profile_url:
                self.logger.warning(get_stopped_scraping_item(sc, 'no profile_url found', response_url=response.url))
                continue #url and identifier are crucial
            profile_url = response.urljoin( relative_profile_url )
            profile_url = clean_but_url( profile_url )
            sc["profile_url"] =  profile_url

            #generating identifier based on profile_url
            identifier = get_id(profile_url)
            #maybe it never happens?
            if not identifier: 
                self.logger.warning(get_stopped_scraping_item(sc, 'no id could be generated'))
                continue #identifier is crucial
            sc["identifier"] = identifier

            #scraping names
            names = author.css("span.authorName::text").getall()
            if not len(names) >= 3:
                self.logger.warning( get_stopped_scraping_item(sc, 'no first_name, last_name or academic_title found'))
                continue #names and academic_title are crucial
            sc["first_name"] = names[0].strip()
            sc["last_name"] = names[1]

            #returns the first matching academic title from ACADEMIC_TITLES or FULL_ACADEMIC_TITLES found in the titles string
            #returns None if it doesn't find a match
            def get_academic_title(titles: str) -> str:
                #not case sensitive
                for short, full in zip(ACADEMIC_TITLES, FULL_ACADEMIC_TITLES):
                    titles = titles.lower()
                    if short.lower() in titles or full.lower() in titles:
                        return short
                return None
                
            #scraping academic_title
            title = get_academic_title(names[2])
            if not title:
                self.logger.info( get_stopped_scraping_item(sc, 'no valid academic_title found') )
                continue #academic_title is crucial
            sc["academic_title"] =  title

            #scraping position
            sc["position"] = author.css("p.possitionInfo > span.authorAffil::text").get()

            #goto a scientist's profile page
            yield response.follow(
                url=sc["profile_url"], 
                callback=self.parse_author, 
                cb_kwargs={"scientist_item":sc},
                meta= {
                    "playwright":True,
                    "playwright_page_methods":[ PageMethod(await_css_loaded) ],
                }
            )


        #move to the next page
        next_page_num = page_num + 1
        if next_page_num > page_count:
            self.logger.info("parsed all people pages")
            yield next(self.MAIN_REQUESTS_GEN)
            return

        request = change_page_number(self.PEOPLE_REQUEST, next_page_num)
        request = request.replace(
            callback = self.parse_people,
            cb_kwargs = {"page_num": next_page_num, "page_count": page_count}
        )
        yield request
    #end of parse_people

    #parses scientist's profile page
    async def parse_author(self, response, scientist_item):
        self.logger.debug("started parse_author")

        container = response.css("div#authorProfileBasicInfoPanel") #container with organizations and email
        if container:
            #scraping scientist's organization
            org_contaniners = container.css('a:not(.iconLink)')
            orgs = []
            for a in org_contaniners:
                name = a.css("span::text").get()
                org_type = self.get_pb_organization_type( name )
                if not org_type or org_type not in self.PB_ORG_TYPES_TO_IMPORTANCE:
                    continue
                org_importance = self.PB_ORG_TYPES_TO_IMPORTANCE[org_type]
                org_id = get_id( a.css("::attr(href)").get() )

                if not org_type or not org_id:
                    continue

                orgs.append( (org_importance, org_id) )
            #end of for
            scientist_item["organizations"] = orgs
                
            #scraping email
            scientist_item["email"] = container.css("p.authorContactInfoEmailContainer > a::text").get()

        #scraping research areas
        # stop scraping if null
        research_areas = response.css("span.authorSimple::text").getall() #science discipline only
        if not research_areas:
            self.logger.warning( get_stopped_scraping_item(scientist_item, "no research_areas found") )
            return #research_areas are crucial
        scientist_item["research_areas"] = response.css("span.authorSimple::text").getall() #science discipline only


        #scraping bibliometrics
        bibl = ItemLoader(item=BibliometricsItem(), response=response)
        bibl.default_output_processor = TakeFirst()

        bibl.add_value("scientist_ref", weakref.ref(scientist_item))

        #scraping publication_count 
        container = response.css("div.achievementsTable > ul") #contains "Achievement summary" table
        path = "li:nth-child(1)" #path from container to li with publication_count
        if not container or not container.css(path + " > span::text").get() == "Publications":
            self.logger.warning( get_stopped_scraping_item(bibl.load_item(), "no publication_count found") )
            return #publication_count is crucial


        publi_count_text = container.css(path + " a::text").get()
        publi_count = basic_conversion.try_make_int(publi_count_text)
        if publi_count is None:
            self.logger.warning( get_stopped_scraping_item(bibl.load_item(), 'no publication_count found') )
            return #publication_count is crucial
        bibl.add_value("publication_count", publi_count)

        bibliometry_container  = response.css("ul.bibliometric-data-list") #contains "Bibliometry*"
        if not bibliometry_container:
            self.logger.warning( get_stopped_scraping_item(bibl.load_item(), 'no "Bibliometry*" table found -> no ministerial_score found') )
            return #ministerial_score is crucial

        #scraping ministerial_score
        mini_score_text = bibliometry_container.css('div.hIndexItem::text').getall()
        if not mini_score_text:
            self.logger.warning( get_stopped_scraping_item(bibl.load_item(), 'no ministerial_score found') )
            return #ministerial_score is crucial

        mini_score_text = "".join(mini_score_text) #probably use processors.Concatenate
        mini_score = basic_conversion.try_make_float(mini_score_text)
        if mini_score is None:
            self.logger.warning( get_stopped_scraping_item(bibl.load_item(), "invalid ministerial score found") )
            return #ministerial_score is crucial
        bibl.add_value("ministerial_score", mini_score)
  

        #will only work if both appear; '-' supported
        #scraping h_index_wos and h_index_scopus
        h_indices = bibliometry_container.css("a.indicatorValue::text").getall()
        if len(h_indices) == 2:
            #None / null for this field is accepted in the database
            bibl.add_value("h_index_scopus", basic_conversion.try_make_int(h_indices[0]))
            bibl.add_value("h_index_wos", basic_conversion.try_make_int(h_indices[1]))

        scientist_item["bibliometrics_item"] = bibl.load_item()
        yield scientist_item
        #yield bibl.load_item()
    #end of parse_author


    #for scraping author-publications page
    async def pre_parse_publications(self, response):
        self.logger.debug("started pre_parse_publications")
        page_count = get_page_count(response)
        if page_count is None:
            self.logger.critical("pre_parse_publications: the total publications page count could not be determined - set to 1")
            page_count = 1
        #end of if

        async for r in self.parse_publications(response, 1, page_count):
            yield r
    #end of pre_parse_publications
        
        
    #for actual of scraping author-publications page
    async def parse_publications(self, response, page_num, page_count):
        self.logger.debug("started parse_publications")
        self.logger.info((f"loaded publication page {page_num} from {page_count} -> url: {add_parenthesis(response.url)}"))

        r'''
        website looks like this:
        <h5></h5>
        <h6></h6>
        <ul></ul>
        <h5></h5>
        <h6></h6>
        <ul></ul>
        <h6></h6>
        <ul></ul>
        ...

        all elements have interesting information
        so we're looking for a pattern: h5, h6, ul, where h6, ul can appear multiple times after a single h5
        '''

        ordered_elements = response.xpath('//div[@id="entitiesT_content"]/h5 | //div[@id="entitiesT_content"]/h6 | //div[@id="entitiesT_content"]/ul')

        i = 0
        while i < len(ordered_elements )-2: #pattern has at least 3 elements
            if not ordered_elements[i].root.tag == "h5":
                i += 1
                continue
            #we have: h5

            #extracting publication_year
            year_text = ordered_elements[i].xpath('text()').get()
            year = basic_conversion.try_make_int(year_text) #can be None

            while i+2< len(ordered_elements):

                if not ordered_elements[i+1].root.tag == "h6":
                    break
                #we have i+1:h6
                if not ordered_elements[i+2].root.tag == "ul":
                    i += 1
                    break

                #we have a pattern where i+1:h6, i+2:ul
                h6 = ordered_elements[i+1]
                ul = ordered_elements[i+2]

                i += 2 #so that we don't repeat ourselves

                #extracting journal_type from h6
                j_type = h6.xpath('text()').get() #can be None

                for h7 in ul.css("h7"): #h7 elements contain name and publication url
                    #everything inside should be a function that raises StopProcessingItem exception if sth goes wrong
                    r'''
                    ul elements have cells structured:
                    <h7>
                        <a class="infoLink" href="publication_url">
                            <span>
                                <span> name </span>
                            </span>
                        </a>
                    </h7>
                    '''
                        
                    #Checking if MAX_PUBLICATIONS_PROCESSED has been exceeded
                    self.publications_processed += 1
                    if not self.publications_processed <= self.MAX_PUBLICATIONS_PROCESSED:
                        self.logger.info(f"Reached upper limit for publications to process - {self.MAX_PUBLICATIONS_PROCESSED}  - stopping parse_publications")
                        return #nothing to scrape after publications

                    a = h7.css("a") #there is only one
                    if not a:
                        self.logger.warning( get_stopped_scraping_item(PublicationItem(), 'name and url could not be found', response_url=response.url) )
                        #no a element -> no name - name is crucial
                        #             -> no url -> no identifier - identifier is crucial
                        continue 

                    publi_url = a.css("::attr(href)").get()
                    if not publi_url:
                        self.logger.warning( get_stopped_scraping_item(PublicationItem(), 'url could not be found', response_url=response.url) )
                        continue #no url -> no identifier - identifier is crucial

                    #generating id based on url
                    identifier = get_id(publi_url)
                    #maybe never happens?
                    if not identifier:
                        self.logger.warning( get_stopped_scraping_item(PublicationItem(), 'identifier could not be generated', response_url=response.url) )
                        continue #identifier is crucial

                    #extracting title
                    title = h7.css("a > span > span::text").get()
                    if not title:
                        self.logger.warning( get_stopped_scraping_item(PublicationItem(identifier=identifier), 'title could not be found', publication_url=publi_url) )
                        continue #title is crucial

                    #putting all the extracted fields together
                    publication = PublicationItem( publication_year=year, journal_type=j_type, identifier=identifier, title=title )

                    yield response.follow(
                        url=publi_url,
                        callback=self.parse_publication,
                        cb_kwargs={"publication_item": publication},
                    )
            #end of while
            i += 1
        #end of while

        #go to next page
        next_page_num = page_num + 1
        if next_page_num > page_count:
            self.logger.info("parsed all publications pages")
            return

        request = change_page_number(self.PUBLICATIONS_REQUEST, next_page_num) #changing url
        request = request.replace(
            callback=self.parse_publications,
            cb_kwargs={ "page_num": next_page_num, "page_count" : page_count}
        )
        yield request
    #end of parse_publications

    #for scraping a scpecific publication page
    def parse_publication(self, response, publication_item):
        self.logger.debug("started parse_publication")
        publi = ItemLoader(item=publication_item, response=response)
        publi.default_output_processor = TakeFirst()

        publi.scientist_ids_out = Identity()
        publi.scientist_ids_in = MapCompose( get_id )
        publi.ministerial_score_in = MapCompose(basic_conversion.try_make_int)
        publi.journal_in = MapCompose(lambda s: s.split(', ISSN')) #will return full string if ', ISSN' won't be present; relies on TakeFirst

        #scraping scientist_ids
        publi.add_css("scientist_ids", "div.authorListElement > a::attr(href)")
        sc_ids = publi.get_output_value("scientist_ids")
        if not sc_ids or not any(sc is not None for sc in sc_ids):
            self.logger.warning( get_stopped_scraping_item(publi.load_item(), "no valid scientists id found", response_url=response.url) )
            return
            

        r'''
        <dl>
            <dt>
                <span> label </span>
            <\dt>
            <dd>
                information organized in various ways
            <\dd>
        <\dl>
        
        pattern: dt with span, dd
        '''

        # checks if label contains key phrases
        # returns a field corresponding to a label
        # returns None if no fields match that label
        # is it possible for it to skip publisher if more than one label finds a match?
        def get_field(label:str):
            key_phrases_to_fields = { 
                "Journal" : "journal",
                "Score (nominal)" : "ministerial_score",
                "Publisher" : "publisher"
            } #case sensitive

            for key_phrase in key_phrases_to_fields.keys():
                if key_phrase in label:
                    return key_phrases_to_fields[key_phrase]

            return None


        dl_elements = response.xpath('//dl[@class="table2ColsContainer"]/*')  # Select all children of dl, there is only one dl like that

        i = 0
        while i < len(dl_elements)-1: #pattern has 2 elements
            if dl_elements[i].root.tag != 'dt':
                i += 1
                continue

            label = dl_elements[i].css('span::text').get()
            if not label:
                i+=1
                continue

            field = get_field( label )
            if not field:
                i += 1
                continue
        
            #moving to the next element
            #highest possible i before this point is len(dl_elements)-2
            i += 1

            if not dl_elements[i].root.tag == 'dd':
                i += 1
                continue

            values = dl_elements[i].css('*::text').getall()
            publi.add_value( field, values, Join(""), Compose(str.strip) )
            i += 1
        #end of while

        yield publi.load_item()
