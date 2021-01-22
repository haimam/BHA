from pdfminer.high_level import extract_text
from bidi.algorithm import get_display

FILENAME = 'issues/81.pdf'
UTF_8 = 'utf-8'


def main():
    text = get_display(extract_text(FILENAME, codec=UTF_8))
    lines = text.splitlines()
    # pages = []
    # pdf = PdfFileReader(open(FILENAME, 'rb'))
    # for page in pdf.pages:
    #     pages.append(page.extractText().encode('cp1255').decode(UTF_8))
    # print(pages[0])
    print(text)


if __name__ == '__main__':
    main()
