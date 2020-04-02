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
            'IL':'이스라엘','BR':'브라질','AU':'호주','NO':'노르웨이','JP':'일본'} 
#just top 20
MAX_TOP=20
RATE_STANDARD=1000
#Confirm rate standard
class CovidCrawler:
    last_updated=0
    def __init__(self):
        self.crawl_data()
        
    def crawl_data(self): #must call when data setting
        request=requests.get('https://coronaboard.kr')
        source=request.text
        soup = BeautifulSoup(source, 'html.parser')
        script_tag=str(soup.select('#top > script')[1])
        
        script_matched=re.search(r'var jsonData = (.+?);',script_tag,re.S)
        data_string=script_matched.group(1)
        json_data=json.loads(data_string)
        updated_info=json_data['lastUpdated'] #updated info in script
        
        if self.last_updated != updated_info:
            self.last_updated=updated_info
            self.world_data=json_data["statGlobalNow"] #Covid Global Stat
            self.get_nations_data_over_standard()
            self.set_data()
            return True
        
        return False #If False, Don't refresh.
    
    def get_nations_data_over_standard(self): #get nations data that confirmed over standard.  
        self.nations_over_standard=[nation for nation in self.world_data if nation['confirmed'] >= RATE_STANDARD]
        
    #All stats just show top 20
    def set_confirmed(self): 
        self.world_confirmed=sorted(self.world_data,key=lambda nation_data: nation_data['confirmed'],reverse=True)[:MAX_TOP]
    def get_confirmed(self): #must call after crawl_data
        return self.world_confirmed
    
    def set_active(self):
        self.world_active=sorted(self.world_data,key=lambda nation_data: nation_data['active'],reverse=True)[:MAX_TOP]
    def get_actvie(self): #must call after crawl_data
        return self.world_active
    
    def set_death(self):
        self.world_death=sorted(self.world_data,key=lambda nation_data: nation_data['death'],reverse=True)[:MAX_TOP]
    def get_death(self):  #must call after crawl_data
        return self.world_death
    
    def set_released(self):
        self.world_released=sorted(self.world_data,key=lambda nation_data: nation_data['released'],reverse=True)[:MAX_TOP]
    def get_released(self):
        return self.world_released
            
    def set_confirmed_increasement(self):
        self.world_confirmed_increasement=sorted(self.world_data,
                                                 key=lambda nation_data: nation_data['confirmed']-nation_data['confirmed_prev'] 
                                                 if 'confirmed_prev' in nation_data else nation_data['confirmed'],
                                                 reverse=True)[:MAX_TOP]
    def get_confirmed_increasement(self):
        return self.world_confirmed_increasement
    
    def set_released_rate(self):
        world_released_rate_rank=sorted(self.nations_over_standard,key=lambda nation_data: nation_data['released'] / nation_data['confirmed'] 
        if 'confirmed' in nation_data and nation_data['confirmed'] != 0 else 0,
                                       reverse=True)[:MAX_TOP]
        self.world_released_rate=[]
        
        for nation in world_released_rate_rank:
            self.world_released_rate.append({'cc':nation['cc'],'releasedRate':format(nation['released']/nation['confirmed']*100,'.1f')})
            
        
    def get_released_rate(self):
        return self.world_released_rate
    
    def set_death_rate(self):
        world_death_rate_rank=sorted(self.nations_over_standard,key=lambda nation_data: nation_data['death'] / nation_data['confirmed'] 
        if 'confirmed' in nation_data and nation_data['confirmed'] != 0 else 0,
                                       reverse=True)[:MAX_TOP]
        self.world_death_rate=[]
        
        for nation in world_death_rate_rank:
            self.world_death_rate.append({'cc':nation['cc'],'deathRate':format(nation['death']/nation['confirmed']*100,'.1f')})
            
    def get_death_rate(self):
        return self.world_death_rate
    
    def set_data(self):
        self.set_confirmed()
        self.set_active()
        self.set_death()
        self.set_released()
        self.set_confirmed_increasement()
        self.set_released_rate()
        self.set_death_rate()
    
if __name__=='__main__':
    covid=CovidCrawler()

    



        
        
        