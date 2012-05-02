# Create your views here.

import mimetypes

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from coauthor.models import Pad

from etherpad import etherpad
import markdown2
import re, time
import jingo
from django.contrib import auth

def ctx(request, options=None):
    if not options:
        options = {}
    options.update({
        'request': request,
        'HTMLPAD_ROOT': settings.HTMLPAD_ROOT,
        'STATIC_URL': settings.STATIC_URL
    })
    return options

def index(request):
    user = request.user
    if user.is_anonymous() or user.userprofile.slug:
        return jingo.render(request, 'coauthor/index.html',
            {'etherpad': settings.ETHERPAD_HOST})
    else:
        return redirect(reverse('coauthor-profile-edit'))


def profile_edit(request):
    return jingo.render(request, 'coauthor/profile.html')

def profile_save(request):
    user = request.user
    user.userprofile.slug = request.POST['slug']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()
    print "USER SAVED"
    user.userprofile.save()
    return redirect(reverse('coauthor-index'))

def signout(request):
    """Sign the user out, destroying their session."""
    auth.logout(request)
    return redirect('/')

def add_trailing_slash(request, **kwargs):
    return redirect('%s/' % request.path)

def read_pad(request, slug, name):
    user = request.user
    group =  Group.objects.filter(name=user.email)[0]
    # if it exists, render it
    print "NAME:", name, "SLUG:", slug
    pads = Pad.objects.filter(name=name, slug=slug)
    if not pads:
        return redirect('/')
    pad = pads[0]

    # get pad body
    markdown = etherpad.getText(pad.padID)
    mymarkdown = MyMarkdown(extras=['header-ids', 'link-patterns'], link_patterns=link_patterns)
    editurl = "http://localhost:8081/author/" + slug + '/' + name

    ext = '.html'
    mimetype = '%s; charset=utf-8' % mimetypes.types_map[ext]
    frag = mymarkdown.convert(markdown)
        
    return render_to_response('coauthor/markeddown.html', 
        ctx(request, {'frag': frag,
            'editurl': editurl}))
    # return HttpResponse(html, mimetype=mimetype)


def edit_pad(request, slug, name):
    user = request.user
    assert (user.userprofile.slug == slug)
    group =  Group.objects.filter(name=user.email)[0]
    # if it exists, render it
    pads = Pad.objects.filter(name=name)
    if pads:
        pad = pads[0]
    else:
        # if it doesn't exist, create it
        padID = etherpad.createGroupPad(group.groupprofile.etherpad_group_id,
            name)
        pad = Pad(author=user,group=group,name=name,slug=slug, padID=padID)
        etherpad.setPublicStatus(padID, 'false')
        pad.save()

    url = settings.ETHERPAD_HOST + '/p/' + group.groupprofile.etherpad_group_id + '$' + pad.name
    url = "http://localhost:8081/e" + '/p/' + group.groupprofile.etherpad_group_id + '$' + pad.name
    rendered_url = "http://localhost:8081/read/" + slug + '/' + name
    validUntil = time.time() + 10000;
    sessionID = etherpad.createSession(pad.group.groupprofile.etherpad_group_id, 
        pad.author.userprofile.etherpad_author_id, validUntil)

    request.session['sessionID'] = sessionID
    return render_to_response('coauthor/edit.html', ctx(request, {
        'host': request.META['HTTP_HOST'],
        'sessionID': sessionID,
        'etherpad_url': url,
        'render_pad_url': rendered_url,
        'name': name
    }))

link_patterns = [
    (re.compile("bug\s+(\d+)", re.I), r"http://bugzilla.mozilla.org/show_bug.cgi?id=\1"),
]

class MyMarkdown(markdown2.Markdown):
    def __init__(self, *args, **kwargs):
        self._headers = [] # stack of current count for that hN header
        markdown2.Markdown.__init__(self, *args, **kwargs)
    def header_id_from_text(self, text, prefix, n):
        if n > len(self._headers):
            self._headers.append(1)
        elif n == len(self._headers):
            self._headers[-1] += 1
        else:
            # Example: n == 1, _headers = [1,3,2]  =>  _headers = [2]
            del self._headers[n:]
            self._headers[-1] += 1
        return '.'.join(map(str, self._headers))


import html2text

def render_pad(request, name, ext, rev):
    resp = etherpad.get_raw_contents(name, rev)
    # return HttpResponse(resp.read(), mimetype="text/plain")

    mymarkdown = MyMarkdown(extras=['header-ids', 'link-patterns'], link_patterns=link_patterns)

    if resp.status == 200:
        if not ext:
            ext = '.html'
        mimetype = '%s; charset=utf-8' % mimetypes.types_map[ext]
        markdown = resp.read()
        # html = resp.read()
        # markdown = html2text.html2text(html)
        frag = mymarkdown.convert(markdown)
            
        return render_to_response('coauthor/markeddown.html', 
            ctx(request, {'frag': frag,
                'htmlpadurl': 'edit'}))
        # return HttpResponse(html, mimetype=mimetype)
    elif resp.status == 404:
        return render_to_response('coauthor/404.html', ctx(request, {
            'edit_pad_url': reverse('edit-pad', kwargs={'name': name}),
            'name': name
        }))

    # TODO: Handle other cases, including etherpad timeouts,
    # server errors, etc.

def cheap_static(request, name, ext):
    data = open(name+'.'+ext).read()
    mimetype = '%s; charset=utf-8' % mimetypes.types_map[ext]
    resp = HttpResponse(data, mimetype=mimetype)
