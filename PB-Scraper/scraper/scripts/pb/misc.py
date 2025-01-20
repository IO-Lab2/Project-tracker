from logging import getLogger

from playwright.async_api import Page, expect

from utils.basic_conversion import try_make_int
from utils.log_messages import get_item_msg

logger = getLogger(__name__)

#awaits until all loading elements disappear
#throws an exception that stops loading if it takes too long
async def await_css_loaded(page:Page):
    await expect(page.locator("css=div.ui-outputpanel-loading").last).to_be_hidden(timeout=10_000)
    #await page.wait_for_load_state("networkidle")

#returns the total number of pages (positive int)
# retuns None if fails
#works with people_page and publication_page
def get_page_count(response):
    page_count_text = response.css("span.entitiesDataListTotalPages::text").get()
    if not page_count_text:
        logger.info("get_page_count: total page count could no be found - assuming it's 1")
        return 1
    page_count = try_make_int(page_count_text)
    if page_count is None or page_count <= 0:
        logger.error(f"get_page_count: invalid page count: {page_count_text}")
        return None
    return page_count

#alias for get_item_msg( event="Scraping: stopped parsing item" )
def get_stopped_scraping_item(item,description=None, **kwargs):
    return get_item_msg("Scraping: stopped parsing item", item, description, **kwargs)


