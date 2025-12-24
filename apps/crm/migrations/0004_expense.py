from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0003_customer_discount"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Sarlavha")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Chiqim")),
                ("spent_on", models.DateField(default=django.utils.timezone.localdate, verbose_name="Sana")),
                ("note", models.TextField(blank=True, verbose_name="Izoh")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Chiqim",
                "verbose_name_plural": "Chiqimlar",
                "ordering": ["-spent_on", "-created_at"],
            },
        ),
    ]
