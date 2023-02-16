from bs4 import BeautifulSoup
import json
import numpy as np
import requests
from requests.models import MissingSchema
import spacy
import trafilatura

def beautifulsoup_extract_text_fallback(response_content):

    soup = BeautifulSoup(response_content, 'html.parser')
    text = soup.find_all(text=True)
    
    cleaned_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',]

    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)
            
    cleaned_text = cleaned_text.replace('\t', '')
    return cleaned_text.strip()
    

def extract_text_from_single_web_page(url):
    
    downloaded_url = trafilatura.fetch_url(url)
    try:
        a = trafilatura.extract(downloaded_url, output_format="json", with_metadata=True, include_comments = False,
                            date_extraction_params={'extensive_search': True, 'original_date': True})
    except AttributeError:
        a = trafilatura.extract(downloaded_url, output_format="json", with_metadata=True,
                            date_extraction_params={'extensive_search': True, 'original_date': True})
    if a:
        json_output = json.loads(a)
        return json_output['text']
    else:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return beautifulsoup_extract_text_fallback(resp.content)
            else:
                return np.nan
        except MissingSchema:
            return np.nan


single_url = "https://link.springer.com/article/10.1007/s11023-021-09573-8"
text = extract_text_from_single_web_page(url=single_url)
print(text)