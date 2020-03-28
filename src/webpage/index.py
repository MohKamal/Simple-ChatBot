# coding: utf-8

import cgi 

#form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

#print(form.getvalue("name"))

html = ""
with open('webpage.html', 'r') as f:
    html = f.read()

print(html)