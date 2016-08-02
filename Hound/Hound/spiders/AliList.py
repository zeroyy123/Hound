from bs4 import BeautifulSoup
import pandas as pd
import re

class AliList():
    def __init__(self,response):
        self.response = response
        self.soup = BeautifulSoup(response.body, "html.parser")

    def get_top_list(self):
        elems = self.soup.find_all('div',class_='cg-main')
        elems = elems[0].find_all('li')
        # print len(elems)
        elems_url = []
        elems_name = []
        elems_parent = []
        for elem in elems:
            elem_parent = elem.find_parents('div',class_='item util-clearfix')
            elem_parent = elem_parent[0].find_all('a')
            elem_parent = elem_parent[0].text
            elems_parent.append(elem_parent)

            elem = elem.find_all('a')
            elem_url = 'http:' + elem[0].get('href')
            elems_url.append(elem_url)

            elem_name = elem[0].text
            elems_name.append(elem_name)

            print elem_parent,elem_name
            print elem_url
        return [elems_name,elems_parent,elems_url]

    def index_mode_adjust(self):
        elems = self.soup.find_all('dl',class_='son-category')
        if len(elems) == 0:
            mode = 'broad mode'
            print 'broad mode'
            return [elems,mode]
        else:
            mode = 'list mode'
            print 'list mode'
            return [elems,mode]

    def get_li_listmode(self,elems):
        elems = elems[0].find_all('li')
        return elems

    def get_li_detial_boardmode(self):
        elems = self.soup.find_all('div',class_='son-bc-list-wrap')
        if len(elems) == 0:
            elems = self.soup.find_all('div',class_='bc-list-wrap')
        elems = elems[0].find_all('ul',class_='bc-list bc-ul bc-list-not-standard')

        elems = elems[0].find_all('li')
        list = []
        for elem in elems:
            parent = elem.find_parent('ul')
            if parent[0].get('class') == 'bc-list bc-ul bc-list-not-standard':
                list.append(elem)

        items_name = []
        items_url = []
        items_parent = []
        for elem in list:
            li_elems = elem.find_all('li')
            if len(li_elems) == 0:
                [item_name,item_url] = self.get_next_url(elem)
                parent_name = ''
                items_name.append(item_name)
                items_url.append(item_url)
                items_parent.append(parent_name)
            else:
                parent_name = elem.find_all('div',class_='bc-cate-name bc-nowrap-ellipsis')
                parent_name = parent_name[0].find_all('a')
                parent_name = parent_name[0].text
                for li_elem in li_elems:
                    [item_name,item_url] = self.get_next_url(li_elem)
                    items_name.append(item_name)
                    items_url.append(item_url)
                    items_parent.append(parent_name)
        return [items_name,items_url,items_parent]


    def get_next_url(self,elem):
        temp = elem.find_all('a')
        item_url = 'http:' + temp[0].get('href')
        item_name = temp[0].text
        return [item_name,item_url]

    def get_item_detial(self):
        sc = self.soup.find_all('strong',class_='search-count')
        search_count = sc[0].text
        item_url = self.response.url
        name = self.soup.find_all('div',id='aliGlobalCrumb')
        name = name[0].find_all('h1')
        name = name[0].find_all('span')
        name = name[-1]
        name = name.text
        return [name,item_url,search_count]