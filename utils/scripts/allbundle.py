#!/usr/bin/python
import os
import sys

CMDS = {
    0: ('restart nodemix_api', '/srv/nodemix_api/scripts/runfcgi.sh'),
    1: ('restart nginx', 'service nginx restart'),
    2: ('update awstats-pages', '/usr/local/awstats/tools/awstats_buildstaticpages.pl \
            -update -config=/srv/awstats/awstats.nodemix_api.conf \
            -dir=/srv/awstats/nodemix_api.html -lang=cn \
            -awstatsprog=/usr/local/awstats/wwwroot/cgi-bin/awstats.pl'),
    3: ('', ''),
    4: ('', ''),
    5: ('', ''),
    6: ('', '')
}

if '__main__'  == __name__:
    print 'Type in number to execude following commands: \n'
    for i in CMDS.keys():
        print '\t%d\t%s\t>%s' % (i, CMDS[i][0], CMDS[i][1])

    o = raw_input()
    try:
        o = int(o)
        cmd = CMDS[o][1]
    except ValueError:
        print 'Bad Input'
        sys.exit()
    except KeyError:
        print 'Command Index Out Of Range'
        sys.exit()

    print cmd
    result = os.popen(cmd)
    print result.read()
    print 'done'
