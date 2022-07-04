# Import required modules 
import csv
import requests
import xml.etree.ElementTree as ET

def loadRSS():

    # URL of rss feed
    url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'

    # Create http response object from give url
    resp = requests.get(url)

    # Saving the xml file
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)


def parseXML(xmlfile):

    # Create element tree object
    tree = ET.parse(xmlfile)

    # Get root element
    root = tree.getroot()

    # Create empty list for news items
    newsitems = []

    # Interate news items
    for item in root.findall('./channels/item'):

        # Empty news dictionary
        new = {}

        # Interate child elements of item
        for child in item:

            if child.tag == '{http://search.yahoo.com/mrss/}content':
                new['media'] = child.attrib['url']
            else:
                new[child.tag] = child.text.encode('utf8')
        
        # Append news dictionary to news items list
        newsitems.append(new)

    # Return news items list
    return newsitems