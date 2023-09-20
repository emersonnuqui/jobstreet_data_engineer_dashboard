import pandas as pd
import numpy as np
import random
import time
import os
import re
from tqdm import tqdm 
from datetime import datetime

import spacy
from spacy.matcher import Matcher

def get_languages(matcher, text):
    languages = [[{"LOWER": {"IN": ['apl', 'assembly', 'bash', 'shell', 'c++', 'c#', 'clojure',
                          'cobol', 'crystal', 'dart', 'delphi', 'elixir', 'haskell',
                          'java', 'javascript', 'julia', 'matlab', 'php','powershell', 'python',
                          'r', 'ruby', 'rust', 'sas', 'solidity', 'sql', 'vba','typescript', 'html', 'css',
                          'swift']}}],
            [{"LOWER":"c"}, {"ORTH":{"IN": ['#', "++"]}}]]
    
    for language in languages:
        matcher.add("LanguagePattern", [language])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    languages = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        languages.append(matched_text)
    languages = list(set(languages))
    languages = ", ".join(languages)
    return languages if languages != '' else None

def get_databases(matcher, text):
    
    databases = [[{"LOWER": {"IN": ['cassandra', 'couchbase', 'couchdb', 'dynamodb', 'elasticsearch', 
                                 'mariadb', 'mongodb', 'mysql', 'neo4j', 'oracle', 'postgresql',
                                 'redis', 'sqlite', 'db2']}}],
               [{"LOWER": "cloud"}, {"LOWER": 'firestone'}],
               [{"LOWER": "microsoft"}, {"LOWER": "sql"}, {"LOWER": "server"}],
               [{"LOWER": "firebase"}, {"LOWER": "realtime"}, {"LOWER": "database"}]]
    
    for database in databases:
        matcher.add("DatabasePattern", [database])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    database = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        database.append(matched_text)
    database = list(set(database))
    database = ", ".join(database)
    return database if database != '' else None

def get_cloud_platforms(matcher, text):
    cloud_platforms = [[{"LOWER": {"IN": ['aws', 'amazon', 'colocation', 'digitanocean', 'firebase',
                                        'heroku', 'linode', 'openstack', 'azure', 'gcp', 'ovh', 'vmware']}}],
                     [{"LOWER":'amazon'}, {"LOWER": "web"}],
                     [{"LOWER": 'google'}, {"LOWER": 'cloud'}],
                     [{"LOWER": 'microsoft'}, {"LOWER": 'azure'}],
                     [{'LOWER': "ibm"}, {"LOWER": 'cloud'}],
                     [{"LOWER": 'managed'}, {"LOWER": "hosting"}],
                     [{"LOWER": "oracle"}, {"LOWER": "cloud"}]]
    
    for cloud_platform in cloud_platforms:
        matcher.add("CloudPattern", [cloud_platform])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    cloud_platform = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        cloud_platform.append(matched_text)
    
    final_cloud = []
    for cloud in cloud_platform:
        if (cloud == 'aws') | (cloud=='amazon') | (cloud == "amazon web"):
            final_cloud.append("amazon web services")
        elif (cloud == 'azure') | (cloud == 'microsoft azure'):
            final_cloud.append('microsoft azure')
        elif (cloud == 'gcp') | (cloud == 'google cloud'):
            final_cloud.append("google cloud product")
        else:
            final_cloud.append(cloud)
            
    final_cloud = list(set(final_cloud))
    final_cloud = ", ".join(final_cloud)
    return final_cloud if final_cloud != '' else None
 
def get_web_frameworks(matcher, text):
    web_frameworks = [[{"LOWER": {"IN": ['angular', 'django', 'drupal', 'fastapi', 'fastify',
                                   'flask', 'jquery', 'gatsby', 'laravel', 'phoenix',
                                   'svelte', 'symfony', 'nodejs', 'nextjs', 'aspnet', 
                                   'vuejs', 'reactjs']}}]]
    for web_framework in web_frameworks:
        matcher.add("WebFrameworkPattern", [web_framework])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    web_framework = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        web_framework.append(matched_text)
    web_framework = list(set(web_framework))
    web_framework = ", ".join(web_framework)
    return web_framework if web_framework != '' else None

def get_libraries(matcher, text):
    libraries = [[{"LOWER": {"IN": ['kafka', 'spark', 'capacitor', 'electron', 'flutter',
                               'gtk', 'hadoop', 'ionic', 'keras', 'numpy', 'pandas',
                               'qt', 'scikit-learn', 'tensorflow', 'tidyverse',
                               'pytorch', 'pyspark', 'xamarin']}}],
            [{"LOWER": 'react'}, {"LOWER":"native"}],
            [{"LOWER": "hugging"}, {"LOWER": "face"}],
            [{"LOWER": "uno"}, {"LOWER": "platform"}]]
    
    for library in libraries:
        matcher.add("LibraryPattern", [library])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    library = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        library.append(matched_text)
    library = list(set(library))
    library = ", ".join(library)
    return library if library != '' else None

def get_developers(matcher, text):
    developers = [[{"LOWER" : {"IN": ['ansible', 'chef', 'docker', 'homebrew', 'kubernetes',
                                 'npm', 'pulumi', 'pupper', 'terraform', 'yarn']}}],
             [{"LOWER": "unity"}, {"LOWER": "3d"}],
             [{"LOWER": "unreal"}, {"LOWER": "engine"}]]
    
    for developer in developers:
        matcher.add("DeveloperPattern", [developer])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    developer = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        developer.append(matched_text)
    developer = list(set(developer))
    developer = ", ".join(developer)
    return developer if developer != '' else None

def get_data_visualizations(matcher, text):
    data_viz = [[{"LOWER": {"IN": ['looker', 'tableau', 'qlik', 'powerbi']}}],
               [{"LOWER": "power"}, {"LOWER": 'bi'}]]
    
    for data_vi in data_viz:
        matcher.add("DataVisualizationPattern", [data_vi])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    data_vi = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        data_vi.append(matched_text)
        
    final_data_viz = []
    for viz in data_vi:
        if (viz == "powerbi") | (viz == "power bi"):
            final_data_viz.append("power bi")
        else:
            final_data_viz.append(viz)
            
    final_data_viz = list(set(final_data_viz))
    final_data_viz = ", ".join(final_data_viz)
    return final_data_viz if final_data_viz != '' else None

def get_version_controls(matcher, text):
    version_controls = [[{"LOWER": {"IN": ['bitbucket', 'github', 'gitlab']}}]]
    
    for version_control in version_controls:
        matcher.add("VersionControlPattern", [version_control])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    version_control = []
    for match_id, start, end in matches:
        matched_text = doc[start:end].text.lower()
        version_control.append(matched_text)
    version_control = list(set(version_control))
    version_control = ", ".join(version_control)
    return version_control if version_control != '' else None

def matcher(df):
    nlp = spacy.load('en_core_web_sm')

    language_matcher = Matcher(nlp.vocab)
    database_matcher = Matcher(nlp.vocab)
    cloud_matcher = Matcher(nlp.vocab)
    web_framework_matcher = Matcher(nlp.vocab)
    library_matcher = Matcher(nlp.vocab)
    developer_matcher = Matcher(nlp.vocab)
    data_viz_matcher = Matcher(nlp.vocab)
    version_control_matcher = Matcher(nlp.vocab)

    for i, row in tqdm(df.iterrows()):
        text = row['summary']
        
        df.loc[i, ['languages', 'databases', 'cloud_platforms', 'web_frameworks',
                    'libraries', 'developers', 'data_visualization', 'version_controls']] = [get_languages(language_matcher, text),
                                                                                                get_databases(database_matcher, text),
                                                                                                get_cloud_platforms(cloud_matcher, text),
                                                                                                get_web_frameworks(web_framework_matcher, text),
                                                                                                get_libraries(library_matcher, text),
                                                                                                get_developers(developer_matcher, text),
                                                                                                get_data_visualizations(data_viz_matcher, text),
                                                                                                get_version_controls(version_control_matcher, text)
                                                                                                ]
    return df