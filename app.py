import re
import time
import traceback
from requests_html import HTMLSession
from flask import Flask, render_template, request
from br_helper.br_helper import BrowserHelper

# test url
'''
    http://iliauni.edu.ge/ge/study/sakontaqto-informacia
'''

app = Flask(__name__)


def get_visible_text_from_url(url, case="requests", sleep_interval=6):
    if case == "requests":
        resp = HTMLSession().get(url)
        page_text =  resp.html.raw_html.decode('utf-8')

    elif case == "browser":
        br = BrowserHelper('chrome',
                            driver_path="files/chromedriver",
                            options={'visibility': 0,
                                    'hide_images': 1})
        br.get(url)
        time.sleep(sleep_interval // 2)
        br.bottom()
        time.sleep(sleep_interval // 2)

        # page_text = br.css1('html').text
        page_text = br.br.page_source
        br.close()

    return page_text


def get_emails(url, case="browser", print_ip=False):
    if print_ip: print(f'Processing request from {request.remote_addr}')

    page_text = get_visible_text_from_url(url, case=case)

    # from https://emailregex.com/
    pattern = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

    # breakpoint()
    emails = {match.group(0) for match in re.finditer(pattern, page_text.lower())}

    return sorted(list(emails))


# for humans
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method != "POST":
        return render_template('index.html')

    # results page        
    url = request.form.get('url')

    try:
        emails = get_emails(url)
        success = 1
    except Exception as e:
        print(traceback.format_exc())        
        emails = []
        success = 0

    return render_template(
                        'results.html',
                        **{'url': url, 'success': success, 'emails': emails})

# API
@app.route('/api/get_emails')
def get_emails_api():
    '''
        Make sure to pass url endoded links if we have such a case
        otherwise we may lose part of url.
    '''

    # breakpoint()
    url = request.args.get('url')
    case = request.args.get('fetch_method') if request.args.get('fetch_method') \
                                            in ['requests', 'browser'] else 'browser'

    try:
        emails = get_emails(url, case=case)
        success = 1
    except Exception as e:
        emails = []
        success = 0

    json_result = {
                    'url': url,
                    'webpage_responded': bool(success),
                    'results_number': len(emails),
                    'emails': emails,
                    }

    return json_result


if __name__ == "__main__":
    app.run(debug=False, port=9871, host="0.0.0.0")
