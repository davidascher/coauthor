from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

PAD_NAME = '(?P<name>[A-Za-z\-0-9]+)'
SLUG = '(?P<slug>[A-Za-z\-0-9]+)'
MAYBE_PAD_EXT = '(?P<ext>\.(css|js|html|txt))?'
MAYBE_REV = '(/rev\.(?P<rev>[0-9]+))?'

RENDER_PAD = '%s%s%s' % (PAD_NAME, MAYBE_PAD_EXT, MAYBE_REV)

urlpatterns = patterns('coauthor.views',
    url(r'^$', 'index', name='coauthor-index'),
    url(r'^signout/$', 'signout', name='coauthor-signout'),
    url(r'^profile/$', 'profile_edit', name='coauthor-profile-edit'),
    url(r'^profile_save/$', 'profile_save', name='coauthor-profile-save'),
    # url(r'^/static/%s$', 'cheapstatic'),
    # (r'^%s$' % RENDER_PAD, 'add_trailing_slash'),
    # url(r'^%s\/$' % RENDER_PAD, 'render_pad', name='render-pad'),
    # url(r'^%s\/edit$' % PAD_NAME, 'edit_pad', name='edit-pad'),
    url(r'^author/%s\/%s\/$' % (SLUG, PAD_NAME), 'edit_pad', name='edit-pad'),
    url(r'^read/%s\/%s\/$' % (SLUG, PAD_NAME), 'read_pad', name='read-pad'),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
# ... the rest of your URLconf goes here ...
# import sys
# print >>sys.stderr, "XXX", staticfiles_urlpatterns()
# raise NameError("patterns: " + str(staticfiles_urlpatterns()))
# raise NameError("patterns: " + str(staticfiles_urlpatterns()))
urlpatterns += staticfiles_urlpatterns()
