import requests


def get_html(url):
    """
    Return Request object
    :param url:
    :return:
    """

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36' \
                 ' (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

    r = requests.get(url, headers={'User-Agent': user_agent})

    return r

