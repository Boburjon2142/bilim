from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog", "0008_merge_20251204_1149"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255, verbose_name="F.I.Sh")),
                ("phone", models.CharField(max_length=50, unique=True, verbose_name="Telefon")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("tags", models.CharField(blank=True, max_length=255, verbose_name="Teglar")),
                ("notes", models.TextField(blank=True, verbose_name="Izoh")),
                ("is_vip", models.BooleanField(default=False, verbose_name="VIP")),
                ("is_problem", models.BooleanField(default=False, verbose_name="Muammo bo‘lgan")),
                ("total_spent", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Umumiy sarf")),
                ("orders_count", models.PositiveIntegerField(default=0, verbose_name="Buyurtmalar soni")),
                ("last_order_at", models.DateTimeField(blank=True, null=True, verbose_name="Oxirgi faollik")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Mijoz",
                "verbose_name_plural": "Mijozlar",
                "ordering": ["-last_order_at", "full_name"],
            },
        ),
        migrations.CreateModel(
            name="Courier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="F.I.Sh")),
                ("phone", models.CharField(blank=True, max_length=50, verbose_name="Telefon")),
                ("telegram_username", models.CharField(blank=True, max_length=100, verbose_name="Telegram")),
                ("telegram_id", models.CharField(blank=True, max_length=64, verbose_name="Telegram ID")),
                ("is_active", models.BooleanField(default=True, verbose_name="Faol")),
                ("last_active_at", models.DateTimeField(blank=True, null=True, verbose_name="Oxirgi faollik")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Kuryer",
                "verbose_name_plural": "Kuryerlar",
                "ordering": ["-is_active", "name"],
            },
        ),
        migrations.CreateModel(
            name="InventoryLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("delta", models.IntegerField(verbose_name="O‘zgarish")),
                (
                    "reason",
                    models.CharField(
                        choices=[("sale", "Sotuv"), ("restock", "To‘ldirish"), ("adjust", "Tuzatish"), ("cancel", "Bekor qilish")],
                        max_length=20,
                        verbose_name="Sabab",
                    ),
                ),
                ("note", models.CharField(blank=True, max_length=255, verbose_name="Izoh")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="inventory_logs", to="catalog.book"),
                ),
            ],
            options={
                "verbose_name": "Ombor yozuvi",
                "verbose_name_plural": "Ombor yozuvlari",
                "ordering": ["-created_at"],
            },
        ),
    ]
