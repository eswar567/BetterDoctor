#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 19:53:33 2018

@author: eswar
"""
import json
import pandas as pd
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("match_file", help = "provide match csv file path")
parser.add_argument("source_file", help = "provide source json file path")
args=parser.parse_args()


    
# read json file line by line and remove /n delimiter at end of each line 
read_source = open(args.source_file, "r").read() 
data = [json.loads(str(item)) for item in read_source.strip().split('\n')]


#normalize each line in json to dataframe for better analysis
source = pd.io.json.json_normalize(data, "practices",["doctor"])

#add columns to find matched documents based on first name and address
source[['first_name','second_name','npi']]=pd.DataFrame(source['doctor'].values.tolist()) # normalize nested loop doctor to diff columns
source['Source_ID']=source.index
source['Name']=source['first_name'].str.lower()+'_'+source['second_name'].str.lower()  #combine FirtName + Last Name
source['Address']=source['street'].str.lower()+'_'+source['street_2'].str.lower()+'_'+source['city'].str.lower()+'_'+source['state'].str.lower()+'_'+source['zip'].str.lower()

# read csv file and create dataframe
match=pd.read_csv(args.match_file)
match['Match_ID'] = match.index
match['Name']=match['first_name'].str.lower()+'_'+match['last_name'].str.lower()
match['Address']=match['street'].str.lower()+'_'+match['street_2'].str.lower()+'_'+match['city'].str.lower()+'_'+match['state'].str.lower()+'_'+match['zip'].str.lower()

merge_all=pd.merge(match,source,on=['npi','Name','Address'],how='inner')
merge=pd.merge(match,source, on = 'npi', how='inner')
merge_name = pd.merge(match,source, on='Name', how='inner')
merge_street = pd.merge(match,source, on='Address', how='inner')


Matched_doc = merge_all['Match_ID'].nunique()
Matched_doc_npi= merge['Match_ID'].nunique()
Matched_doc_name= merge_name['Match_ID'].nunique()
Matched_doc_address= merge_street['Match_ID'].nunique()

if __name__=="__main__":
    print ('Total matched documents:' , Matched_doc)
    print ('Number of matched documents by NPI:', Matched_doc_npi)
    print ('Number of matched documents using First and Last name:', Matched_doc_name)
    print ('Number of matched documents using Address:', Matched_doc_address)
    




