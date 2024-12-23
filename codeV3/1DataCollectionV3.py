import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def fetch_arxiv_papers(query, start=0, max_results=100):
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
        'search_query': query,
        'start': start,
        'max_results': max_results,
        'sortBy': 'lastUpdatedDate',
        'sortOrder': 'descending'
    }
    
    response = requests.get(base_url, params=params)
    return response.content

def parse_arxiv_response(xml_content):
    soup = BeautifulSoup(xml_content, 'lxml')       ### ----> Changed xml parser to lxml
    papers = []
    
    for entry in soup.find_all('entry'):
        paper = {}
        paper['title'] = entry.title.text.strip()
        paper['abstract'] = entry.summary.text.strip()
        paper['published'] = entry.published.text.strip()
             ### ----> Changed to same as above lines to fix error ---> same error ---> removing to see what happens ---> worked collecting papers
        paper['categories'] = [category['term'] for category in entry.find_all('category')]
        papers.append(paper)
    
    return papers

def collect_arxiv_data(query, total_results=1000, batch_size=100):
    all_papers = []
    for start in range(0, total_results, batch_size):
        xml_content = fetch_arxiv_papers(query, start, batch_size)
        papers = parse_arxiv_response(xml_content)
        all_papers.extend(papers)
        print(f"Collected {len(all_papers)} papers so far...")
        sleep(3)  # Be respectful to the API
    
    return pd.DataFrame(all_papers)

# Main execution
if __name__ == "__main__":
    query = 'all:semiconductor'
    df = collect_arxiv_data(query)
    
    # Save to CSV
    df.to_csv('arxiv_semiconductors.csv', index=False)
    print(f"Saved {len(df)} papers to arxiv_semiconductors_chemistry.csv")

    # Display first few rows and basic info
    print(df.head())
    print(df.info()) 