#!/bin/env python3

"""
Mimic a silly Antares Pipeline, the main
purpose is to populate the Antares database with
some fake data to test provenance queries.
"""

import pymysql
from datetime import datetime
import constants as consts
from constants import tables, delta_bright_range, bright_range, \
    ra_range, dec_range, uncert_range, night1, night2, catalogs, \
    containers, NumAlertsPerNight, NumNights, BaseNight
import random
from algorithm import ComputeAttributes

Debug = False
Reset = True

## combine the given 'ra' and 'dec' into a coordinate.
def coord():
    ra = random.uniform( ra_range[0], ra_range[1] )
    dec = random.uniform( dec_range[0], dec_range[1] )
    return str(ra) + ':' + str(dec)

## return a value of brightness for the source table
def brightness():
    return random.uniform( bright_range[0], bright_range[1] )

## return a value of delta brightness for the source table
def delta_brightness():
    return random.uniform( delta_bright_range[0], delta_bright_range[1] )

def uncert():
    return random.randint( uncert_range[0], uncert_range[1] )

def deltaT( target ):
    if target == 'ImageBase':
        return random.randint( 0, 2 )

    if target == 'AlertBase':
        return random.randint( 1, 3 )

    if target == 'ReplicaBase':
        return random.randint( 2, 4 )

    if target == 'AlertDerived':
        return random.randint( 1, 3 )


def print_table( tablename ):
    print( '\nSelect everything from {0} table.\n'.format(tables[tablename]) )
    query = "select * from {0}".format( tables[ tablename ] )
    cur.execute( query )
    for r in cur.fetchall():
        print( r )


def setup_db():
    ## connect to database
    global conn, cur # make them global for convenience
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares' )
    cur = conn.cursor()

    if Reset == True:
        ## delete one by one to avoid potential constraints violations.
        sql_delete = 'delete from protracker_attributevalue'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_derivedattribute'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_replicaassociatedwith'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_alertreplica'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_alert'
        cur.execute( sql_delete )        
        sql_delete = 'delete from protracker_source'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_image'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_astroobject'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_attribute'
        cur.execute( sql_delete )        
        sql_delete = 'delete from protracker_locus'
        cur.execute( sql_delete )
        sql_delete = 'delete from protracker_attributevalue'
        cur.execute( sql_delete )
                                
## populate tables for processing
def setup_tables():

    # set up attribute table
    for k,v in consts.attrs.items():
        sql_insert = """insert into {0} values("{1}",{2},"{3}")""".format(
            tables['attr'], k, random.randint(0, 1), v )
        cur.execute( sql_insert )

    for i in range( 0, NumNights ): # one image per night
        night = { 'year': BaseNight['year'], 'month': BaseNight['month'],
                  'day': BaseNight['day'] + i*3, 'hour': BaseNight['hour'],
                  'min': BaseNight['min'], 'sec': BaseNight['sec']}
        taken_at = datetime( night['year'], night['month'], night['day'], 
                             night['hour'], night['min'], night['sec'] )
        telescope = "LSST-{0}".format( i+1 )
        passband = "Passband Filter {0}".format( i+1 )
        sql_insert = """insert into {0} values({1},"{2}","{3}","{4}")""".format(
            tables['image'], consts.ImageID, taken_at, telescope, passband )
        cur.execute( sql_insert )

        baseattr_image( consts.ImageID, night )
        setup_alerts( consts.ImageID, night )
        consts.ImageID += 1

    conn.commit()
    if Debug:
        print_table( 'image' )
        print_table( 'attr' )
        print_table( 'source' )
        print_table( 'locus' )
        print_table( 'alert' )
        print_table( 'astro' )
        print_table( 'replica' )
        print_table( 'replica_astro' )

def setup_alerts( img_id, night ):
    for i in range( 1, NumAlertsPerNight ):
        ## populate the source table
        pos = coord()
        sql_insert = """insert into {0} values({1},"{2}",{3},{4},"{5}",{6})""".format(
            tables['source'], consts.SourceID, pos, brightness(),
            delta_brightness(), "/path/to/thumbnail", img_id )
        cur.execute( sql_insert ) 

        ## populate the locus table
        sql_insert = """insert into {0} values({1},"{2}",{3})""".format(
            tables['locus'], consts.LocusID, pos, uncert() )
        cur.execute( sql_insert )

        taken_at = datetime( night['year'], night['month'], night['day'], 
                             night['hour'], night['min'], night['sec'] )

        ## populate the alert table
        sql_insert = """insert into {0} values({1},"{2}",{3},{4},"{5}")""".format(
            tables['alert'], consts.AlertID, taken_at,
            consts.LocusID,consts.SourceID, 'NA' )
        cur.execute( sql_insert )

        ## populate the astroobject table
        sql_insert = """insert into {0} values({1},"{2}",{3},{4},{5})""".format(
            tables['astro'], consts.AstroObjID,
            catalogs[random.randint(0, len(catalogs)) - 1],
            random.randint(0, 9999), random.randint(0, 1), consts.LocusID )
        cur.execute( sql_insert )

        baseattr_alert( consts.AlertID, night )
        fork_replicas( consts.AlertID, consts.LocusID, night )

        consts.AlertID += 1
        consts.SourceID += 1
        consts.LocusID += 1
        consts.AstroObjID += 1

def baseattr_image( imgid, night ):

    computed_at = datetime( night['year'], night['month'], night['day'], 
                            night['hour'], night['min'], night['sec']+deltaT('ImageBase') )

    attrname = 'IM-Temperature'
    container_type = containers[ 'image' ]
    val = random.randint(50, 80)
    confidence = random.random()
    annotation = 'Base Attribute: Temperature'

    sql_insert = """insert into {0} values({1},{2},"{3}","{4}","{5}","{6}",{7},"{8}")""".format(
        tables['attrval'], consts.AttrValID, imgid, container_type, computed_at,
        val, annotation, confidence, attrname )
    cur.execute( sql_insert )
    consts.AttrValID += 1

def baseattr_alert( aid, night ):
    ## attributes for alert
    computed_at = datetime( night['year'], night['month'], night['day'], 
                            night['hour'], night['min'], night['sec']+deltaT('AlertBase') )
    attrname = 'CA-G'
    container_type = containers[ 'alert' ]
    val = random.uniform( 4537.239, 8916.328 )
    confidence = random.random()
    annotation = 'Base Attribute: G'

    sql_insert = """insert into {0} values({1},{2},"{3}","{4}","{5}","{6}",{7},"{8}")""".format(
        tables['attrval'], consts.AttrValID, aid, container_type, computed_at,
        val, annotation, confidence, attrname )
    cur.execute( sql_insert )
    consts.AttrValID += 1

    attrname = 'CA-R'
    val = random.uniform( 1239.389, 3231.439 )
    confidence = random.random()
    annotation = 'Base Attribute: R'

    sql_insert = """insert into {0} values({1},{2},"{3}","{4}","{5}","{6}",{7},"{8}")""".format(
        tables['attrval'], consts.AttrValID, aid, container_type, computed_at,
        val, annotation, confidence, attrname )
    cur.execute( sql_insert )
    consts.AttrValID += 1


## initialize base attributes
def baseattr_replica( rid, has_astro, night ):

    ## attributes for replicas
    computed_at = datetime( night['year'], night['month'], night['day'], 
                            night['hour'], night['min'], night['sec']+deltaT('ReplicaBase') )
    attrname = 'AR-HasAstrObject'
    container_type = containers[ 'replica' ]
    val = has_astro
    confidence = random.random()
    annotation = 'Base Attribute: Has AstroObject?'

    sql_insert = """insert into {0} values({1},{2},"{3}","{4}","{5}","{6}",{7},"{8}")""" .format(
        tables['attrval'], consts.AttrValID, rid, container_type, computed_at,
        val, annotation, confidence, attrname )
    cur.execute( sql_insert )
    consts.AttrValID += 1

def compute_derivedattr( night ):
    ## attributes for alert
    taken_at = datetime( night['year'], night['month'], night['day'],
                         night['hour'], night['min'], night['sec'] )
    query = """select * from {0} where TakenAt="{1}" """.format( tables['alert'], taken_at )
    cur.execute( query )
    alerts = cur.fetchall()
    for r in alerts:
        aid = r[ 0 ]
        computed_at = datetime( night['year'], night['month'], night['day'], 
                                night['hour'], night['min'], night['sec']+deltaT('AlertDerived') )
        attrname = 'CA-GMinusR'
        container_type = containers[ 'alert' ]
        
        query = """select * from {0} where ContainerID={1} and ContainerType="{2}" and AttrName_id="{3}" """.format(
            tables['attrval'], aid, containers['alert'], "CA-G" )
        cur.execute( query )
        G = cur.fetchall()[0][4]
        
        query = """select * from {0} where ContainerID={1} and ContainerType="{2}" and AttrName_id="{3}" """.format(
            tables['attrval'], aid, containers['alert'], "CA-R" )
        cur.execute( query )
        R = cur.fetchall()[0][4]

        val = ComputeAttributes.ComputeGMinusR( float(G), float(R) )
        confidence = random.random()
        annotation = 'Derived Attribute: GMinusR'

        sql_insert = """insert into {0} values({1},{2},"{3}","{4}","{5}","{6}",{7},"{8}")""" .format(
            tables['attrval'], consts.AttrValID, aid, container_type, computed_at,
            val, annotation, confidence, attrname )
        cur.execute( sql_insert )

        sql_insert = """insert into {0}(HashName,FunctionName,FileName,PackageName,AstronomerName,AttrName_id)
        values("{1}","{2}","{3}","{4}","{5}","{6}")""" .format(
            tables['derived_attr'], consts.SHA1, 'ComputeGMinusR', 'ComputeAttributes.py',
            'algorithm', 'Astronomer-A', attrname )
        cur.execute( sql_insert )

        consts.AttrValID += 1
    
        query = "select * from {0} where AlertID_id={1}".format( tables['replica'], aid )
        cur.execute( query )
        for r in cur.fetchall():
            rid = r[ 0 ]
            computed_at = datetime( night1['year'], night1['month'], night1['day'], 
                                    night1['hour'], night1['min'], night1['sec']+5 )
            attrname = 'AR-VeriablilityProbability'
            container_type = containers[ 'replica' ]
            val = ComputeAttributes.ComputeVeriProb()
            confidence = random.random()
            annotation = 'Derived Attribute: Veriablility Probability'

            sql_insert = """insert into {0} values({1},{2},"{3}","{4}","{5}","{6}",{7},"{8}")""".format(
                tables['attrval'], consts.AttrValID, rid, container_type, computed_at,
                val, annotation, confidence, attrname )
            cur.execute( sql_insert )

            sql_insert = """insert into {0}(HashName,FunctionName,FileName,PackageName,AstronomerName,AttrName_id)
            values("{1}","{2}","{3}","{4}","{5}","{6}")""" .format(
                tables['derived_attr'], consts.SHA1, 'ComputeVeriProb', 'ComputeAttributes.py',
                'algorithm', 'Astronomer-B', attrname )
            cur.execute( sql_insert )

            consts.AttrValID += 1

    conn.commit()

    if Debug:
        print_table( 'attrval' )
        print_table( 'derived_attr' )
    
# cleanup...
def finalize():
    cur.close()
    conn.close()

def fork_replicas( aid, locus, night ):
    astroobjs = []
    ## retrieve all astro objects
    query = "select * from {0}".format( tables['astro'] )
    cur.execute( query )
    for r in cur.fetchall():
        astroobjs.append( r[0] )

    ## fork replicas
    replica_num = random.randint( 0, consts.MaxReplicaNum )
    for i in range( 1, replica_num+1 ):
        ## populate the alert replica table
        sql_insert = """insert into {0} values({1},{2},{3},{4},{5},{6})""".format(
            tables['replica'], consts.ReplicaID, i, random.randint(1,5),
            random.random(), aid, locus )
        cur.execute( sql_insert )

        has_astro = 'False'
        ## astro object association
        if random.random() > consts.AstroAssoProb:
            index = random.randint( 0, len(astroobjs)-1 )
            sql_insert = """insert into {0}(AssociationProbability,AstroObjectID_id,ReplicaID_id) values({1},{2},{3})""".format(
                tables['replica_astro'], random.random(),
                astroobjs[index], consts.ReplicaID )
            cur.execute( sql_insert )
            has_astro = 'True'

        baseattr_replica( consts.ReplicaID, has_astro, night )
        consts.ReplicaID += 1

def filter_alerts( night ):

    decision = ''
    taken_at = datetime( night['year'], night['month'], night['day'],
                         night['hour'], night['min'], night['sec'] )
    query = """select * from {0} where TakenAt="{1}" """.format( tables['alert'], taken_at )
    cur.execute( query )
    alerts = cur.fetchall()
    for r in alerts:
        aid = r[ 0 ]
        prob = random.random()
        if prob < consts.RarestProb:
            decision = 'R'
        elif prob < consts.Stage2Prob:
            decision = 'L2'
        elif prob < consts.Stage1Prob:
            decision = 'L1'
        else:
            decision = 'D'

        sql_update = """update {0} set Decision="{1}" where AlertID={2} """.format(
            tables['alert'], decision, aid )
        cur.execute( sql_update )

    conn.commit()
    if Debug:
        print_table( 'alert' )

def main():
    setup_db()
    setup_tables()
    
    for i in range( 0, NumNights ): # one image per night
        night = { 'year': BaseNight['year'], 'month': BaseNight['month'],
                  'day': BaseNight['day'] + i*3, 'hour': BaseNight['hour'],
                  'min': BaseNight['min'], 'sec': BaseNight['sec']}
        compute_derivedattr( night )

    for i in range( 0, NumNights ): # one image per night
        night = { 'year': BaseNight['year'], 'month': BaseNight['month'],
                  'day': BaseNight['day'] + i*3, 'hour': BaseNight['hour'],
                  'min': BaseNight['min'], 'sec': BaseNight['sec']}
        filter_alerts( night )

    finalize()

if __name__ == '__main__':
    main()
