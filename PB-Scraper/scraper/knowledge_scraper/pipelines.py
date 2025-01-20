# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from knowledge_scraper.items import ScientistItem, OrganizationItem, BibliometricsItem, PublicationItem
from scripts.database.database import make_connection
from scripts.database.data_query import does_row_exist, select_match
from scripts.database.data_manipulation import insert_or_update_with_id, insert_or_update_matched
from utils import basic_validation
from utils.misc import process_based_on_type, HandlerNotFoundError, filter_values, add_parenthesis
from utils.log_messages import get_item_msg, get_invalid_value_msg

from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter

from logging import getLogger
from datetime import date

logger = getLogger(__name__)

class ValidationPipeline:
    def process_item(self, item, spider):
        # it's very important that DropItem isn't handled
        try:
            process_based_on_type(item, 
                {
                    ScientistItem : self.validate_scientist,
                    #BibliometricsItem : self.validate_bibliometrics,
                    PublicationItem : self.validate_publication,
                    OrganizationItem : self.validate_organization,
                })
        except HandlerNotFoundError as e:
            raise DropItem(f"Item of unrecognized type {type(item)} wasn't validated: {e}")

        return item


    def validate_and_null(self, item, key, *validation_funcs, process_independently=False):
        '''
        extends basic_validation.validate_obj

        validate the value of a specified key in an item and replace it with None if any validation fails

        if key is not in item, item[key] will be set to None
        if process_independently == True, will replace item[key] with a list containing only values which passed validation

        item: item whoose value you want to check
        key: key to acces the value you want to validate, 
        '''
        if not key in item:
            logger.debug( get_item_msg("Validation: set field to null", item, f"validate_and_null: provided key {add_parenthesis(key)} is not in item", add_identifier=True) )
            item[key] = None
            return

        value = item[key]
        if value is None:
            logger.debug( get_item_msg("Validation: set field to null", item, f"validate_and_null: value corresponding to key {add_parenthesis(key)} is None. Nothing to do", add_identifier=True) )
            return

        is_valid = basic_validation.validate_obj(value, *validation_funcs, process_independently=process_independently)

        if process_independently:
            #value and is_valid are iterables

            if len(value) == 0:
                logger.debug( get_item_msg("Validation: set field to empty list", item, f"{key} has no elements", add_identifier=True) )
                item[key] = []
                return

            valid_values, invalid_values = filter_values(value, is_valid, include_removed=True)
            item[key] = valid_values

            #logging
            if invalid_values:
                invalid_values_text = ", ".join( [str( add_parenthesis(v) ) for v in invalid_values] )
                logger.info( get_item_msg("Validation: removed invalid values from field", item, f"validate_and_null: {key}: {invalid_values_text}", add_identifier=True) )

            return
            
        if not is_valid:
            logger.info( get_item_msg("Validation: set field to null", item, "validate_and_null: " + get_invalid_value_msg(item, key), add_identifier=True) )
            item[key] = None
    #end of validate_and_null


    def validate_and_drop(self, item, key, *validation_funcs, process_independently=False):
        '''
        extends basic_validation.validate_obj

        validate the value of a specified key in an item and raise DropItem if any validation fails
        if process_independently, removes invalid values - if there are no valid values, drops item

        item: item whoose value you want to check
        key: key to acces the value you want to validate
        '''
        if key not in item:
            raise DropItem( get_item_msg("Validation: dropped item", item, f"validate_and_drop: key {key} not in item") )
            
        value = item[key]
        is_valid = basic_validation.validate_obj(value, *validation_funcs, process_independently=process_independently)
        if process_independently:
            #value and is_valid are iterables
            valid_values, invalid_values = filter_values(value, is_valid, include_removed=True)

            #logging
            if invalid_values:
                invalid_values_text = ", ".join( [str( add_parenthesis(v) ) for v in invalid_values] )
                logger.info( get_item_msg("Validation: removed invalid values from field", item, f"validate_and_dropped: {key}: {invalid_values_text}", add_identifier=True) )

            if not valid_values:
                #an empty list is not a valid value
                raise DropItem( get_item_msg("Validation: dropped item", item, f"validate_and_drop: key {key} has no valid values assigned to it") )

            item[key] = valid_values
            return

        if not is_valid:
            raise DropItem( get_item_msg("Validation: dropped item", item, f"validate_and_drop: {get_invalid_value_msg(item, key)}") )
    #end of validate_and_drop


    #only to be used with ScientistItem
    def validate_scientist(self, sc):
        #NOT NULL
        self.validate_and_drop(sc, "identifier", basic_validation.validate_uuid_str)
        self.validate_and_drop(sc, "first_name", basic_validation.validate_name, (basic_validation.length_check, 100))
        self.validate_and_drop(sc, "last_name", basic_validation.validate_name, (basic_validation.length_check, 100))
        #longest academic_title is "prof."
        self.validate_and_drop(sc, "academic_title", basic_validation.validate_academic_title)

        #drop if invalid, maybe check against a list of valid ones
        self.validate_and_drop(sc, "research_areas", basic_validation.is_non_empty_str, (basic_validation.length_check, 255), process_independently=True)

        #NULLABLE
        self.validate_and_null(sc, "position", basic_validation.is_non_empty_str, (basic_validation.length_check, 255))
        self.validate_and_null(sc, "email", basic_validation.validate_email, (basic_validation.length_check, 255))
        self.validate_and_null(sc, "profile_url", basic_validation.validate_url)

        #NOT IN TABLE
        def validate_org_type_id_pair(pair):
            #is pair
            if not ( isinstance(pair, tuple) and len(pair) == 2 ):
                return False

            #is content valid
            if not isinstance(pair[0], int):
                return False
            if not basic_validation.validate_uuid_str(pair[1]):
                return False
            
            return True
        #end of validate_org_type_id_pair
        self.validate_and_drop(sc, "organizations",  validate_org_type_id_pair, process_independently=True) #- check if it exists in database

        #validating bibliometrics
        self.validate_and_drop(sc, "bibliometrics_item", (isinstance, BibliometricsItem))
        self.validate_bibliometrics( sc["bibliometrics_item"] )


    #only to be used with BibliometricsItem
    def validate_bibliometrics(self, bibl):
        #NOT NULL
        self.validate_and_drop(bibl, "publication_count", basic_validation.is_non_negative_int)
        self.validate_and_drop(bibl, "ministerial_score", basic_validation.is_non_negative_float)
        self.validate_and_drop(bibl, "scientist_ref", basic_validation.validate_weak_ref)

        #NULLABLE
        self.validate_and_null(bibl, "h_index_wos", basic_validation.is_non_negative_int)
        self.validate_and_null(bibl, "h_index_scopus", basic_validation.is_non_negative_int)


    #only to be used with PublicationItem
    def validate_publication(self, publ):
        #NOT NULL
        self.validate_and_drop(publ, "identifier", basic_validation.validate_uuid_str)
        self.validate_and_drop(publ, "title", basic_validation.is_non_empty_str)

        #NULLABLE
        self.validate_and_null(publ, "journal", basic_validation.is_non_empty_str, (basic_validation.length_check, 255))
        self.validate_and_null(publ, "publisher", basic_validation.is_non_empty_str,  (basic_validation.length_check, 255))
        self.validate_and_null(publ, "journal_type", basic_validation.is_non_empty_str, (basic_validation.length_check, 255))
        self.validate_and_null(publ, "ministerial_score", basic_validation.is_non_negative_int)
        self.validate_and_null(publ, "publication_year", basic_validation.validate_publication_year)

        #NOT IN THE TABLE
        self.validate_and_drop(publ, "scientist_ids", basic_validation.validate_uuid_str, process_independently=True) #NOT NULL -> check in database


    #only to be used with OrganizationItem
    def validate_organization(self, org):
        #NOT NULL
        self.validate_and_drop(org, "identifier", basic_validation.validate_uuid_str)
        self.validate_and_drop(org, "name", basic_validation.is_non_empty_str, (basic_validation.length_check, 255))
        self.validate_and_drop(org, "organization_type", basic_validation.validate_organization_type)

        #NOT IN THE TABLE
        #universities must have parent_id set to None
        if org["organization_type"] == "university":
            self.validate_and_drop(org, "parent_id", lambda v: v is None)
        else:
            self.validate_and_drop(org, "parent_id", basic_validation.validate_uuid_str) # - to do - check in database
#end of ValidationPipeline


#for checking any ids that refer to other objects
class DbValidationPipeline(ValidationPipeline):
    def __init__(self):
        self.conn = make_connection() #deliberate no exception handling - if no connection gets established, this pipeline is not supposed to work
        #self.items_processed = 0 #temp
        
    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        '''self.items_processed += 1
        if self.items_processed > 2:
            raise DropItem("item count exceeded")'''

        return super().process_item(item,spider)


    def validate_organization(self, org):
        super().validate_organization(org)

        if org["organization_type"] == "university":
            return

        parent_exists = False
        try:
            parent_exists = does_row_exist("organizations", org["parent_id"], self.conn)
        except Exception as e:
            logger.error(f"validate_organizations: sth went wrong when querying a database - {e}")

        if not parent_exists:
            raise DropItem( get_item_msg("Validation: dropped_item", org, f'parent_id {add_parenthesis(org["parent_id"])} could not be found in database') )
    #end of validate_organization


    def filter_in_db(self, ids, table, key=None, include_removed=False):
        '''
        checks if ids are in table in database

        ids (list of str) : ids to check in the database
        table (str) : name of the table to check in
        key (optional func) : function that will be called with each id, only the returned value of it will be used when querying the database (does not change ids or return types)
            e.g. lambda x: x[0]
        include_removed (bool) : if True will return tuple ( valid ids, invalid ids )
        
        returns a list of valid ids
            or tuple if include_removed
        '''
        mask = []
        exists = False
        for id in ids:
            if key:
                id = key(id)

            try: 
                exists = does_row_exist(table, id, self.conn)
            except Exception as e:
                self.error(f"filter_in_db: sth went wrong when querying the database - {e}")
            mask.append(exists)

        return filter_values(ids, mask, include_removed=include_removed)
    #end of filter_in_db


    def validate_scientist(self, sc):
        super().validate_scientist(sc)

        #checking organizations
        orgs = sc["organizations"]
        orgs, removed_orgs = self.filter_in_db(orgs, "organizations", key=lambda p: p[1], include_removed=True)

        #logging
        if removed_orgs:
            removed_text = " ".join( [ f'({p[0]}, {add_parenthesis(p[1])});' for p in removed_orgs ] )
            logger.info(f"validate_scientist: organizations {removed_text} could not be found in database")

        if not orgs:
            raise DropItem( get_item_msg("Validation: dropped item", sc, "ScientistItem had no valid organizations") )

        sc["organizations"] = orgs
    #end of validate_scientist

    def validate_publication(self, publi):
        super().validate_publication(publi)

        sc_ids = publi["scientist_ids"]
        valid_ids, removed_ids = self.filter_in_db(sc_ids, "scientists", include_removed=True)
 
        #logging
        if removed_ids:
            removed_text = ", ".join( [ add_parenthesis(id) for id in removed_ids ] )
            logger.debug(f"validate_publication: scientists {removed_text} could not be found in database")

        if not valid_ids:
            raise DropItem( get_item_msg("Validation: dropped item", publi, "None of PublicationItem's scientist_ids were in database") )

        publi["scientist_ids"] = valid_ids
    #end of validate_publication

#end of DbValidationPipeline




class DbStoragePipeline:
    def __init__(self):
        self.conn = make_connection() #deliberate no exception handling - if no connection gets established, this pipeline is not supposed to work

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        process_based_on_type(item, {
            ScientistItem : self.store_scientist,
            PublicationItem : self.store_publication,
            OrganizationItem : self.store_organization,
        }, default_handler= lambda x: None)
        return item

    def store_organization(self, org):
        #add organization
        insert_or_update_with_id(
            table = "organizations", 
            identifier = org["identifier"], 
            conn = self.conn,
            values = {
                "id" : org["identifier"],
                "name" : org["name"],
                "type" : org["organization_type"]
            }
        )

        #add relation as child
        insert_or_update_matched(
            table = "organizations_relationships", 
            search_param = { "child_id" : org["identifier"] }, 
            conn=self.conn, 
            values = {
                "parent_id" : org["parent_id"],
                "child_id" : org["identifier"]
            }
        )

        #if department, add relation as parent
        if org["organization_type"] == 'department':
            insert_or_update_matched(
                table = "organizations_relationships", 
                search_param = {"parent_id" : org["identifier"]},
                conn = self.conn, 
                values = {
                    "parent_id" : org["identifier"],
                    "child_id" : None
                }
            )
    #end of store_organization
            

    def store_scientist(self, sc):
        #choosing organization with lowest importance
        smallest_org = min( sc["organizations"], key=lambda p: p[0] )[1]

        #storing scientist
        insert_or_update_with_id(
            table = "scientists", 
            identifier = sc["identifier"], 
            conn = self.conn,
            values = {
                "id" : sc["identifier"],
                "first_name" : sc["first_name"],
                "last_name" : sc["last_name"],
                "academic_title" : sc["academic_title"],
                "position" : sc["position"],
                "email" : sc["email"],
                "profile_url" : sc["profile_url"]
            }
        )

        #storing scientist_organization
        #only one organization per scientist
        insert_or_update_matched(
            table = "scientist_organization", 
            search_param = {"scientist_id" : sc["identifier"]},
            conn = self.conn, 
            values = {
                "scientist_id" : sc["identifier"],
                "organization_id" : smallest_org
            }
        )

        #storing bibliometrics
        biblio = sc["bibliometrics_item"]
        insert_or_update_matched(
            table = "bibliometrics", 
            search_param = {"scientist_id" : sc["identifier"]},
            conn = self.conn, 
            values = {
                "h_index_wos" : biblio["h_index_wos"],
                "h_index_scopus" : biblio["h_index_scopus"],
                "publication_count" : biblio["publication_count"],
                "ministerial_score" : biblio["ministerial_score"],
                "scientist_id" : sc["identifier"],
            }
        )

        for research_area in sc["research_areas"]:
            #adding research area if not in database or updating with the same values
            research_area_id = insert_or_update_matched(
                table = "research_areas", 
                search_param = {"name" : research_area},
                conn = self.conn, 
                values = { "name" : research_area }
            )

            #pointless, why update if it has all values already
            #storing scientists_research_areas
            insert_or_update_matched(
                table="scientists_research_areas", 
                search_param = {
                    "scientist_id" : sc["identifier"], 
                    "research_area_id" : research_area_id
                }, 
                conn = self.conn, 
                values = {
                    "scientist_id" : sc["identifier"],
                    "research_area_id" : research_area_id
                }
            )
    #end of store_scientist

    def store_publication(self, publi):
        #storing publication
        publication_date = publi["publication_year"]
        if publication_date is not None:
            publication_date = date( publication_date, 1, 1)

        insert_or_update_with_id(
            table = "publications",
            identifier = publi["identifier"],
            conn = self.conn,
            values = {
                "id" : publi["identifier"],
                "title" : publi["title"],
                "journal" : publi["journal"],
                "publisher" : publi["publisher"],
                "journal_type" : publi["journal_type"],
                "publication_date" : publication_date,
                "ministerial_score" : publi["ministerial_score"]
            }
        )

        #rewriting data with the same data?
        #storing scientists_publications
        for sc_id in publi["scientist_ids"]:
            insert_or_update_matched(
                table = "scientists_publications",
                search_param = {
                    "publication_id" : publi["identifier"],
                    "scientist_id" : sc_id
                },
                conn = self.conn,
                values = {
                    "publication_id" : publi["identifier"],
                    "scientist_id" : sc_id
                }
            )
    #end of store_publication

#end of DbStoragePipeline

class ExportPreparationPipeline:
    '''
    before exporting processes items based on Field metadata

    Supported keys:
    dont_export (bool) : the value of item's key will be unset (the field will not be deleted though)
    as_item (bool) : treats item's value as a separate item
    '''
    def process_item(self, item, spider):
        for k,v in item.fields.items():
            if not v:
                continue

            if 'as_item' in v and k in item:
                item[k] = self.process_item(item[k], spider)

            if 'dont_export' in v:
                if k in item:
                    del item[k]
        #end of for
        return item
    #end of process_item
#end of ExportPreparationPipeline
