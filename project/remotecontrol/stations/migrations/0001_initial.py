# Generated by Django 4.1.3 on 2022-11-21 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Название станции')),
                ('status', models.CharField(choices=[('running', 'исправная'), ('broken', 'неисправна')], default='running', max_length=10, verbose_name='Статус')),
                ('create_data', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания станции')),
                ('broken_data', models.DateTimeField(default=None, verbose_name='Дата поломки станции')),
            ],
        ),
        migrations.CreateModel(
            name='Directive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axis', models.CharField(choices=[('x', 'x'), ('y', 'y'), ('z', 'z')], max_length=1, verbose_name='Направление')),
                ('distance', models.BigIntegerField(verbose_name='Дистанция')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directives', to='stations.station')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='directives', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.BigIntegerField(default=100)),
                ('y', models.BigIntegerField(default=100)),
                ('z', models.BigIntegerField(default=100)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='stations.station', verbose_name='Станция')),
            ],
        ),
    ]