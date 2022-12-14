# Generated by Django 4.1.1 on 2022-09-15 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_order_items'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.BigIntegerField(verbose_name='Цена')),
                ('currency', models.CharField(max_length=3, verbose_name='Волюта')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
            },
        ),
    ]
