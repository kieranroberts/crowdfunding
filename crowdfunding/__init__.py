from crowdfunding import crowdfunding
import threading
import queue

'''
crowdfunding: Main module
Copyright 2016, Kieran Roberts
Licensed under MIT.
'''

def enthread(target):
    q = queue.Queue()
    def wrapper():
        q.put(target())
    t = threading.Thread(target=wrapper)
    t.start()
    return q

def main():
    db = crowdfunding.DatabaseController()
    
    
    cc = crowdfunding.CrowdCube()
    ks = crowdfunding.KickStarter()
    
    threads = []
    scrapers = [cc,ks]
    
    for scraper in scrapers
        threads.append(enthread(target = scraper))
    
    for thread in threads:
        db.update(thread.get())
    
    raised = db.raised(group_by='platform', min_days=10)
    cc_raised = raised['crowdcube']
    ks_raised = raised['kickstarter']
    print('Capital raised.\n \
            CrowdCube: ', '{:0,.0f}'.format(cc_raised), ' GBP\n \
            KickStarter: ', '{:0,.0f}'.format(ks_raised), ' USD\n \
            Total raised (after currency conversion): ', '{:0,.0f}'.format(cc_raised + 0.82*ks_raised), ' GBP')
