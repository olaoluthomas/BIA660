import mechanize
import cookielib
import bs4

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
# br.set_debug_http(True)
# br.set_debug_redirects(True)
# br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]

# Open the test 'site
r = br.open('https://stackoverflow.com/')
html = r.read()

# Show the source
#print html
# or
# print br.response().read()

# Show the html title
# print br.title()

# Show the response headers
# print r.info()
# or
# print br.response().info()

# Show the available forms
# for f in br.forms():
#    print f

# Select the first (index zero) form
# br.select_form (nr=0)

# Let's search
br.form['q']='python magic methods'
br.submit()
print br.response().read()

# Looking at some results in link format
# for l in br.links(url_regex='stockrt'):
#    print l
