# this is intended to talk to etherpadlite, not the original etherpad

from django.conf import settings
import requests, json, urllib

ETHERPAD_APIKEY = settings.ETHERPAD_API_KEY
ETHERPAD_HOST = settings.ETHERPAD_HOST

# PAD_TEXT_URL = "/ep/pad/export/%s/latest?format=txt"
# PAD_REV_TEXT_URL = "/ep/pad/export/%s/rev.%d?format=txt"

# protocols = dict(https=httplib.HTTPSConnection,
#                  http=httplib.HTTPConnection)
                 
# def _get_url(urlpath):
#     conn = protocols[settings.ETHERPAD_PROTOCOL](settings.ETHERPAD_HOST)
#     conn.request("GET", urlpath)
#     return conn.getresponse()

# def get_edit_url(name):
#     return '%s://%s/%s' % (settings.ETHERPAD_PROTOCOL,
#                            settings.ETHERPAD_HOST, name)

# def get_raw_contents(name, rev=None):
#     if rev:
#         urlpath = PAD_REV_TEXT_URL % (name, int(rev))
#     else:
#         urlpath = PAD_TEXT_URL % name

#     return _get_url(urlpath)



class Etherpad:
    def mkurl(self, cmd, **kw):
        kw['apikey'] = ETHERPAD_APIKEY
        arglist = urllib.urlencode(kw)
        print cmd, kw
        return ETHERPAD_HOST + '/api/1/' + cmd + '?' + arglist

    def getText(self, padID, revision=None):
        if revision is not None:
            url = self.mkurl('getText', padID=padID, revision=revision)
        else:
            url = self.mkurl('getText', padID=padID)
        r = requests.get(url)
        return json.loads(r.content)['data']['text']

    def createAuthorIfNotExistsFor(self, authorMapper):
        url = self.mkurl('createAuthorIfNotExistsFor', authorMapper=authorMapper)
        r = requests.get(url)
        return json.loads(r.content)['data']['authorID']


    def createGroupIfNotExistsFor(self, groupMapper):
        url = self.mkurl('createGroupIfNotExistsFor', groupMapper=groupMapper)
        r = requests.get(url)
        return json.loads(r.content)['data']['groupID']

    def createSession(self, groupID, authorID, validUntil):
        url = self.mkurl('createSession', groupID=groupID, authorID=authorID, validUntil=validUntil)
        retval = json.loads(requests.get(url).content)
        if (retval['code'] != 0):
            raise ValueError(retval)
        return retval['data']['sessionID']

    def setPassword(self, padID, password):
        url = self.mkurl('setPassword', padID=padID, password=password)
        r = requests.get(url)
        print r.content
        retval = json.loads(r.content)
        if retval['code'] != 0:
            raise ValueError(retval)

    def isPasswordProtected(self, padID):
        url = self.mkurl('isPasswordProtected', padID=padID)
        r = requests.get(url)
        retval = json.loads(r.content)
        if retval['code'] != 0:
            raise ValueError(retval)
        return retval['data']['isPasswordProtected']


    def setPublicStatus(self, padID, publicStatus):
        url = self.mkurl('setPublicStatus', padID=padID, publicStatus=publicStatus)
        r = requests.get(url)
        print r.content
        retval = json.loads(r.content)
        if retval['code'] != 0:
            raise ValueError(retval)

    def getPublicStatus(self, padID):
        url = self.mkurl('getPublicStatus', padID=padID)
        r = requests.get(url)
        print r.content
        retval = json.loads(r.content)
        if retval['code'] != 0:
            raise ValueError(retval)
        return retval['data']['publicStatus']

    def createPad(self, padID):
        url = self.mkurl('createPad', padID=padID)
        r = requests.get(url)
        print r.content
        retval = json.loads(r.content)
        if retval['code'] != 0:
            raise ValueError(retval)

    def createGroupPad(self, groupID, padName):
        url = self.mkurl('createGroupPad', groupID=groupID, padName=padName)
        r = requests.get(url)
        print r.content
        retval = json.loads(r.content)
        if retval['code'] != 0:
            raise ValueError(retval)
        print "RETURNING PADID of", retval['data']['padID']
        return retval['data']['padID']

    def getEditURL(self, padID):
        return ETHERPAD_HOST + '/p/' + padID


etherpad = Etherpad()

