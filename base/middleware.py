from projcube.utils.viewsbase import ApiBaseError
# NOTE ????

def StoreDebugPage(req, resp):
    import os
    import time
    import config
    page_name = ''.join(str(time.time()).split('.')) + \
                '-' + \
                '-'.join(str(req.get_full_path()).split('/'))
    page_path = os.path.join(config.LOG_ROOT,
            '%s.html' % page_name)
    page = open(page_path, 'w')
    page.write(resp.content)
    page.close()


class BaseMiddleware(object):
    #def process_request(self, req):
        #return None

    def process_exception(self, req, e):
        if isinstance(e, ApiBaseError):
            return e.get_resp()

    def process_response(self, req, resp):
        if 200 != resp.status_code and \
                req.get_full_path().find('ajax') > 0:
            StoreDebugPage(req, resp)

        return resp

