import requests
from bs4 import BeautifulSoup
import re
import json

SPAN_BR_REGEX = r'<span style="color:#1B7EC1;">([^<]+)</span>([^<]+)<br>'
REF_REGEX = r'open\(\'([^\']+\')'
BASE_URL = 'http://iaflibrary.org.il/Page.asp?CatID=2683'


def main():
    all_data = {}
    for url in (BASE_URL, f'{BASE_URL}&page_n=2', f'{BASE_URL}&page_n=3'):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.findAll("div", {"class": "Book"})
        book_refs = [book.findAll("a")[1].attrs['href'] for book in books]
        for book_ref in book_refs:
            response = requests.get(book_ref)
            soup = BeautifulSoup(response.content, "html.parser")
            td = soup.findAll('td', {'width': '100%', 'align': 'right', 'valign': 'top', 'style': 'padding-right:20px;'})

            data = {"כותר": td[0].findAll('b')[0].text}

            span_br = set(str(td[0].findAll('br')).splitlines())
            for x in span_br:
                groups = re.findall(SPAN_BR_REGEX, str(x))
                if groups:
                    data[groups[0][0].strip(':')] = groups[0][1].strip()

            files = td[0].findAll('span', {'style': 'cursor:pointer;'})
            file_refs = [file.attrs['onclick'] for file in files]
            file_refs = [re.findall(REF_REGEX, file_ref)[0][:-1] for file_ref in file_refs]
            if len(file_refs) == 3:
                data.update({
                    "תוכן עניינים": file_refs[0],
                    "הורדה לקריאה במחשב": file_refs[1],
                    "הורדה לקורא אלקטרוני": file_refs[2]
                })
            else:
                data.update({
                    "הורדה לקריאה במחשב": file_refs[0],
                    "הורדה לקורא אלקטרוני": file_refs[1]
                })

            all_data[book_ref] = data

    with open('all_data.json', 'w') as f:
        f.write(json.dumps(all_data, indent=4, ensure_ascii=False).encode('utf8').decode())


if __name__ == '__main__':
    main()
