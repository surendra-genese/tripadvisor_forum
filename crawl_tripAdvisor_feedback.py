'''
Trip Advisor
'''
import csv
import requests
from lxml import html
BASE_URL = "https://www.tripadvisor.co.uk"
OUTPUT_CSV = 'tripadvisor_2020.csv'
def main():
    url = "https://www.tripadvisor.co.uk/ShowForum-g293889-i9243-o20-Nepal.html"
    
    next_link = True
    with open(OUTPUT_CSV,'w',newline='') as output_csv_file:
        headers = ['Forum','Topic','Replies','Last Post','Topic Link']
        thewriter = csv.writer(output_csv_file)
        thewriter.writerow(headers)
    while next_link:
        next_link = crawl(url)
        url = BASE_URL + next_link
def crawl(url):
    response = requests.get(url)
    tree = html.fromstring(response.text)
    #import pdb;pdb.set_trace()
    tables = tree.xpath("//table//tr")
    for table_row in tables[1:]:
        try:
            forum = table_row[1].xpath(".//text()")[1].strip()
        #import pdb;pdb.set_trace()
            topic_unfiltered = table_row[2].xpath(".//text()")
            topic = ' '.join([d.strip() for d in topic_unfiltered])
            replies = table_row[3].xpath(".//text()")[0].strip()
            last_post = table_row[4].xpath(".//text()")[1]
            topics_link = table_row[2].xpath(".//a/@href")[0]
            with open(OUTPUT_CSV,'a',newline='') as output_csv_file:
                headers = [forum,topic,replies,last_post,topics_link]
                thewriter = csv.writer(output_csv_file)
                thewriter.writerow(headers)
        except Exception as e:
            print(e)
    try:
        next_link = tree.xpath("//a[contains(text(),'»')]/@href")[1]
    except:
        next_link = False
    return next_link

if __name__ == "__main__":
    main()