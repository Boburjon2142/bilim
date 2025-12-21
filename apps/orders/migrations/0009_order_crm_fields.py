from django.db import migrations, models


def migrate_statuses(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.filter(status="accepted").update(status="paid")
    Order.objects.filter(status="finished").update(status="closed")


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0008_deliverysettings_shop_location_link"),
        ("crm", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Yangi"),
                    ("paid", "To‘langan"),
                    ("assigned", "Kuryerga biriktirilgan"),
                    ("delivering", "Yetkazilmoqda"),
                    ("closed", "Yopilgan"),
                    ("canceled", "Bekor qilingan"),
                ],
                default="new",
                max_length=20,
                verbose_name="Holat",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="order_source",
            field=models.CharField(
                choices=[("online", "Online"), ("pos", "Do‘kon (POS)")],
                default="online",
                max_length=20,
                verbose_name="Kanal",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="orders",
                to="crm.customer",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="courier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="orders",
                to="crm.courier",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="paid_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="To‘langan vaqti"),
        ),
        migrations.AddField(
            model_name="order",
            name="assigned_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Biriktirilgan vaqti"),
        ),
        migrations.AddField(
            model_name="order",
            name="delivered_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Yetkazildi vaqti"),
        ),
        migrations.AddField(
            model_name="order",
            name="canceled_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Bekor qilingan vaqti"),
        ),
        migrations.RunPython(migrate_statuses, migrations.RunPython.noop),
    ]
