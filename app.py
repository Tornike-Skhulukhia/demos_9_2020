import re
from requests_html import HTMLSession
from flask import Flask, render_template, request

# test url
'''
    http://iliauni.edu.ge/ge/study/sakontaqto-informacia
'''

app = Flask(__name__)

def get_emails(url):
    s = HTMLSession()
    resp = s.get(url)

    # from https://emailregex.com/
    pattern = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

    emails = {match.group(0) for match in re.finditer(pattern, resp.html.text.lower())}

    return emails


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
        # breakpoint()
        emails = []
        success = 0

    return render_template(
                        'results.html',
                        **{'url': url, 'success': success, 'emails': emails})

# API
@app.route('/api/get_emails')
def get_emails_api():
    url = request.args.get('url')

    try:
        emails = list(get_emails(url))
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
