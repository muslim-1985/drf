# Generated by Django 2.2 on 2019-06-14 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telegramm_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='botmessagefiles',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='telegramm_bot.BotUserMessage'),
        ),
    ]
