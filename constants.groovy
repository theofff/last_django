import groovy.transform.Field

@Field
def user = 'ssh-guillaume-fixe'
@Field
def host = '10.132.0.21'
@Field
def urlrepo = 'https://github.com/theofff/last_django.git'
@Field
def folder = "\$(echo  \$urlrepo | cut -d '/' -f 5 | cut -d '.' -f 1)"
@Field
def imagename = 'concarneau:5002/django_concarneau'
@Field
def image = "\$(echo \"\$imagename\" | cut -d '/' -f 2)"
@Field
def latest = "\$(ssh \$user@\$host \"ls /var/lib/docker/volumes/ssh-guillaume-fixe_registry_data/_data/docker/registry/v2/repositories/\"\$image\"/_manifests/tags/ | sort -n | tail -n 1\")"
@Field
def tagto = "\$(bc -l <<< \"scale=1; \$latest+0.1\")"

return this;
