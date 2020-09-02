'''
    move to pytest later
'''
from app import get_emails

def test_get_emails():
    test_info = {
                    "http://iliauni.edu.ge/ge/study/sakontaqto-informacia": 23,
                    "http://iliauni.edu.ge/ge/study/sakontaaaaaqto-informacia": 0,
                    'https://www.blg.com/en/people#q=%20&first=15&sort=%40biolastname%20ascending': 15,
                    'https://gowlingwlg.com/en/people/?page=2&q=&mode=anyword&sort=Lastname&locations=GWLG.Africa,GWLG.AustraliaNewZealand,GWLG.Austria,GWLG.BalticStates,GWLG.UnitedStates,GWLG.UK,GWLG.UAEDubai,GWLG.Netherlands,GWLG.Russia,GWLG.Switzerland,GWLG.Spain,GWLG.NordicRegion,GWLG.Luxembourg,GWLG.Italy,GWLG.Germany,GWLG.India,GWLG.Japan,GWLG.LatinAmerica,GWLG.Ireland': 12,

                }
    print("Test started", "\n", "#"*80)

    for url, expected_num in test_info.items():
        print(f"Checking ({expected_num}) {url:<70} ", end="|")
        try:
            emails_num = len(get_emails(url))
        except:
            emails_num = 0

        print("+" if emails_num == expected_num else "-")


# GO
test_get_emails()