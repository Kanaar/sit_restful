# Generated by Django 4.0 on 2021-12-30 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('amount_of_tickets', models.IntegerField()),
                ('pref_aisle', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('is_front', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('is_aisle', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_booked', models.BooleanField(default=False)),
                ('rank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_seating.rank')),
                ('row', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_seating.row')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('position', models.CharField(choices=[('l', 'left'), ('c', 'centre'), ('r', 'right'), ('ll', 'outer left'), ('rr', 'outer right')], default='c', max_length=50)),
                ('is_balcony', models.BooleanField(default=False)),
                ('is_loge', models.BooleanField(default=False)),
                ('is_curved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='api_seating.order')),
                ('seat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_seating.seat')),
            ],
        ),
        migrations.AddField(
            model_name='row',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_seating.section'),
        ),
        migrations.AddField(
            model_name='order',
            name='rank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_seating.rank'),
        ),
        migrations.AddField(
            model_name='order',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_seating.section'),
        ),
    ]
