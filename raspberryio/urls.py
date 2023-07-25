from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from django_notify.urls import get_pattern as get_notify_pattern
from wiki.urls import get_pattern as get_wiki_pattern
from aggregator.feeds import CommunityAggregatorFeed, CommunityAggregatorFirehoseFeed

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),


    # RaspberryIO apps
    url(r"^$", 'raspberryio.project.views.index', name="home"),
    url(r'^users/$', 'raspberryio.userprofile.views.profile_users', name='profile-users'),
    url(r'^dashboard/$', 'raspberryio.userprofile.views.profile_dashboard', name='profile-dashboard'),
    url(r'^projects/', include('raspberryio.project.urls')),
    url(r'^accounts/', include('raspberryio.userprofile.urls')),
    url(r'^search/', include('raspberryio.search.urls')),
    url(r'^community/blogs/', include('raspberryio.aggregator.urls')),
    url(r'^community/', include('raspberryio.qanda.urls')),
    url(r'^rss/community/blogs/firehose/$', CommunityAggregatorFirehoseFeed(), name='aggregator-firehose-feed'),
    url(r'^rss/community/blogs/(?P<slug>[\w-]+)/$', CommunityAggregatorFeed(), name='aggregator-feed'),

    # django-push
    url(r'^subscriber/', include('django_push.subscriber.urls')),

    # django-activity-streams
    url('^activity/', include('actstream.urls')),

    # wiki
    url(r'^wiki/notify/', get_notify_pattern()),
    url(r'^wiki/.*_settings/', RedirectView.as_view(url='/wiki/')),
    url(r'wiki/', get_wiki_pattern()),
    # Mezzanine urls
    url(r'^', include('mezzanine.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
