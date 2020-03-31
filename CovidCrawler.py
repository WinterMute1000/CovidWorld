# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 07:56:47 2020

@author: User
"""
import re
import requests
from bs4 import BeautifulSoup
import json

CC_MAPPING={'US':'미국','IT':'이탈리아','ES':'스페인','CN':'중국','DE':'독일','FR':'프랑스',
            'IR':'이란','GB':'영국','CH':'스위스','BE':'벨기에','NL':'네덜란드',
            'TR':'터키','KR':'대한민국','AT':'오스트리아','CA':'캐나다','PT':'포르투갈',
            'IL':'이스라엘','BR':'브라질','AU':'호주','NO':'노르웨이'} 
#just top 20
MAX_TOP=20
class CovidCrawler:
    last_updated=0
    def __init__(self):
        self.crawl_data()
        
    def crawl_data(self): #must call when data setting
        request=requests.get("https://coronaboard.kr")
        source=request.text
        soup = BeautifulSoup(source, 'html.parser')
        script_tag=str(soup.select('#top > script')[1])
        
        script_matched=re.search(r'var jsonData = (.+?);',script_tag,re.S)
        data_string=script_matched.group(1)
        json_data=json.loads(data_string)
        updated_info=json_data["lastUpdated"] #updated info in script
        
        if self.last_updated != updated_info:
            self.last_updated=updated_info
            self.world_data=json_data["statGlobalNow"] #Covid Global Stat
            self.set_data()
            return True
        
        return False #If False, Don't refresh.
    
    #All stats just show top 20
    def set_confirmed(self): 
        self.world_confirmed=sorted(self.world_data,key=lambda nation_data: nation_data["confirmed"],reverse=True)[:MAX_TOP]
    def get_confirmed(self): #must call after crawl_data
        return self.world_confirmed
    
    def set_active(self):
        self.world_active=sorted(self.world_data,key=lambda nation_data: nation_data["active"],reverse=True)[:MAX_TOP]
    def get_actvie(self): #must call after crawl_data
        return self.world_active
    
    def set_death(self):
        self.world_death=sorted(self.world_data,key=lambda nation_data: nation_data["death"],reverse=True)[:MAX_TOP]
    def get_death(self):  #must call after crawl_data
        return self.world_death
    
    def set_released(self):
        self.world_released=sorted(self.world_data,key=lambda nation_data: nation_data["released"],reverse=True)[:MAX_TOP]
    def get_released(self):
        return self.world_released
            
    def set_confirmed_increasement(self):
        self.world_confirmed_increasement=sorted(self.world_data,key=lambda nation_data: nation_data["confirmed"]-nation_data["confirmed_prev"],reverse=True)[:MAX_TOP]
    def get_confirmed_increasement(self):
        return self.world_confirmed_increasement
    
    def set_data(self):
        self.set_confirmed()
        self.set_active()
        self.set_death()
        self.set_released()
        self.set_confirmed_increasement()
        
if __name__=='__main__':
    covid=CovidCrawler()

    



        
        
        