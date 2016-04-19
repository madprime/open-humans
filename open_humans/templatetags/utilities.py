import logging
import os
import re

import bleach
import markdown as markdown_library

from django import template
from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.loader_tags import do_include
from django.utils.safestring import mark_safe

from common.utils import full_url as full_url_method

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def source_to_name(source):
    """
    Given 'go_viral', return 'GoViral'
    """
    try:
        return apps.get_app_config(source).verbose_name
    except:  # pylint: disable=bare-except
        return source


@register.filter
def lookup(dictionary, key):
    """
    Get a dictionary value by key within a template.
    """
    return dictionary.get(key)


class TryIncludeNode(template.Node):
    """
    A Node that instantiates an IncludeNode but wraps its render() in a
    try/except in case the template doesn't exist.
    """
    def __init__(self, parser, token):
        self.include_node = do_include(parser, token)

    def render(self, context):
        try:
            return self.include_node.render(context)
        except template.TemplateDoesNotExist:
            return ''


@register.tag
def try_include(parser, token):
    """
    Include the specified template but only if it exists.
    """
    return TryIncludeNode(parser, token)


@register.filter
def markdown(value):
    """
    Translate markdown to a safe subset of HTML.
    """
    cleaned = bleach.clean(markdown_library.markdown(value),
                           tags=bleach.ALLOWED_TAGS +
                           ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    linkified = bleach.linkify(cleaned)

    return mark_safe(linkified)


@register.simple_tag(takes_context=True)
def next_page(context):
    """
    Get the next page for signup or login.

    The query string takes priority over the template variable and the default
    is an empty string.
    """
    if 'next' in context.request.GET:
        return context.request.GET['next']

    if 'next' in context.request.POST:
        return context.request.POST['next']

    if 'next' in context:
        return context['next']

    return ''


def slugify_url(url):
    """
    Turn '/study/connect_me/' into 'study-connect-me'.
    """
    return (url
            .lower()
            .strip('/')
            .replace(':', '-')
            .replace('/', '-')
            .replace('_', '-'))


def script_if_exists(slug):
    """
    Return a script tag if the given slug path exists.
    """
    fs_path = os.path.join(settings.BASE_DIR,
                           'build/js/{}.js'.format(slug))

    if os.path.exists(fs_path):
        return '<script src="{}js/{}.js"></script>'.format(
            settings.STATIC_URL, slug)


@register.simple_tag(takes_context=True)
def page_bundle(context):
    """
    Get the bundle path for a given page, first trying the view name and then
    the URL slug.
    """
    # for example, /study/connect/abc/ has a view_name of studies:connect
    name = slugify_url(context.request.resolver_match.view_name)
    script = script_if_exists(name)

    if script:
        return mark_safe(script)

    path = slugify_url(context.request.path)
    script = script_if_exists(path)

    if script:
        return mark_safe(script)

    if settings.DEBUG:
        return mark_safe('<!-- DEBUG: not found: "{}", "{}" -->'
                         .format(name, path))

    return ''


@register.simple_tag(takes_context=True)
def page_body_id(context):
    """
    Get the CSS class for a given page.
    """
    path = slugify_url(context.request.path)

    if not path:
        path = 'home'

    return 'page-{}'.format(path)


@register.simple_tag(takes_context=True)
def page_body_class(context):
    """
    Get the CSS class for a given resolved URL.
    """
    return 'url-{}'.format(context.request.resolver_match.url_name)


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    """
    Return 'active' if the given URL or pattern is active.
    """
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname

    path = context.request.path

    if re.search(pattern, path):
        return 'active'

    return ''


@register.simple_tag()
def badge(badge_object):
    """
    Return HTML for a badge.
    """
    if not (badge_object['url'].startswith('/') or
            badge_object['url'].startswith('http')):
        badge_object['static_url'] = static(badge_object['url'])
    else:
        badge_object['static_url'] = badge_object['url']

    if badge_object['url'] == 'direct-sharing/images/badge.png':
        return mark_safe(
            """<div class="oh-badge-default">
                 <img class="oh-badge" src="{static_url}">
                 <div class="oh-badge-name">{name}</div>
               </div>""".format(**badge_object))

    return mark_safe(
        '<img class="oh-badge" src="{static_url}" alt="{name}" title="{name}">'
        .format(**badge_object))


@register.filter
def join_and(value):
    """
    Given a list of strings, format them with commas and spaces, but
    with 'and' at the end.

    >>> join_and(['apples', 'oranges', 'pears'])
    "apples, oranges, and pears"
    """
    # convert numbers to strings
    value = [str(item) for item in value]

    if len(value) == 1:
        return value[0]

    if len(value) == 2:
        return '{} and {}'.format(value[0], value[1])

    # join all but the last element
    all_but_last = ', '.join(value[:-1])
    return '{}, and {}'.format(all_but_last, value[-1])


@register.filter
def full_url(value):
    return full_url_method(value)
