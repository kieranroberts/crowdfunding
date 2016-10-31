from crowdfunding import crowdfunding

'''
crowdfunding: Main module

Copyright 2016, Kieran Roberts
Licensed under MIT.
'''

def main():
    db = crowdfunding.DatabaseController()
    
    cc = crowdfunding.CrowdCube()
    data = cc.scrape()
    db.update(data)
    
    ks = crowdfunding.KickStarter()
    data = ks.scrape()
    db.update(data)
    
    raised = db.raised(group_by='platform', min_days=10)
    print('Total raised.\nCrowdCube: ', raised['crowdcube'], '\nKickStarter: ', raised['kickstarter']) 
