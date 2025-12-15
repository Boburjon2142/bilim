from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.translation import get_language
from django.conf import settings

from .models import Book, Category, Author, Banner, FeaturedCategory
from .cache_keys import (
    language_codes,
    home_top_categories_key,
    home_featured_authors_key,
    home_banners_key,
    home_featured_cfgs_key,
    home_featured_books_key,
    home_best_selling_key,
    home_new_books_key,
    home_recommended_key,
    best_selling_list_key,
    recommended_list_key,
    categories_top_key,
    nav_categories_key,
)


def _invalidate_keys(keys):
    """Delete multiple cache keys if they exist."""
    cache.delete_many([k for k in keys if k])


def _home_featured_books_keys_for_all_languages():
    """
    Return keys for featured book strips (by category/limit) across languages.
    This reloads FeaturedCategory list to keep invalidation precise instead of clearing all cache.
    """
    keys = []
    langs = language_codes()
    cfgs = FeaturedCategory.objects.filter(is_active=True)
    for cfg in cfgs:
        limit = cfg.limit or 10
        for lang in langs:
            keys.append(home_featured_books_key(cfg.category_id, limit, lang))
    return keys


@receiver([post_save, post_delete], sender=Category)
def invalidate_category_caches(sender, instance, **kwargs):
    """
    Category changes impact nav menu, category listings, and home top categories.
    We clear only those keys so pages refresh immediately; TTL alone would delay updates.
    """
    keys = []
    for lang in language_codes():
        keys += [
            nav_categories_key(lang),
            categories_top_key(lang),
            home_top_categories_key(lang),
        ]
    _invalidate_keys(keys)


@receiver([post_save, post_delete], sender=Author)
def invalidate_author_caches(sender, instance, **kwargs):
    """
    Author changes affect featured authors on the home page.
    """
    keys = [home_featured_authors_key(lang) for lang in language_codes()]
    _invalidate_keys(keys)


@receiver([post_save, post_delete], sender=Banner)
def invalidate_banner_caches(sender, instance, **kwargs):
    """
    Banners appear on the home hero; invalidate to show new/removed banners instantly.
    """
    keys = [home_banners_key(lang) for lang in language_codes()]
    _invalidate_keys(keys)


@receiver([post_save, post_delete], sender=FeaturedCategory)
def invalidate_featured_category_caches(sender, instance, **kwargs):
    """
    Featured category config drives home sections; invalidate cfgs and their book strips.
    """
    keys = []
    for lang in language_codes():
        keys.append(home_featured_cfgs_key(lang))
    keys += _home_featured_books_keys_for_all_languages()
    _invalidate_keys(keys)


@receiver([post_save, post_delete], sender=Book)
def invalidate_book_caches(sender, instance, **kwargs):
    """
    Book changes affect multiple public pages (home lists, bestsellers, recommended, category strips).
    Invalidate targeted keys instead of clearing the whole cache.
    """
    langs = language_codes()
    keys = []
    for lang in langs:
        keys += [
            home_best_selling_key(lang),
            home_new_books_key(lang),
            home_recommended_key(lang),
            best_selling_list_key(lang),
            recommended_list_key(lang),
        ]
        # Featured strips for this book's category (limit varies per config)
        cfgs = FeaturedCategory.objects.filter(is_active=True, category_id=instance.category_id)
        for cfg in cfgs:
            limit = cfg.limit or 10
            keys.append(home_featured_books_key(cfg.category_id, limit, lang))
    _invalidate_keys(keys)
