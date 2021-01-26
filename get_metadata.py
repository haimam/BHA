import requests
from bs4 import BeautifulSoup
import re
import json
import os

SPAN_BR_REGEX = r'<span style="color:#1B7EC1;">([^<]+)</span>([^<]+)<br>'
REF_REGEX = r'open\(\'([^\']+\')'
NUM_REGEX = r'^(.+)מס'
BASE_URL = 'http://iaflibrary.org.il/Page.asp?CatID=2683'
ISSUE = "גליון"
IAF_PREFIX = 'www.iaf.org.il'

MONTHS = ['ינואר', 'פברואר', 'פבואר', 'מרץ', 'מרס', 'מארס', 'אפריל', 'מאי', 'יוני', 'ינוי', 'יולי', 'אוגוסט', 'ספטמבר', 'ספטצבר', 'אוקטובר', 'נובמבר', 'דצמבר']
MONTHS_MAP = {
    "ינואר": "ינואר",
    "פברואר": "פברואר",
    "פבואר": "פברואר",
    "מרץ": "מרץ",
    "מרס": "מרץ",
    "מארס": "מרץ",
    "אפריל": "אפריל",
    "מאי": "מאי",
    "יוני": "יוני",
    "ינוי": "יוני",
    "יולי": "יולי",
    "אוגוסט": "אוגוסט",
    "ספטמבר": "ספטמבר",
    "ספטצבר": "ספטמבר",
    "אוקטובר": "אוקטובר",
    "נובמבר": "נובמבר",
    "דצמבר": "דצמבר",
}

ALL_DATA_FILE_PATH = 'all_data.json'


def json_write(data):
    with open(ALL_DATA_FILE_PATH, 'w') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf8').decode())


def json_read():
    try:
        if os.path.exists(ALL_DATA_FILE_PATH):
            with open('all_data.json', 'r') as json_file:
                result = json.load(json_file)
        else:
            result = {}
        return result
    except json.decoder.JSONDecodeError:
        return {}


def get_months(title, num):
    from_month, to_month, month = "", "", ""
    title_stripped = []
    for x in title:
        if '-' in x:
            title_stripped += x.split('-')
        else:
            title_stripped.append(x)
    months = [x for x in title_stripped if x in MONTHS]
    if len(months) == 1:
        month = MONTHS_MAP[months[0]]
    elif len(months) == 2:
        index_one = MONTHS.index(months[0])
        index_two = MONTHS.index(months[1])
        larger_index = index_one > index_two
        if larger_index:
            to_month = MONTHS_MAP[MONTHS[index_one]]
            from_month = MONTHS_MAP[MONTHS[index_two]]
        else:
            to_month = MONTHS_MAP[MONTHS[index_two]]
            from_month = MONTHS_MAP[MONTHS[index_one]]
    else:
        if num == "11":
            pass
        elif num == "12":
            pass
        elif num == "16-17":
            pass
        elif num == "33":
            from_month = "ספטמבר"
            to_month = "אוקטובר"
        elif num == "39-40":
            from_month = "מאי"
            to_month = "יוני"
        else:
            raise Exception('wow')
    return from_month, to_month, month


def get_metadata_from_library():
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

            title = td[0].findAll('b')[0].text.split()
            num = title[-1].strip(')').strip('(')
            new_num = "-1"
            if num == "1951":
                num = "16-17"
            try:
                number = int(num)
                if number > 100:
                    new_num = number - 100
            except ValueError:
                pass
            data = {"לינק": book_ref, "מספר גיליון": num, "כותר": ' '.join(title), "מספר גיליון חדש": new_num}
            from_month, to_month, month = get_months(title, num)
            if month:
                data.update({"חודש": month})
            else:
                if from_month and to_month:
                    data.update({"חודש התחלה": from_month, "חודש סוף": to_month})
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

    json_write(all_data)


def get_metadata_from_iaf():
    all_data = json_read()
    # response = requests.get("https://www.iaf.org.il/52-he/IAF.aspx")
    soup = BeautifulSoup(open('IAF_content.txt', 'r').read(), "html.parser")
    refs = soup.findAll('a', {'href': True, 'id': True, 'target': True})
    issue_refs = list(reversed([ref for ref in refs if ref.text.startswith(ISSUE)]))
    new_data = {}
    for issue_ref in issue_refs:
        if issue_ref.text != "גליון נוכחי":
            title = issue_ref.text.split()
            title_stripped = []
            for x in title:
                if ',' in x:
                    title_stripped += x.split(',')
                else:
                    title_stripped.append(x)
            link = issue_ref.attrs['href'].strip('http://').strip('https://').strip('?')
            link = link if link.startswith(IAF_PREFIX) else os.path.join(IAF_PREFIX, link)
            num = title_stripped[1].strip(',')
            if '-' in num:
                _, bigger_num = num.split('-')
            else:
                bigger_num = num
            if int(bigger_num) > 118:
                if not title_stripped[2]:
                    month = title_stripped[3]
                    year = title_stripped[4]
                else:
                    month = title_stripped[2]
                    year = title_stripped[3]
                data = {
                    "כותר": ' '.join(title),
                    "מספר גיליון חדש": num,
                    "לינק": link,
                    "חודש": MONTHS_MAP[month],
                    "שנת הוצאה": year
                }
                new_data.update({link: data})
    all_data.update(new_data)
    json_write(all_data)


def main():
    get_metadata_from_library()
    get_metadata_from_iaf()


if __name__ == '__main__':
    main()
