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
    cc_raised = raised['crowdcube']
    ks_raised = raised['kickstarter']
    print('Capital raised.\n \
            CrowdCube: ', '{:0,.0f}'.format(cc_raised), ' GBP\n \
            KickStarter: ', '{:0,.0f}'.format(ks_raised), ' USD\n \
            Total raised (after currency conversion): ', '{:0,.0f}'.format(cc_raised + 0.82*ks_raised), ' GBP')
