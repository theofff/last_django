node {
   stage ('Full_build') {
           sshagent(['b2390935-2bca-4e61-a7e1-2410de6a8bfc']) {
              sh """#!/bin/bash
              user='ssh-guillaume-fixe'
              host='10.132.0.21'
              urlrepo='https://github.com/theofff/last_django.git'
              folder=\$(echo  \$urlrepo | cut -d '/' -f 5 | cut -d '.' -f 1)
              imagename='concarneau:5002/django_concarneau'
              image=\$(echo \"\$imagename\" | cut -d '/' -f 2)
              latest=\$(ssh \$user@\$host \"ls /var/lib/docker/volumes/registry_docker_registry_data/_data/docker/registry/v2/repositories/\"\$image\"/_manifests/tags/ | sort -n | tail -n 1\")
              tagto=\$(bc -l <<< \"scale=1; \$latest+0.1\")
              ssh \$user@\$host "
              git clone \$urlrepo
              docker build -t \$imagename:\$tagto \$folder
              docker push \$imagename:\$tagto
              
              sudo kubectl apply -f deployment.yml
              rm -rf \$folder
              "
              """
        }
    }
}
