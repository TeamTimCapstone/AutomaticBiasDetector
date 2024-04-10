import requests
from bs4 import BeautifulSoup

def scrape(url):
#    url = 'https://www.cnn.com/2024/03/15/politics/supreme-court-rules-that-public-officials-can-block-social-media-followers/index.html'
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output_with_newlines = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output_with_newlines += '{} '.format(t)
            output = ''.join(output_with_newlines.splitlines())
    
    #try:
     #   output = output[output.find('.')+1:]
    #    output = output[:output.rfind('.')+1]
    #except:
     #   pass

    return output
