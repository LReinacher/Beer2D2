import os
import sys

def django_handler():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Interface.settings")
    from django.core.management import execute_from_command_line

    django_args = []
    django_args.append(sys.argv[0])
    django_args.append('runserver')
    django_args.append('127.0.0.1:80')
    django_args.append('--noreload')
    execute_from_command_line(django_args)


if __name__ == "__main__":
    django_handler()