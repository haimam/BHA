from pdfminer.high_level import extract_text
from bidi.algorithm import get_display

from constants import REPLACE_CHAR

FILENAME = 'issues/test.pdf'
UTF_8 = 'utf-8'


def clean_line(raw_line):
    raw_line = raw_line.strip()
    line = ""
    for char in raw_line:
        line += REPLACE_CHAR.get(char, char)
    return line


def is_important_line(line):
    if not line:
        return False
    else:
        if line in ('^', '.', '..', '...'):
            return False
        return True

elemnts_lst = ["מוצא על־ידי", "העורך",  "םגן־העורך",  "תצלומים:", " תצלומי •השער", "הדפסת העטיפה:",


sgan_orech = {
    'name': 'deputy_editor',
    'possible_keys': [
        'סגן-עורך',
        'סגן-העורך',
        'םגן-עורך',
        'םגן-העורך',
        'סגן עורך',
        'סגן העורך',
        'םגן עורך',
        'םגן העורך'
    ]
}

keys = {

}

def main():
    metadata = """
     שנה 22• ,מם׳ 81
 מרם 1970
 מוצא על־ידי
 מפקדת חיל האויר
 העורך
 מ שה ה ד ר
 םגן־העורך
 רב סרן י הודה ע ופר
 תצלומים: יחידת צילום
 אוידי חיל האויר
 תצלומי •השער
 שמואל תובל
 מ נעי פנויים, דגמים וגלימות
 ישנים יש לפנות אך ודק אל:
 ההוצאה לאוד, מחי החפצה,
 דח׳ ב׳ פס׳ 29 ,הקריה, ת׳׳א
 ד ״פערב ח--
 דאד צבאי 2704
E£Y L HA'AVI K
I.D.F./AIR FORCE
MAGAZINE
ARMY POST No. 2704
ISRAEL
 ״הדפוס החדש״ בע״מ, ת״א
 הדפסת העטיפה:
 דפוס ניידט
 הדפסת הדגם:
 דפוס ״פסטל״ בע״מ
 המחיר: 50.2 ל״י
    """

    index = """
מכות מכאיבות לעומק - אלי פיינגדש . . . . 4
 כיקוד כטייסת פקייהוקים - ב. ארנון . . . . 12
 גס הפ מפילים מטופי אויב... - צבי גוטמן . . 19
 אצלנו כחיל 27
 פיפור קרב אחד - א. בדוד 30
 מטום התקיפה המעולה כיותר כעולם - גיטד, יפה . 34
 ״רוח הרפאים״ - עמוס עשת 50
 יום הרעייה - ג. יפה 66
 הדרך לשחקים - נתן גרוס 70
 המירז׳ המשופפ 78
 דאפו שונא לטופ!... - ג. צבי 85
 שערוריית ה״מירז׳ים״ 87
 ערבה, ״הצבר המעופןן״ - ג. אליעזר . . .. 90
 ״הטובים״ והבולים - יורם לוין 99
 ״מופקכה״ - מי אה 1 - ״גולדי״ 104
 התעשייה האוירונוטית במערב אירופה - י. צ׳צ׳יק . 107
 ח״א של דרום וויאטנם - ע. עמית 113
 ברית המועצות מחדשת פני חיל האויר שלה . . 126
 ״א־7״, יורשו של ה״פקייהוק״? - מאיד כהן . . 130
 חייו ומותו של הברון האדום 137
 מדרגות, מדרגות .' 144
 האיש שפרכ למוה 146
 הנשר מהים האגאי 148
 הזקן והקרחון - ג׳ים ליסטון 150
 האנחה האחרונה של ״אווז־חפח״ - אן צ׳מברלין . 154
 תשכץ תעופתי מפי 3 1
"""
    x = metadata.splitlines()
    y = index.splitlines()
    # pages = []
    # pdf = PdfFileReader(open(FILENAME, 'rb'))
    # for page in pdf.pages:
    #     pages.append(page.extractText().encode('cp1255').decode(UTF_8))
    # print(pages[0])
    print(metadata)


if __name__ == '__main__':
    main()
