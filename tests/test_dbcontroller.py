import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from crowdfunding.crowdfunding import DatabaseController

db = DatabaseController()
data = [[ 'crowdcube', 
            'MyFirstInvestment', 
            'Invest in me.', 
            'http://locahost',
            500,
            50,
            13],
        [ 'crowdcube', 
            'MySportsInvestment',
            'New sports team.',
            'http://localhost',
            3000,
            22,
            24],
        [ 'kickstarter',
            'ABCInc',
            'Nursery centers.',
            'http://localhost',
            117050,
            78,
            18],
        [ 'kickstarter',
            'Maths For All',
            'Tutoring service for students of mathematics.',
            'http://localhost',
            2456,
            72,
            5],
        [ 'crowdcube',
            'Mobile4me',
            'Converting old mobile phones into electronics kits.',
            'http://localhost',
            12,
            1,
            3]]

db.update(data)
for entry in db.find():
    print(entry)
    
print(db.raised('platforms'))
