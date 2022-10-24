import requests
import json
import re
from bs4 import BeautifulSoup

from mydataclasses import Price
from exceptions import \
    RequestException, \
    UnexpectedPageStructureException, \
    FailedToGetJsonException, \
    ProductNotAvailableException


def magnit_cosmetic_parser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    try:
        request = requests.post(url=url, headers=headers)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")

    shop = html.select('.js-shop__xml-code')
    if len(shop) == 0:
        raise UnexpectedPageStructureException(url=url)
    shop_xml_code = shop[0]['value']

    enigmat = html.select('.js-remains')
    if len(enigmat) == 0:
        raise UnexpectedPageStructureException(url=url)
    enigma_token = enigmat[0]['value']

    json_data = None
    try:
        for line in str(html).split('\n'):
            if "PRODUCT_XML_CODE" in line:
                json_str = re.search(r'\{.*\}', line).group(0)
                json_data = list(json.loads(json_str).items())[0]
    except json.JSONDecodeError:
        raise FailedToGetJsonException(url=url)
    if json_data is None:
        raise FailedToGetJsonException(url=url)

    payload = (
            "SHOP_XML_CODE={xmlcode}&".format(xmlcode=shop_xml_code) +
            "PRODUCTS%5B{j1}%5D={j2}&".format(j1=json_data[0], j2=json_data[1]) +
            "JUST_ONE=Y&"
            "enigma={enigma}&".format(enigma=enigma_token) +
            "ism=N&"
            "type=detail"
    )

    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://magnitcosmetic.ru',
        'Referer': 'https://magnitcosmetic.ru/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    url = 'https://magnitcosmetic.ru/local/ajax/load_remains/catalog_load_remains.php'
    try:
        request = requests.request("POST", url, headers=headers, data=payload)
    except requests.exceptions.RequestException:
        RequestException(url=url)

    try:
        json_odj = json.loads(request.text)
        price = [int(part) for part in json_odj['data'][0]['price'].split('.')]
    except json.JSONDecodeError:
        raise FailedToGetJsonException(url=url)

    if price[0] == price[1] == 0:
        raise ProductNotAvailableException(url=url)

    default_price = Price(price[0], price[1])
    promo_price = None

    return default_price, promo_price


def magnit_parser(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        request = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")

    s1 = html.select(".label__price_new")
    s2 = html.select(".label__price_old")

    if (len(s1) > 2 or len(s2) > 2) or \
            (len(s1) == 0 and len(s2) == 0):
        raise UnexpectedPageStructureException(url=url)

    if len(s2) == 0:
        p1 = [int(part) for part in s1[0].text.strip().split()]
        p2 = None

        default_price = Price(p1[0], p1[1])
        promo_price = None
    else:
        p1 = [int(part) for part in s1[0].text.strip().split()]
        p2 = [int(part) for part in s2[0].text.strip().split()]

        default_price = Price(p2[0], p2[1])
        promo_price = Price(p1[0], p2[0])

    return default_price, promo_price


def sem_dney_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s1 = html.select(".tovarview_newprice")
    s2 = html.select(".tovarview_oldprice")

    if len(s1) == 0 or len(s2) == 0:
        raise UnexpectedPageStructureException(url=url)

    p1 = [int(part) for part in s1[0].text.split('.')]
    p2 = [int(part) for part in s2[0].text.split('.')]

    if len(p1) == 1:
        promo_price = Price(p1[0], 0)
    else:
        promo_price = Price(p1[0], p1[1])

    if len(p2) == 1:
        default_price = Price(p2[0], 0)
    else:
        default_price = Price(p2[0], p2[1])

    return default_price, promo_price


def vprok_parser(url):
    try:
        url = url[:-1]
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s = html.select(".ml-2")
    if len(s) == 0:
        raise UnexpectedPageStructureException(url=url)

    p1 = s[0]
    p2 = s[1]

    if "text-muted" in str(p1):
        p2 = [int(part) for part in s[1].text.split()[0].split('.')]
        default_price = Price(p2[0], p2[1])
        promo_price = None
    else:
        p1 = [int(part) for part in s[0].text.split()[0].split('.')]
        p2 = [int(part) for part in s[1].text.split()[0].split('.')]
        default_price = Price(p2[0], p2[1])
        promo_price = Price(p1[0], p1[1])

    return default_price, promo_price


def victoria_parser(url):
    try:
        url = url[:-1]
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s = html.select(".priceVal")
    if len(s) == 0:
        raise UnexpectedPageStructureException(url=url)
    s = [int(part) for part in s[0].text.split()[0].split(',')]

    default_price = Price(s[0], s[1])
    promo_price = None

    return default_price, promo_price


def zapovednaya_polyana_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")

    s = html.select(".price_matrix_block")
    if len(s) == 0:
        raise UnexpectedPageStructureException(url=url)
    html = BeautifulSoup(str(s[0]), "html.parser")

    s1 = html.select(".price")
    s2 = html.select(".price.discount")
    if len(s1) == len(s2) == 0:
        raise UnexpectedPageStructureException(url=url)

    if len(s2) == 0:
        p = s1[0]['data-value']
        if len(p.split('.')) == 1:
            default_price = Price(int(p), 0)
        else:
            default_price = Price(int(p.split('.')[0]), int(p.split('.')[1]))
        promo_price = None

    else:
        p1 = s1[0]['data-value']
        if len(p1.split('.')) == 1:
            promo_price = Price(int(p1), 0)
        else:
            promo_price = Price(int(p1.split('.')[0]),  int(p1.split('.')[1]))

        p2 = s2[0]['data-value']
        if len(p2.split('.')) == 1:
            default_price = Price(int(p2), 0)
        else:
            default_price = Price(int(p2.split('.')[0]), int(p2.split('.')[1]))

    return default_price, promo_price


def okeandra_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s = html.find(id="price-field")

    if s is None:
        raise UnexpectedPageStructureException(url=url)

    default_price = Price(int(s.text.split()[0]), 0)
    promo_price = None

    return default_price, promo_price


def kalina_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s = html.find(itemprop="highPrice")

    if s is None:
        raise UnexpectedPageStructureException(url=url)

    default_price = Price(int(s['content']), 0)
    promo_price = None

    return default_price, promo_price


def belfeya_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s = html.find(id="productPrice")

    if s is None:
        raise UnexpectedPageStructureException(url=url)

    p = [int(part) for part in s.text.split()[0].split('.')]
    default_price = Price(p[0], p[1])
    promo_price = None

    return default_price, promo_price


def wbc_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s1 = html.find(id="good_price")
    s2 = html.find(itemprop="price")

    if s1 is None and s2 is None:
        raise UnexpectedPageStructureException(url=url)

    new_price = [int(part) for part in s1.text.split('.')]
    old_price = [int(part) for part in s2.text.split('.')]
    if new_price == old_price:
        default_price = Price(new_price[0], new_price[1])
        promo_price = None
    else:
        default_price = Price(old_price[0], old_price[1])
        promo_price = Price(new_price[0], new_price[1])

    return default_price, promo_price


def optima_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    price_block = html.select(".description__right-buy")
    if len(price_block) == 0:
        raise UnexpectedPageStructureException(url=url)

    arr = [elem for elem in price_block[0].text.split('\n') if elem]
    if len(arr) == 2:
        default_price = Price(int(arr[0].split()[1]), 0)
        promo_price = None
    else:
        default_price = Price(int(arr[1].split()[0]), 0)
        promo_price = Price(int(arr[0].split()[1]), 0)

    return default_price, promo_price


def parfum_lider_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    new_price = None
    old_price = None
    for line in str(html).split('\n'):
        if "getCatalogDetail" in line:
            json_str = re.search(r'\{.*\}', line).group(0)
            json_obj = json.loads(json_str)
            new_price = str(json_obj['PRICE'])
            old_price = str(json_obj['PRICE_OLD'])
            break
    if new_price is None and old_price is None:
        raise UnexpectedPageStructureException(url=url)

    if new_price == old_price:
        np = [int(part) for part in new_price.split('.')]
        default_price = Price(np[0], np[1])
        promo_price = None
    else:
        np = [int(part) for part in new_price.split('.')]
        op = [int(part) for part in old_price.split('.')]
        default_price = Price(op[0], op[1])
        promo_price = Price(np[0], np[1])

    return default_price, promo_price


def fortuna_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s1 = html.find(id="price-new")
    s2 = html.find(id="price-old")

    if s1 is None and s2 is None:
        raise UnexpectedPageStructureException(url=url)

    if s2 is None:
        split = [int(part) for part in s1.text.split()[0].split('.')]
        default_price = Price(split[0], split[1])
        promo_price = None
    else:
        split1 = [int(part) for part in s2.text.split()[0].split('.')]
        split2 = [int(part) for part in s1.text.split()[0].split('.')]
        default_price = Price(split1[0], split1[1])
        promo_price = Price(split2[0], split2[1])

    return default_price, promo_price


def podrugka_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s1 = html.select(".price__item--current")
    s2 = html.select(".price__item--old")

    if len(s1) == len(s2) == 0:
        raise UnexpectedPageStructureException(url=url)

    if len(s2) == 0:
        default_price = Price(int(s1[0].text.split()[0]), 0)
        promo_price = None
    else:
        default_price = Price(int(s2[0].text.split()[0]), 0)
        promo_price = Price(int(s1[0].text.split()[0]), 0)

    return default_price, promo_price


def ulybka_radugi_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s1 = html.select(".new-price")
    s2 = html.select(".price-offline__old-price")

    if len(s1) == len(s2) == 0:
        raise UnexpectedPageStructureException(url=url)

    if len(s2) == 0:
        default_price = Price(int(s1[0].text.split()[0]), 0)
        promo_price = None
    else:
        default_price = Price(int(s2[0].text.split()[0]), 0)
        promo_price = Price(int(s1[0].text.split()[0]), 0)

    return default_price, promo_price


def novex_parser(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        raise RequestException(url=url)

    html = BeautifulSoup(request.content, "html.parser")
    s = html.select(".price")

    if len(s) == 0:
        raise UnexpectedPageStructureException(url=url)

    if len(s) == 1:
        s1 = [int(s[0].contents[0].text), int(s[0].contents[1].text)]
        default_price = Price(s1[0], s1[1])
        promo_price = None
    else:
        s1 = [int(s[0].contents[0].text), int(s[0].contents[1].text)]
        s2 = [int(s[1].contents[0].text), int(s[1].contents[1].text)]
        price1 = Price(s1[0], s1[1])
        price2 = Price(s2[0], s2[1])

        if len(s[0].attrs['class']) == 2:
            default_price = price1
            promo_price = price2
        else:
            default_price = price2
            promo_price = price1

    return default_price, promo_price
