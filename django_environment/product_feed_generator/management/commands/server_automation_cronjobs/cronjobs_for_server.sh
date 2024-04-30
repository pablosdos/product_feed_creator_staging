# Test Staging Server – testing; every minute
*/1 * * * * cd /home/datafeeds/django_environment && pipenv run python manage.py serverkast_refresh >> /home/datafeeds/django_environment/product_feed_generator/management/commands/server_automation_cronjobs/error-log.txt 2>&1

# Staging Server – usage, latest; every morning at 4; check and send today emails
0 4 * * * cd /home/datafeeds/django_environment && pipenv run python manage.py serverkast_refresh >> /home/datafeeds/django_environment/product_feed_generator/management/commands/server_automation_cronjobs/error-log.txt 2>&1
0 4 * * * cd /home/datafeeds/django_environment && pipenv run python manage.py topsystems_refresh >> /home/datafeeds/django_environment/product_feed_generator/management/commands/server_automation_cronjobs/error-log.txt 2>&1