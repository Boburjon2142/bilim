from django.conf import settings
from django.utils.translation import get_language


def language_codes():
    """
    Return all language codes we should invalidate for.
    Falls back to default language when LANGUAGES is not defined.
    """
    if getattr(settings, "LANGUAGES", None):
        return [code for code, _ in settings.LANGUAGES]
    return [getattr(settings, "LANGUAGE_CODE", "default")]


def current_language():
    return get_language() or getattr(settings, "LANGUAGE_CODE", "default")


def make_key(base: str, *parts, lang: str | None = None) -> str:
    code = lang or current_language()
    suffix = ":".join(str(p) for p in parts if p is not None)
    return f"{base}:{suffix}:{code}" if suffix else f"{base}:{code}"


# Home page keys
def home_top_categories_key(lang=None):
    return make_key("home:top_categories", lang=lang)


def home_featured_authors_key(lang=None):
    return make_key("home:featured_authors", lang=lang)


def home_banners_key(lang=None):
    return make_key("home:banners", lang=lang)


def home_featured_cfgs_key(lang=None):
    return make_key("home:featured_cfgs", lang=lang)


def home_featured_books_key(category_id: int, limit: int, lang=None):
    return make_key("home:featured_books", category_id, limit, lang=lang)


def home_best_selling_key(lang=None):
    return make_key("home:best_selling_top6", lang=lang)


def home_new_books_key(lang=None):
    return make_key("home:new_books_top6", lang=lang)


def home_recommended_key(lang=None):
    return make_key("home:recommended_top6", lang=lang)


# Listing pages
def best_selling_list_key(lang=None):
    return make_key("books:best_selling:list", lang=lang)


def recommended_list_key(lang=None):
    return make_key("books:recommended:list", lang=lang)


def categories_top_key(lang=None):
    return make_key("categories:list:top", lang=lang)


def nav_categories_key(lang=None):
    return make_key("nav:categories:all", lang=lang)
