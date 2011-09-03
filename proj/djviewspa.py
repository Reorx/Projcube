import re

def tup2str(tup):
    s = ''
    for i in tup:
        s += i
    return s

with open('urls.py', 'r') as fUrls:
    name_list = []

    for line, i in enumerate(fUrls):
        res = re.search('^\s+[\w\W]+views\.(?P<name>.+)\),\n', i)
        if res:
            name_list.append(res.group('name'))

    with open('views.py', 'a') as fViews:
        for i in name_list:
            func_s = ('def ', i, '(req, tpl=\'.html\'):\n',
                      '    ', 'cdic = {}\n',
                      '    ', 'return render_tpl(req, tpl, cdic)\n\n')
            fViews.write(tup2str(func_s))
