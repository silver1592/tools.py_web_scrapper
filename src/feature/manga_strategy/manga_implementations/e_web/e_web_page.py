'''Module to set the implementation for page of E_web'''
from feature.manga_strategy.manga_interfaces import IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaPage
import feature.html_reader.common_attrs as COMMON_ATTRS
import feature.html_reader.common_tags as COMMON_TAGS

class EMangaPage(BaseMangaPage,IMangaPage):
    '''Structure in case of a EManga Page'''

    def get_img_url(self) -> tuple[str, dict[str,str]]:
        self._logger.debug("Getting image url from [%s]", self.url)
        imgs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "img")
        img = imgs[0]

        return img.get_attr_value(COMMON_ATTRS.SRC), {}

    def _get_image_name(self) -> str:
        divs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "i2")
        img_details_ele = divs[0].children[1]
        details = img_details_ele.get_value()
        det_array:list[str] = details.split("::")

        self.image_name = det_array[0].strip()
        return self.image_name

    def get_image_number(self) -> tuple[str,str]:
        div = self.reader.get_by_attrs(COMMON_ATTRS.ID, "i2")[0]
        img_details_ele = div.get_children_by_tag(COMMON_TAGS.SPAN)

        self.image_number = (
            img_details_ele[0].get_value().strip(),
            img_details_ele[1].get_value().strip()
        )
        return self.image_number

    def get_next_page_async(self) -> IMangaPage:
        next_page_url = self._get_next_image_url()
        new_page = self.strategy.get_page_from_url_async(next_page_url)

        return new_page

    def is_last_page(self) -> bool:
        next_page_url = self._get_next_image_url()
        return self.url == next_page_url

    def _get_next_image_url(self) -> str:
        imgs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "img")
        img = imgs[0]
        next_page_component = img.parent
        return next_page_component.get_attr_value(COMMON_ATTRS.HREF)

    def get_manga_name(self) ->str:
        manga_name = self.reader.get_by_tag_name(COMMON_TAGS.H1)[0]
        return manga_name.get_value()

    def get_index_page(self) -> IMangaIndex:
        manga_arrows = self.reader.get_by_attrs(COMMON_ATTRS.CLASS, "sb")
        index_arrow = manga_arrows[0].get_children_by_tag(COMMON_TAGS.ANCHOR)[0]
        href = index_arrow.get_attr_value(COMMON_ATTRS.HREF)

        return self.strategy.get_index_page(href)
