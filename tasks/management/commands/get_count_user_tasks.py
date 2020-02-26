# coding: utf-8
from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = u"Display all tasks completed in the last 'days' days (default=3 days)"

    # def add_arguments(self, parser):
    #     parser.add_argument('--days', dest='days', type=int, default=3)

    def handle(self, *args, **options):
        main_user = ''
        tasks_count = 0
        all_users = dict()
        for user in User.objects.all():
            for task in user.tasks.all():
                if user == main_user:
                    tasks_count = 5
                else:
                    all_users[main_user] = tasks_count
                    main_user = user.username
                    tasks_count = 0
        print(all_users)

