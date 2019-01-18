#!/usr/bin/env bash

# the apache user needs write access to this directory
chown apache /var/lib/pulp
chown apache /var/lib/pulp/celery

# copy the basic directory structure if it isn't already present.
if [ ! -e /var/lib/pulp/content ]
then
    cp -a /var/local/var_lib_pulp/* /var/lib/pulp/
fi
if [ ! -e /etc/pulp/server.conf ]
then
    cp -a /var/local/etc_pulp/* /etc/pulp/
fi
#if [ ! -e /etc/pki/pulp/ca.crt ]
#then
#    cp -a /var/local/etc_pki_pulp/* /etc/pki/pulp/
#fi

#ssl generate certs

country=US
state=Arizona
locality=Phoenix
organization=common
organizationalunit=IT
email=pulp-list@redhat.com
commonname=*.redhat

openssl req \
    -new \
    -newkey rsa:4096 \
    -days 3650 \
    -nodes \
    -x509 \
    -subj "/C=$country/ST=$state/L=$locality/O=$organization/OU=$organizationalunit/CN=$commonname/emailAddress=$email" \
    -keyout /etc/pki/pulp/ca.key \
    -out /etc/pki/pulp/ca.crt

# a hacky way of waiting until mongo is done initializing itself. Eventually
# (probably 2.5.1) pulp-manage-db will do this on its own in a reasonable way.
# It waits currently, but quickly backs off to a poll interval of 32 seconds,
# which is undesirable.
until echo "" | nc db 27017 2>/dev/null
do
    echo "waiting for mongodb"
    sleep 1
done

runuser -u apache pulp-manage-db
