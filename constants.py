ImageID = 1 # starts from 1
SourceID = 1 # starts from 1
AlertID = 1 # starts from 1
SourceID = 1 # start from 1
LocusID = 1 # start from 1
AstroObjID = 1 # start from 1
ReplicaID = 1 # start from 1
MaxReplicaNum = 5
AttrValID = 1 # start from 1

NumAlertsPerNight = 20

catalogs = ( '2MASS', 'Kepler', 'SDSS' )

BaseNight = { 'year': 2014, 'month': 12, 'day': 6,
           'hour': 23, 'min': 35, 'sec': 30 }
NumNights = 3

night1 = { 'year': 2014, 'month': 12, 'day': 6,
           'hour': 23, 'min': 35, 'sec': 30 }

night2 = { 'year': 2014, 'month': 12, 'day': 9,
           'hour': 21, 'min': 19, 'sec': 59 }

bright_range = ( 3.33, 9.99 )
delta_bright_range = ( 0.333, 0.999 )
ra_range = ( 10.68458, 54.45895 )
dec_range = ( 41.26917, 97.24892 )
uncert_range = ( 1, 10 )
channel_range = ( 1, 5 )

AstroAssoProb = 0.7

SHA1 = "547d5ecf357d887c123cd9b950ccc96a5594f851"
#SHA1 = "9d178220f594db551f2bbe6eaa308ea33c4fc092"

RarestProb = 0.15
Stage1Prob = 0.5
Stage2Prob = 0.75

attrs = {
    'IM-Temperature': 'Integer', # base
    'IM-NumAlerts': 'Integer', # derived
    'IM-Throttle': 'Integer', # derived
    'IM-AlertBrightnessDistribution': 'String', # derived
    'CA-G': 'Float', # base
    'CA-R': 'Float', # base
    'CA-GMinusR': 'Float', # derived
    'CA-CACoordinate': 'String', # base
    'AR-HasAstrObject': 'String', # base
    'AR-VeriablilityProbability': 'Float', # derived
}

containers = {
    'alert': 'E',
    'replica': 'R',
    'astro': 'A',
    'image': 'I',
    'source': 'S',    
}

tables = {
    'alert': 'protracker_alert',
    'replica': 'protracker_alertreplica',
    'astro': 'protracker_astroobject',
    'attr': 'protracker_attribute',
    'attrval': 'protracker_attributevalue',
    'derived_attr': 'protracker_derivedattribute',
    'image': 'protracker_image',
    'locus': 'protracker_locus',
    'locus_agg': 'protracker_locusaggregatedalert',
    'replica_astro': 'protracker_replicaassociatedwith',
    'source': 'protracker_source',
}
