from django.core.management.base import BaseCommand, CommandError

import os
import shutil


class Command(BaseCommand):
    help = 'Create a new set of template for a given notification key. Need a source template. Syntaxe: new_key base_key'

    def add_arguments(self, parser):
        parser.add_argument('new_template', type=str)
        parser.add_argument('base_template', type=str)

    def handle(self, new_template, base_template, *args, **options):

        new_key = '{}.html'.format(new_template)
        base_key = '{}.html'.format(base_template)

        BASE_PATH = 'notifications/templates/notifications/species/'

        for sub_path in ('center/buttons/', 'center/message/', 'mails/', ''):

            source_path = os.path.join(BASE_PATH, sub_path, base_key)
            dest_path = os.path.join(BASE_PATH, sub_path, new_key)

            if not os.path.isfile(source_path):
                print "Source file {} doesn't exists !".format(source_path)
            elif os.path.isfile(dest_path):
                print "Destination file {} already exists !".format(dest_path)
            else:
                print "{} -> {}".format(source_path, dest_path)
                shutil.copyfile(source_path, dest_path)
