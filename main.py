# Import required modules 
import csv
from dataclasses import fields
import pip._vendor.requests as requests
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

def savetoCSV(newsitems, filename):

    # Specific the filds for the csv file
    fields = ['guid', 'title', 'link', 'pubDate', 'description', 'media']

    # Writing to csv file
    with open(filename, 'w') as csvfile:

        # Create a csv writer object
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)

         # Write headers (field names)
        csvwriter.writeheader()

        # Write data rows (field values)
        csvwriter.writerows(newsitems)

def main():

    # Load RSS from web to update the xml file
    loadRSS()

    # Parse the xml file
    newsitems = parseXML('topnewsfeed.xml')

    # Store news items in a csv file
    savetoCSV(newsitems, 'topnews.csv')

if __name__ == "__main__":
    # Calling main function
    main()