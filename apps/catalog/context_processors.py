from django.core.cache import cache
from .models import Category


def categories(request):
    # Shared navigation categories; safe to cache because menu is identical for all users.
    nav_categories = cache.get_or_set(
        "nav:categories:all",
        lambda: list(Category.objects.all()),
        60 * 60,  # 1 hour; invalidate manually on category edits or wait TTL
    )
    return {"nav_categories": nav_categories}
