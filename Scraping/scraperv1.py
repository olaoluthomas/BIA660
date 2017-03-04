import mechanize, cookielib, bs4

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
# br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
br.open('http://stackoverflow.com')
for f in br.forms():
    print f
br.select_form(nr=0)
br.form["q"] = 'python'
br.submit()

links = [l for l in br.links(url_regex="question-hyperlink")]
# soup = bs4.BeautifulSoup(req, 'xml')
# for l in br.links(url_regex='/questions/'):
    # print l
2+2