import gettext as gettext_module
import os
import rrd_xml_parser
from contextlib import ContextDecorator
from threading import local

_LANGS = dict(
    ru=gettext_module.translation(domain='rrd_xml_parser',
                                  localedir=os.path.join(os.path.dirname(rrd_xml_parser.__file__), 'locale'),
                                  languages=['ru'],
                                  codeset='utf-8',
                                  fallback=True
                                  ),
    en=gettext_module.translation(domain='rrd_xml_parser',
                                  localedir=os.path.join(os.path.dirname(rrd_xml_parser.__file__), 'locale'),
                                  languages=['en'],
                                  codeset='utf-8',
                                  fallback=True
                                  )
)

_active = local()

DEFAULT_LANGUAGE_CODE = 'en'

_default = None


def to_locale(language):
    language = language.lower()
    parts = language.split('-')
    try:
        country = parts[1]
    except IndexError:
        return language
    else:
        # A language with > 2 characters after the dash only has its first
        # character after the dash capitalized; e.g. sr-latn becomes sr_Latn.
        # A language with 2 characters after the dash has both characters
        # capitalized; e.g. en-us becomes en_US.
        parts[1] = country.title() if len(country) > 2 else country.upper()
    return parts[0] + '_' + '-'.join(parts[1:])


def to_language(locale):
    """Turn a locale name (en_US) into a language name (en-us)."""
    p = locale.find('_')
    if p >= 0:
        return locale[:p].lower() + '-' + locale[p + 1:].lower()
    else:
        return locale.lower()


def translation(language):
    """
    Return a translation object in the default 'django' domain.
    """
    global _LANGS
    lang = to_locale(to_language(language))
    if lang not in _LANGS:
        domain = os.path.basename(os.path.dirname(rrd_xml_parser.__file__))
        languages = [to_locale(language)]
        localedir = os.path.join(os.path.dirname(rrd_xml_parser.__file__), 'locale')
        _LANGS[lang] = gettext_module.translation(domain=domain, localedir=localedir, languages=languages,
                                                  codeset='utf-8')
    return _LANGS[lang]


def activate(language):
    if not language:
        return
    _active.value = translation(language)


def deactivate():
    if hasattr(_active, "value"):
        del _active.value


def deactivate_all():
    """
    Make the active translation object a NullTranslations() instance. This is
    useful when we want delayed translations to appear as the original string
    for some reason.
    """
    _active.value = gettext_module.NullTranslations()
    _active.value.to_language = lambda *args: None


def gettext(message):
    """
    Translate the 'message' string. It uses the current thread to find the
    translation object to use. If no current translation is activated, the
    message will be run through the default translation object.
    """
    global _default

    eol_message = message.replace('\r\n', '\n').replace('\r', '\n')

    if len(eol_message) == 0:
        result = type(message)("")
    else:
        _default = _default or translation(DEFAULT_LANGUAGE_CODE)
        translation_object = getattr(_active, "value", _default)

        result = translation_object.gettext(eol_message)
    return result


def get_language():
    """Return the currently selected language."""
    t = getattr(_active, "value", None)
    if t is not None:
        try:
            return t.to_language()
        except AttributeError:
            pass
    # If we don't have a real translation object, assume it's the default language.
    return DEFAULT_LANGUAGE_CODE


class override(ContextDecorator):
    def __init__(self, language, deactivate=False):
        self.language = language
        self.deactivate = deactivate

    def __enter__(self):
        self.old_language = get_language()
        if self.language is not None:
            activate(self.language)
        else:
            deactivate_all()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.old_language is None:
            deactivate_all()
        elif self.deactivate:
            deactivate()
        else:
            activate(self.old_language)
