import re
import urllib.parse
import urllib.request

import lxml.html
import timeout_decorator

export_text = 'organizations.txt'
start_url = 'https://dszn.ru/department/subordinate'


def main():
    get_page(start_url)


def get_page(url):
    page = download_page(url)
    extract_links(page)


@timeout_decorator.timeout(35)
def download_page(url):
    req = urllib.request.Request(url=url)
    handler = urllib.request.urlopen(req, timeout=30)
    page = handler.read().decode('utf-8')
    return page


def extract_links(page):
    doc = lxml.html.document_fromstring(page)
    links = doc.xpath('//div[@class = "item-wrap"]/a[contains(@href, "/department/subordinate/")]')
    for l in links:
        try:
            href = l.attrib['href']
            href = f"https://dszn.ru/{href}"
            get_department(href)
        except Exception as e:
            print(e)


def get_department(url):
    page = download_page(url)
    doc = lxml.html.document_fromstring(page)
    name = get_first_element(doc, "//h1")
    address = get_first_element(doc, "//label[. = 'Адрес:']/following-sibling::div")
    metro = get_first_element(doc, "//label[. = 'Метро:']/following-sibling::div")
    first_tel = get_first_element(doc, "//label[. = 'Cправочный телефон:']/following-sibling::div")
    second_tel = get_first_element(doc, "//label[. = 'Телефон «горячей линии»:']/following-sibling::div")
    email = get_first_element(doc, "//label[. = 'E-mail:']/following-sibling::div")
    zone = get_first_element(doc, "//label[. = 'Зона ответственности:']/following-sibling::div")
    site = get_first_element(doc, "//label[. = 'Сайт:']/following-sibling::div")
    rasp = get_week(doc)
    own = get_owner(doc)
    with open(export_text, 'a') as f:
        f.write(f"{name}\t{address}\t{metro}\t{first_tel}\t{second_tel}\t{email}\t{zone}\t{site}\t{rasp}\t{own}\n")


def get_first_element(doc, xpath):
    res = doc.xpath(xpath)
    if len(res) > 0:
        return res[0].text_content().strip(' \t\n')
    return ""


def get_week(doc):
    res_string = ""
    res = doc.xpath("//div[@class = 'soc-center__table']/div[@class = 'soc-center__row hide']")
    for r in res:
        day_of_week = get_first_element(r, ".//div[@class = 'soc-center__col2']")
        rasp = get_first_element(r, ".//div[@class = 'soc-center__col3']")
        ss = f"{day_of_week} {rasp}"
        ss = re.sub(r'\s+', " ", ss)
        res_string += f"{ss};"
    return res_string


def get_owner(doc):
    res_string = ""
    res = doc.xpath("//div[@class = 'inf-panel']/div[@class = 'inf-panel__cont']")
    for r in res:
        name = get_first_element(r, ".//div[1]")
        d = get_first_element(r, ".//div[2]")
        t = get_first_element(r, ".//div[3]")
        ss = f"{name}, {d}, {t}"
        ss = re.sub(r'\s+', " ", ss)
        res_string += f"{ss};"
    return res_string


if __name__ == "__main__":
    main()
