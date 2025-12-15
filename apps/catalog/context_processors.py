from django.core.cache import cache
from django.utils.translation import get_language
from .models import Category
from .cache_keys import nav_categories_key


def categories(request):
    # Shared navigation categories; safe to cache because menu is identical for all users.
    lang = get_language()
    nav_categories = cache.get_or_set(
        nav_categories_key(lang),
        lambda: list(Category.objects.all()),
        60 * 60,  # 1 hour; invalidate manually on category edits or wait TTL
    )
    return {"nav_categories": nav_categories}
