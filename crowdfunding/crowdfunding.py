from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re
from time import time
import json


class DatabaseController:
    """
    A class that creates a mongo database with methods that that update to 
    aggregates information from the database.
    """
    def __init__(self):
        self.post = MongoClient('localhost', 27017).client.fundingplatforms.posts
    def update(self, args):
        new_posts = [ { 'platform' : arg[0],
                        'title' : arg[1],
                        'summary' : arg[2],
                        'link' : arg[3],
                        'raised' : arg[4],
                        'pct_raised' : arg[5],
                        'days_remain' : arg[6] }
                    for arg in args ]
        self.post.insert_many(new_posts)
    
    def raised(self, group_by=None, min_days = 10):
        if group_by == None:
            pipeline = [
                        { "$match" : { "days_remain" : { "$gte" : min_days }}},
                        {"$group": {"_id": None, "total" : {"$sum": "$raised"}}}
                        ]
        elif group_by == 'platform':
            pipeline = [
                        { "$match" : { "days_remain" : { "$gte" : min_days }}},
                        {"$group": {"_id": "$platform", "total" : {"$sum": "$raised"}}}
                        ]
        
        else: 
            raise ValueError("group_by must be None or 'platform'")
            
        agg = list(self.post.aggregate(pipeline))
        return { agg[i]['_id'] : agg[i]['total'] for i in range(len(agg)) }
       
        
    
class CrowdCube:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
    

    def scrape(self):
        url = 'https://www.crowdcube.com'
        content = requests.Session().post(url+'/investments', headers=self.headers)
        soup = BeautifulSoup(content.text, 'lxml')
        projects = soup.findAll('div', class_='pitch')
        
        data = list()
        for p in projects:
            # Extract the project summary and url separately
            summary = p.find('p', class_='pitch__description').text.strip()
            link = p.find('h2', class_='pitch__title').find('a').attrs['href']
            
            # Lets extract the JSON structure containing the required data.
            pStr = p.find('script').text.split('{', 1)[1].rsplit('}', 1)[0]
            jsonValue = '{' + re.sub('\s*(\S*)\s*:',r'"\1":', pStr).strip() + '}'
            p = json.loads(jsonValue)
            data.append( ['crowdcube',
                            p['pitch_name'],
                            summary,
                            link,
                            p['current_amount'],
                            p['progress'],
                            p['days_remaining'] ])
        return data

class KickStarter:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
    
    def scrape(self):
        
        # find IDs for the 15 categories. They are not 1,2, .., 15.

        content = requests.get('https://www.kickstarter.com/discover?ref=nav', headers=self.headers)
        cat = BeautifulSoup(content.text, 'lxml').findAll('div', class_='category-container mobile-col mb3')
        categories = [ int(re.findall('category-([0-9]+)', '\n'.join(cat[i].find('a').attrs['class']))[0]) 
                        for i in range(len(cat)) ] 

        url = 'https://www.kickstarter.com'
        data = list() 
        for i in categories:
            for j in range(1,6):
                url_page = url + \
                        '/discover/advanced?google_chrome_workaround\
                        &category_id={!s}&woe_id=0&sort=magic&seed=2462371&page={!s}'.format(i,j)
        
                # url_page is used to extract a list of JSON structures for category i and page j.
                projects = requests.get(url_page, headers=self.headers).json()['projects']
                time_now = int(time())
        
                # Just using list comprehension to make a list of JSONs to post into my mongoDB.
                data.extend([ [ 'kickstarter',
                                projects[k]['name'],
                                projects[k]['blurb'],
                                url + '/projects/' + str(projects[k]['creator']['id']) + '/'+ str(projects[k]['slug']),
                                int(float(projects[k]['usd_pledged'])),
                                int(100*int(float(projects[k]['pledged']))/int(float(projects[k]['goal']))),
                                int(1.0*(int(projects[k]['deadline'])-time_now)/(60*60*24)) ] for k in range(len(projects))
                            ])
        return data



if __name__ == "__main__":
    main()
