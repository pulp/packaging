%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?rhel} == 5
%define pulp_admin 0
%define pulp_client_oauth 0
%define pulp_server 0
%define pulp_streamer 0
%else
%define pulp_admin 1
%define pulp_client_oauth 1
%define pulp_server 1
%define pulp_streamer 1
%endif

# Determine whether we should target Upstart or systemd for this build
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 15
%define pulp_systemd 1
%else
%define pulp_systemd 0
%endif

# Required gofer version
%global gofer_version 2.5


# ---- Pulp Platform -----------------------------------------------------------

Name: pulp
Version: 2.8.4
Release: 2%{?dist}
Summary: An application for managing software content
Group: Development/Languages
License: GPLv2+
URL:     https://github.com/pulp/pulp
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
# do not include either of these on rhel 5
%if 0%{?rhel} == 6
BuildRequires: python-sphinx10 >= 1.0.8
%endif
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 19
BuildRequires: python-sphinx >= 1.0.8
%endif
BuildRequires: rpm-python

%description
Pulp provides replication, access, and accounting for software repositories.

%prep
%autosetup -n %{name}-%{version}

%build
for directory in agent bindings client_consumer client_lib common devel
do
    pushd $directory
    %{__python} setup.py build
    popd
done

# pulp-admin build block
%if %{pulp_admin}
pushd client_admin
%{__python} setup.py build
popd
%endif # End pulp-admin build block

%if %{pulp_server}
for directory in server repoauth oid_validation nodes/common nodes/parent nodes/child nodes/extensions/admin nodes/extensions/consumer
do
    pushd $directory
    %{__python} setup.py build
    popd
done

# SELinux Configuration
cd server/selinux/server
%if 0%{?rhel} >= 6
    distver=rhel%{rhel}
%endif
%if 0%{?fedora} >= 18
    distver=fedora%{fedora}
%endif
sed -i "s/policy_module(pulp-server, [0-9]*.[0-9]*.[0-9]*)/policy_module(pulp-server, %{version})/" pulp-server.te
sed -i "s/policy_module(pulp-celery, [0-9]*.[0-9]*.[0-9]*)/policy_module(pulp-celery, %{version})/" pulp-celery.te
sed -i "s/policy_module(pulp-streamer, [0-9]*.[0-9]*.[0-9]*)/policy_module(pulp-streamer, %{version})/" pulp-streamer.te
./build.sh ${distver}
cd -
%endif # end of the pulp-server build block

# Build the pulp-streamer if enabled.
%if %{pulp_streamer}
pushd streamer
%{__python} setup.py build
popd
%endif

# build man pages if we are able
pushd docs
%if 0%{?rhel} == 6
make man SPHINXBUILD=sphinx-1.0-build
%endif
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 19
make man
%endif
popd

%install
rm -rf %{buildroot}
for directory in agent bindings client_consumer client_lib common devel
do
    pushd $directory
    %{__python} setup.py install -O1 --skip-build --root %{buildroot}
    popd
done

# Directories
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/agent
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/agent/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/consumer
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/consumer/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/gofer/plugins
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/server
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}/content
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/consumer
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/consumer/extensions
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/agent
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/agent/handlers
mkdir -p %{buildroot}/%{_var}/log/%{name}/
mkdir -p %{buildroot}/%{_bindir}
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 19
mkdir -p %{buildroot}/%{_mandir}/man1
%endif


# pulp-streamer installation
%if %{pulp_streamer}
pushd streamer
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

mkdir -p %{buildroot}/%{_var}/www/streamer/
mkdir -p %{buildroot}/%{_sysconfdir}/default/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/%{_datadir}/%{name}/wsgi

cp streamer/etc/pulp/streamer.conf %{buildroot}/%{_sysconfdir}/%{name}/streamer.conf
cp streamer/etc/httpd/conf.d/pulp_streamer.conf \
    %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp_streamer.conf
cp streamer/usr/share/pulp/wsgi/streamer.tac %{buildroot}/%{_datadir}/%{name}/wsgi/streamer.tac
cp streamer/usr/share/pulp/wsgi/streamer_auth.wsgi \
    %{buildroot}/%{_datadir}/%{name}/wsgi/streamer_auth.wsgi

# Server init scripts/unit files and environment files
%if %{pulp_systemd} == 0
cp streamer/etc/default/upstart_pulp_streamer %{buildroot}/%{_sysconfdir}/default/pulp_streamer
cp -d streamer/etc/rc.d/init.d/* %{buildroot}/%{_initddir}/
%else
cp streamer/etc/default/systemd_pulp_streamer %{buildroot}/%{_sysconfdir}/default/pulp_streamer
mkdir -p %{buildroot}/%{_usr}/lib/systemd/system/
cp streamer/usr/lib/systemd/system/* %{buildroot}/%{_usr}/lib/systemd/system/
%endif

# End of the pulp-streamer installation block
%endif


# pulp-admin installation
%if %{pulp_admin}
pushd client_admin
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/admin
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/admin/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/admin
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/admin/extensions

cp -R client_admin/etc/pulp/admin/admin.conf %{buildroot}/%{_sysconfdir}/%{name}/admin/
cp client_admin/etc/bash_completion.d/pulp-admin %{buildroot}/%{_sysconfdir}/bash_completion.d/
# pulp-admin man page (no need to fence this against el5 again)
cp docs/_build/man/pulp-admin.1 %{buildroot}/%{_mandir}/man1/
%endif # End pulp_admin installation block

# Server installation
%if %{pulp_server}
for directory in server repoauth oid_validation nodes/common nodes/parent nodes/child nodes/extensions/admin nodes/extensions/consumer
do
    pushd $directory
    %{__python} setup.py install -O1 --skip-build --root %{buildroot}
    popd
done

# These directories are specific to the server
mkdir -p %{buildroot}/%{_datadir}/pulp/wsgi
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/content/sources/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/server
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/server/plugins.conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/vhosts80
mkdir -p %{buildroot}/%{_sysconfdir}/default/
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins/types
mkdir -p %{buildroot}/%{_var}/lib/%{name}/uploads
mkdir -p %{buildroot}/%{_var}/lib/%{name}/published
mkdir -p %{buildroot}/%{_var}/lib/%{name}/static
mkdir -p %{buildroot}/%{_var}/www
mkdir -p %{buildroot}/%{_var}/cache/%{name}
mkdir -p %{buildroot}/%{_var}/run/%{name}
# These directories are used for Nodes
mkdir -p %{buildroot}/%{_var}/lib/%{name}/nodes/published/http
mkdir -p %{buildroot}/%{_var}/lib/%{name}/nodes/published/https
mkdir -p %{buildroot}/%{_var}/www/%{name}/nodes

# Configuration
cp -R server/etc/pulp/* %{buildroot}/%{_sysconfdir}/%{name}

# Apache Configuration
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
cp server/etc/httpd/conf.d/pulp_apache_24.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp.conf
%else
cp server/etc/httpd/conf.d/pulp_apache_22.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp.conf
%endif
cp server/etc/httpd/conf.d/pulp_content.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp_content.conf

# Server init scripts/unit files and environment files
%if %{pulp_systemd} == 0
cp server/etc/default/upstart_pulp_celerybeat %{buildroot}/%{_sysconfdir}/default/pulp_celerybeat
cp server/etc/default/upstart_pulp_resource_manager %{buildroot}/%{_sysconfdir}/default/pulp_resource_manager
cp server/etc/default/upstart_pulp_workers %{buildroot}/%{_sysconfdir}/default/pulp_workers
cp -d server/etc/rc.d/init.d/* %{buildroot}/%{_initddir}/
%else
cp server/etc/default/systemd_pulp_celerybeat %{buildroot}/%{_sysconfdir}/default/pulp_celerybeat
cp server/etc/default/systemd_pulp_resource_manager %{buildroot}/%{_sysconfdir}/default/pulp_resource_manager
cp server/etc/default/systemd_pulp_workers %{buildroot}/%{_sysconfdir}/default/pulp_workers
mkdir -p %{buildroot}/%{_usr}/lib/systemd/system/
cp server/usr/lib/systemd/system/* %{buildroot}/%{_usr}/lib/systemd/system/
mkdir -p %{buildroot}/%{_usr}/lib/tmpfiles.d/
cp server/usr/lib/tmpfiles.d/* %{buildroot}/%{_usr}/lib/tmpfiles.d/
%endif

# Pulp Web Services
cp -R server/usr/share/pulp/wsgi %{buildroot}/%{_datadir}/pulp

# Web Content
ln -s %{_var}/lib/pulp/published %{buildroot}/%{_var}/www/pub

# Nodes Publishing
ln -s %{_var}/lib/pulp/content %{buildroot}/%{_var}/www/pulp/nodes

# Tools
cp server/bin/* %{buildroot}/%{_bindir}

# Ghost
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/ca.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/ca.crt
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/rsa.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/rsa_pub.key

# Install SELinux policy modules
pushd server/selinux/server
./install.sh %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_datadir}/pulp/selinux/server
cp enable.sh %{buildroot}%{_datadir}/pulp/selinux/server
cp uninstall.sh %{buildroot}%{_datadir}/pulp/selinux/server
cp relabel.sh %{buildroot}%{_datadir}/pulp/selinux/server
popd

# Nodes Configuration
pushd nodes/common
cp -R etc/pulp %{buildroot}/%{_sysconfdir}
popd
pushd nodes/parent
cp -R etc/httpd %{buildroot}/%{_sysconfdir}
cp -R etc/pulp %{buildroot}/%{_sysconfdir}
popd
pushd nodes/child
cp -R etc/pulp %{buildroot}/%{_sysconfdir}
popd

# Nodes Scripts
pushd nodes/common
cp bin/* %{buildroot}/%{_bindir}
popd

# Types
cp -R nodes/child/pulp_node/importers/types/* %{buildroot}/%{_usr}/lib/pulp/plugins/types/

# WWW
ln -s %{_var}/lib/pulp/nodes/published/http %{buildroot}/%{_var}/www/pulp/nodes
ln -s %{_var}/lib/pulp/nodes/published/https %{buildroot}/%{_var}/www/pulp/nodes
# End Nodes Configuration

# Templates for Django
mkdir -p %{buildroot}/%{_datadir}/pulp/templates
cp server/usr/share/pulp/templates/* %{buildroot}/%{_datadir}/pulp/templates/

%endif # End server installation block

# Everything else installation

# Ghost
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/rsa.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/rsa_pub.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/server/rsa_pub.key

# Configuration
cp -R agent/etc/pulp/agent/agent.conf %{buildroot}/%{_sysconfdir}/%{name}/agent/
cp -R client_consumer/etc/pulp/consumer/consumer.conf %{buildroot}/%{_sysconfdir}/%{name}/consumer/
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 19
cp client_consumer/etc/bash_completion.d/pulp-consumer %{buildroot}/%{_sysconfdir}/bash_completion.d/
%endif

# Agent
cp agent/etc/gofer/plugins/pulpplugin.conf %{buildroot}/%{_sysconfdir}/gofer/plugins

# Ghost
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/consumer-cert.pem

# pulp-consumer man page
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 19
cp docs/_build/man/pulp-consumer.1 %{buildroot}/%{_mandir}/man1
%endif

%clean
rm -rf %{buildroot}


# define required pulp platform version.
%global pulp_version %{version}


# ---- Server ------------------------------------------------------------------
%if %{pulp_server}
%package server
Summary: The pulp platform server
Group: Development/Languages
Requires: pulp-selinux
Requires: python-%{name}-common = %{pulp_version}
Requires: python-%{name}-repoauth = %{pulp_version}
Requires: python-blinker
Requires: python-celery >= 3.1.0
Requires: python-celery < 3.2.0
Requires: python-pymongo >= 3.0.0
Requires: python-mongoengine >= 0.10.0
Requires: python-setuptools
Requires: python-oauth2 >= 1.5.211
Requires: python-httplib2
Requires: python-isodate >= 0.5.0-1.pulp
Requires: python-importlib
Requires: python-qpid
Requires: python-nectar >= 1.5.0
Requires: python-semantic_version >= 2.2.0
Requires: httpd
Requires: mod_ssl
Requires: openssl
Requires: nss-tools
Requires: python-ldap
Requires: python-gofer >= %{gofer_version}
Requires: crontabs
Requires: acl
Requires: mod_wsgi >= 3.4-1.pulp
Requires: mod_xsendfile >= 0.12
Requires: m2crypto
Requires: genisoimage
Requires: kobo
Requires: sshpass
# RHEL6 ONLY
%if 0%{?rhel} == 6
Requires: nss >= 3.12.9
Requires: Django14
%else
Requires: python-django >= 1.4.0
%endif
%if %{pulp_systemd} == 1
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
Obsoletes: pulp

%description server
Pulp provides replication, access, and accounting for software repositories.

%files server
# - root:root
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/default/pulp_celerybeat
%config(noreplace) %{_sysconfdir}/default/pulp_workers
%config(noreplace) %{_sysconfdir}/default/pulp_resource_manager
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_content.conf
%dir %{_sysconfdir}/pki/%{name}
%dir %{_sysconfdir}/%{name}/content/sources/conf.d
%dir %{_sysconfdir}/%{name}/server
%dir %{_sysconfdir}/%{name}/server/plugins.conf.d
%dir %{_sysconfdir}/%{name}/vhosts80
%dir %{_datadir}/%{name}/wsgi
%{_datadir}/%{name}/templates
%{_datadir}/%{name}/wsgi/webservices.wsgi
%{_datadir}/%{name}/wsgi/content.wsgi
%{_bindir}/pulp-manage-db
%{_bindir}/pulp-qpid-ssl-cfg
%{_bindir}/pulp-gen-ca-certificate
%dir %{_usr}/lib/%{name}/plugins/types
%{python_sitelib}/%{name}/server/
%{python_sitelib}/%{name}/plugins/
%{python_sitelib}/pulp_server*.egg-info
%if %{pulp_systemd} == 0
# Install the init scripts
%defattr(755,root,root,-)
%{_initddir}/pulp_celerybeat
%{_initddir}/pulp_workers
%{_initddir}/pulp_resource_manager
%else
# Install the systemd unit files
%defattr(-,root,root,-)
%{_usr}/lib/systemd/system/pulp_celerybeat
%{_usr}/lib/systemd/system/pulp_workers
%{_usr}/lib/systemd/system/pulp_resource_manager
%defattr(-,root,root,-)
%{_usr}/lib/tmpfiles.d/
%endif
# 640 root:apache
%defattr(640,root,apache,-)
%ghost %{_sysconfdir}/pki/%{name}/ca.key
%ghost %{_sysconfdir}/pki/%{name}/ca.crt
%ghost %{_sysconfdir}/pki/%{name}/rsa.key
%ghost %{_sysconfdir}/pki/%{name}/rsa_pub.key
%config(noreplace) %{_sysconfdir}/%{name}/server.conf
# - apache:apache
%defattr(-,apache,apache,-)
%dir %{_var}/lib/%{name}
%{_var}/lib/%{name}/published
%{_var}/lib/%{name}/static
%{_var}/lib/%{name}/uploads
%{_var}/www/pub
%{_var}/cache/%{name}/
%{_var}/run/%{name}/
%defattr(640,apache,apache,750)
%dir %{_var}/log/%{name}
# Install the docs
%defattr(-,root,root,-)
%doc README LICENSE COPYRIGHT

%pre server
# If we are upgrading
if [ $1 -gt 1 ] ; then
    %if %{pulp_systemd} == 1
        /bin/systemctl stop pulp_workers > /dev/null 2>&1 ||:
        /bin/systemctl stop pulp_celerybeat > /dev/null 2>&1 ||:
        /bin/systemctl stop pulp_resource_manager > /dev/null 2>&1 ||:
    %else
        /sbin/service pulp_workers stop > /dev/null 2>&1 ||:
        /sbin/service pulp_celerybeat stop > /dev/null 2>&1 ||:
        /sbin/service pulp_resource_manager stop > /dev/null 2>&1 ||:
    %endif
fi

%post server

# RSA key pair
KEY_DIR="%{_sysconfdir}/pki/%{name}"
KEY_PATH="$KEY_DIR/rsa.key"
KEY_PATH_PUB="$KEY_DIR/rsa_pub.key"
if [ ! -f $KEY_PATH ]
then
  # Ensure the key generated is only readable by the owner.
  OLD_UMASK=$(umask)
  umask 077
  openssl genrsa -out $KEY_PATH 2048 &> /dev/null
  openssl rsa -in $KEY_PATH -pubout > $KEY_PATH_PUB 2> /dev/null
  umask $OLD_UMASK
fi
chmod 640 $KEY_PATH
chmod 644 $KEY_PATH_PUB
chown root:apache $KEY_PATH
chown root:apache $KEY_PATH_PUB
ln -fs $KEY_PATH_PUB %{_var}/lib/%{name}/static

# CA certificate
if [ $1 -eq 1 ]; # not an upgrade
then
  pulp-gen-ca-certificate
fi


%preun server
# If we are uninstalling
if [ $1 -eq 0 ] ; then
    %if %{pulp_systemd} == 1
        /bin/systemctl stop pulp_workers > /dev/null 2>&1 ||:
        /bin/systemctl stop pulp_celerybeat > /dev/null 2>&1 ||:
        /bin/systemctl stop pulp_resource_manager > /dev/null 2>&1 ||:
    %else
        /sbin/service pulp_workers stop > /dev/null 2>&1 ||:
        /sbin/service pulp_celerybeat stop > /dev/null 2>&1 ||:
        /sbin/service pulp_resource_manager stop > /dev/null 2>&1 ||:
    %endif
fi

%if %{pulp_systemd} == 1
%postun server
%systemd_postun
%endif


# ---- Nodes Common ----------------------------------------------------------------

%package nodes-common
Summary: Pulp nodes common modules
Group: Development/Languages
Requires: pulp-server = %{pulp_version}
Requires: python-pulp-bindings = %{pulp_version}

%description nodes-common
Pulp nodes common modules.

%files nodes-common
%defattr(-,root,root,-)
%dir %{python_sitelib}/pulp_node
%dir %{python_sitelib}/pulp_node/extensions
%{_bindir}/pulp-gen-nodes-certificate
%{python_sitelib}/pulp_node/extensions/__init__.py*
%{python_sitelib}/pulp_node/*.py*
%{python_sitelib}/pulp_node_common*.egg-info
%defattr(640,root,apache,-)
# The nodes.conf file contains OAuth secrets, so we don't want it to be world readable
%config(noreplace) %{_sysconfdir}/pulp/nodes.conf
%defattr(-,root,root,-)
%doc

%post nodes-common
# Generate the certificate used to access the local server.
pulp-gen-nodes-certificate

%postun nodes-common
# clean up the nodes certificate.
if [ $1 -eq 0 ]; then
  rm -rf /etc/pki/pulp/nodes
fi


# ---- Parent Nodes ----------------------------------------------------------

%package nodes-parent
Summary: Pulp parent nodes support
Group: Development/Languages
Requires: %{name}-nodes-common = %{version}
Requires: pulp-server = %{pulp_version}

%description nodes-parent
Pulp parent nodes support.

%files nodes-parent
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_nodes.conf
%{_sysconfdir}/pulp/server/plugins.conf.d/nodes/distributor/
%{python_sitelib}/pulp_node/profilers/
%{python_sitelib}/pulp_node/distributors/
%{python_sitelib}/pulp_node_parent*.egg-info
%defattr(-,apache,apache,-)
%{_var}/lib/pulp/nodes
%{_var}/www/pulp/nodes
%defattr(-,root,root,-)
%doc


# ---- Child Nodes -----------------------------------------------------------

%package nodes-child
Summary: Pulp child nodes support
Group: Development/Languages
Requires: %{name}-nodes-common = %{version}
Requires: pulp-server = %{pulp_version}
Requires: python-pulp-agent-lib = %{pulp_version}
Requires: python-nectar >= 1.5.0

%description nodes-child
Pulp child nodes support.

%files nodes-child
%defattr(-,root,root,-)
%dir %{_sysconfdir}/pulp/server/plugins.conf.d/nodes/importer
%{python_sitelib}/pulp_node/importers/
%{python_sitelib}/pulp_node/handlers/
%{python_sitelib}/pulp_node_child*.egg-info
%{_usr}/lib/pulp/plugins/types/nodes.json
%{_sysconfdir}/pulp/agent/conf.d/nodes.conf
%defattr(640,root,apache,-)
# We don't want the importer config to be world readable, since it can contain proxy passwords
%{_sysconfdir}/pulp/server/plugins.conf.d/nodes/importer/*
%defattr(-,root,root,-)
%doc


# ---- Nodes Admin Extensions ------------------------------------------------------

%package nodes-admin-extensions
Summary: Pulp admin client extensions
Group: Development/Languages
Requires: %{name}-nodes-common = %{version}
Requires: pulp-admin-client = %{pulp_version}

%description nodes-admin-extensions
Pulp nodes admin client extensions.

%files nodes-admin-extensions
%defattr(-,root,root,-)
%{python_sitelib}/pulp_node/extensions/admin/
%{python_sitelib}/pulp_node_admin_extensions*.egg-info
%doc


# ---- Nodes Consumer Extensions ---------------------------------------------------

%package nodes-consumer-extensions
Summary: Pulp nodes consumer client extensions
Group: Development/Languages
Requires: %{name}-nodes-common = %{version}
Requires: %{name}-consumer-client = %{pulp_version}

%description nodes-consumer-extensions
Pulp nodes consumer client extensions.

%files nodes-consumer-extensions
%defattr(-,root,root,-)
%{python_sitelib}/pulp_node/extensions/consumer/
%{python_sitelib}/pulp_node_consumer_extensions*.egg-info
%doc

%endif # End pulp_server if block


# ---- Lazy Streamer ---------------------------------------------------------------

%if %{pulp_streamer}
%package -n python-pulp-streamer
Summary: The pulp lazy streamer
Group: Development/Languages

Requires: httpd
Requires: pulp-server
Requires: python-mongoengine
Requires: python-nectar >= 1.5.0
%if 0%{?rhel}
Requires: python-twisted-core
Requires: python-twisted-web
%endif
%if 0%{?fedora}
Requires: python-twisted
%endif
%if %{pulp_systemd} == 1
Requires(preun): systemd
Requires(postun): systemd
%endif

%description -n python-pulp-streamer
The streamer component of the Pulp Lazy Sync feature.

%files -n python-pulp-streamer
%defattr(-,root,root,-)
%{_bindir}/pulp_streamer
%{python_sitelib}/%{name}/streamer/
%{python_sitelib}/pulp_streamer*.egg-info
%config(noreplace) %{_sysconfdir}/%{name}/streamer.conf
%config(noreplace) %{_sysconfdir}/default/pulp_streamer
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_streamer.conf
%{_datadir}/%{name}/wsgi/streamer.tac
%{_datadir}/%{name}/wsgi/streamer_auth.wsgi

%if %{pulp_systemd} == 0
# Install the init scripts
%defattr(755,root,root,-)
%{_initddir}/pulp_streamer
%else
# Install the systemd unit files
%defattr(-,root,root,-)
%{_usr}/lib/systemd/system/pulp_streamer.service
%endif
# - apache:apache
%defattr(-,apache,apache,-)
%{_var}/www/streamer

# Uninstall scriptlet
%preun -n python-pulp-streamer
if [ $1 -eq 0 ] ; then
    %if %{pulp_systemd} == 1
        /bin/systemctl stop pulp_streamer > /dev/null 2>&1 ||:
    %else
        /sbin/service pulp_streamer stop > /dev/null 2>&1 ||:
    %endif
fi
%if %{pulp_systemd} == 1
%postun -n python-pulp-streamer
%systemd_postun
%endif

# End of pulp streamer if block
%endif


# ---- Common ------------------------------------------------------------------

%package -n python-pulp-common
Summary: Pulp common python packages
Group: Development/Languages
Obsoletes: pulp-common
Requires: python-isodate >= 0.5.0-1.pulp
Requires: python-iniparse
# RHEL5 ONLY
%if 0%{?rhel} == 5
Requires: python-simplejson
%endif

%description -n python-pulp-common
A collection of components that are common between the pulp server and client.

%files -n python-pulp-common
%defattr(-,root,root,-)
%dir %{_usr}/lib/%{name}
%dir %{python_sitelib}/%{name}
%{python_sitelib}/%{name}/__init__.*
%{python_sitelib}/%{name}/common/
%{python_sitelib}/pulp_common*.egg-info
%doc README LICENSE COPYRIGHT


# ---- Devel ------------------------------------------------------------------

%package -n python-pulp-devel
Summary: Pulp devel python packages
Group: Development/Languages
%if 0%{?rhel} == 6
Requires: python-unittest2
%endif

%description -n python-pulp-devel
A collection of tools used for developing & testing Pulp plugins

%files -n python-pulp-devel
%defattr(-,root,root,-)
%dir %{python_sitelib}/%{name}
%{python_sitelib}/%{name}/__init__.*
%{python_sitelib}/%{name}/devel/
%{python_sitelib}/pulp_devel*.egg-info
%doc README LICENSE COPYRIGHT


# ---- Client Bindings ---------------------------------------------------------

%package -n python-pulp-bindings
Summary: Pulp REST bindings for python
Group: Development/Languages
Requires: python-%{name}-common = %{pulp_version}
%if %{pulp_client_oauth}
Requires: python-oauth2 >= 1.5.170-2.pulp
%endif
Requires: m2crypto

%description -n python-pulp-bindings
The Pulp REST API bindings for python.

%files -n python-pulp-bindings
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/bindings/
%{python_sitelib}/pulp_bindings*.egg-info
%doc README LICENSE COPYRIGHT


# ---- Client Extension Framework -----------------------------------------------------

%package -n python-pulp-client-lib
Summary: Pulp client extensions framework
Group: Development/Languages
Requires: m2crypto
Requires: python-%{name}-common = %{pulp_version}
Requires: python-okaara >= 1.0.32
Requires: python-isodate >= 0.5.0-1.pulp
Requires: python-setuptools
Obsoletes: pulp-client-lib

%description -n python-pulp-client-lib
A framework for loading Pulp client extensions.

%files -n python-pulp-client-lib
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/client/commands/
%{python_sitelib}/%{name}/client/extensions/
%{python_sitelib}/%{name}/client/upload/
%{python_sitelib}/%{name}/client/*.py
%{python_sitelib}/%{name}/client/*.pyc
%{python_sitelib}/%{name}/client/*.pyo
%{python_sitelib}/pulp_client_lib*.egg-info
%doc README LICENSE COPYRIGHT


# ---- Agent Handler Framework -------------------------------------------------

%package -n python-pulp-agent-lib
Summary: Pulp agent handler framework
Group: Development/Languages
Requires: python-%{name}-common = %{pulp_version}

%description -n python-pulp-agent-lib
A framework for loading agent handlers that provide support
for content, bind and system specific operations.

%files -n python-pulp-agent-lib
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/agent/
%{python_sitelib}/pulp_agent*.egg-info
%dir %{_sysconfdir}/%{name}/agent
%dir %{_sysconfdir}/%{name}/agent/conf.d
%dir %{_usr}/lib/%{name}/agent
%doc README LICENSE COPYRIGHT


# ---- Admin Client (CLI) ------------------------------------------------------
%if %{pulp_admin}
%package admin-client
Summary: Admin tool to administer the pulp server
Group: Development/Languages
Requires: python >= 2.6
Requires: python-%{name}-common = %{pulp_version}
Requires: python-%{name}-bindings = %{pulp_version}
Requires: python-%{name}-client-lib = %{pulp_version}
Obsoletes: pulp-admin
Obsoletes: pulp-builtins-admin-extensions <= %{pulp_version}

%description admin-client
A tool used to administer the pulp server, such as repo creation and
synching, and to kick off remote actions on consumers.

%files admin-client
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/client/admin/
%{python_sitelib}/pulp_client_admin*.egg-info
%dir %{_sysconfdir}/%{name}/admin
%dir %{_sysconfdir}/%{name}/admin/conf.d
%{_sysconfdir}/bash_completion.d/pulp-admin
%dir %{_usr}/lib/%{name}/admin/extensions/
%config(noreplace) %{_sysconfdir}/%{name}/admin/admin.conf
%{_bindir}/%{name}-admin
%doc README LICENSE COPYRIGHT
%doc %{_mandir}/man1/pulp-admin.1*
%endif # End of pulp_admin if block


# ---- Consumer Client (CLI) ---------------------------------------------------

%package consumer-client
Summary: Consumer tool to administer the pulp consumer.
Group: Development/Languages
Requires: python-%{name}-common = %{pulp_version}
Requires: python-%{name}-bindings = %{pulp_version}
Requires: python-%{name}-client-lib = %{pulp_version}
Obsoletes: pulp-consumer
Obsoletes: pulp-builtins-consumer-extensions <= %{pulp_version}

%description consumer-client
A tool used to administer a pulp consumer.

%files consumer-client
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/client/consumer/
%{python_sitelib}/pulp_client_consumer*.egg-info
%dir %{_sysconfdir}/%{name}/consumer
%dir %{_sysconfdir}/%{name}/consumer/conf.d
%dir %{_sysconfdir}/pki/%{name}/consumer/
%dir %{_usr}/lib/%{name}/consumer/extensions/
%config(noreplace) %{_sysconfdir}/%{name}/consumer/consumer.conf
%{_bindir}/%{name}-consumer
%ghost %{_sysconfdir}/pki/%{name}/consumer/rsa.key
%ghost %{_sysconfdir}/pki/%{name}/consumer/rsa_pub.key
%ghost %{_sysconfdir}/pki/%{name}/consumer/server/rsa_pub.key
%ghost %{_sysconfdir}/pki/%{name}/consumer/consumer-cert.pem
%doc README LICENSE COPYRIGHT
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 19
%{_sysconfdir}/bash_completion.d/pulp-consumer
%doc %{_mandir}/man1/pulp-consumer.1*
%endif


%post consumer-client

# RSA key pair
KEY_DIR="%{_sysconfdir}/pki/%{name}/consumer/"
KEY_PATH="$KEY_DIR/rsa.key"
KEY_PATH_PUB="$KEY_DIR/rsa_pub.key"
if [ ! -f $KEY_PATH ]
then
  # Ensure the key generated is only readable by the owner.
  OLD_UMASK=$(umask)
  umask 077
  openssl genrsa -out $KEY_PATH 2048 &> /dev/null
  openssl rsa -in $KEY_PATH -pubout > $KEY_PATH_PUB 2> /dev/null
  umask $OLD_UMASK
fi
chmod 640 $KEY_PATH


# ---- Agent -------------------------------------------------------------------

%package agent
Summary: The Pulp agent
Group: Development/Languages
Requires: python-%{name}-bindings = %{pulp_version}
Requires: python-%{name}-agent-lib = %{pulp_version}
Requires: %{name}-consumer-client = %{pulp_version}
Requires: python-gofer >= %{gofer_version}
Requires: gofer >= %{gofer_version}
Requires: m2crypto

%description agent
The pulp agent, used to provide remote command & control and
scheduled actions such as reporting installed content profiles
on a defined interval.

%files agent
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/agent/agent.conf
%{python_sitelib}/%{name}/agent/gofer/
%{_sysconfdir}/gofer/plugins/pulpplugin.conf
%doc README LICENSE COPYRIGHT

# --- Selinux ---------------------------------------------------------------------

%if %{pulp_server}
%package        selinux
Summary:        Pulp SELinux policy for pulp components.
Group:          Development/Languages
BuildRequires:  rpm-python
BuildRequires:  make
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy-devel
BuildRequires:  hardlink
Obsoletes: pulp-selinux-server

Requires: selinux-policy >= 3
Requires(post): policycoreutils-python
Requires(post): /usr/sbin/semodule, /sbin/fixfiles, /usr/sbin/semanage
Requires(postun): /usr/sbin/semodule

%description    selinux
SELinux policy for Pulp's components

%pre selinux
# Record old version so we can limit which restorecon statement are executed later
test -e %{_localstatedir}/lib/rpm-state/%{name} || mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
oldversion=$(semodule -l | grep pulp-server)
echo ${oldversion:12} > %{_localstatedir}/lib/rpm-state/%{name}/old-version

exit 0
%post selinux
# Enable SELinux policy modules
if /usr/sbin/selinuxenabled ; then
 %{_datadir}/pulp/selinux/server/enable.sh %{_datadir}
fi

# restorcecon wasn't reading new file contexts we added when running under 'post' so moved to 'posttrans'
# Spacewalk saw same issue and filed BZ here: https://bugzilla.redhat.com/show_bug.cgi?id=505066
%posttrans selinux
if /usr/sbin/selinuxenabled ; then
 cat %{_localstatedir}/lib/rpm-state/%{name}/old-version | xargs %{_datadir}/pulp/selinux/server/relabel.sh
 rm %{_localstatedir}/lib/rpm-state/%{name}/old-version
fi

%preun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
%{_datadir}/pulp/selinux/server/uninstall.sh
%{_datadir}/pulp/selinux/server/relabel.sh
rm -r %{_localstatedir}/lib/rpm-state/%{name}
fi
exit 0

%files selinux
%defattr(-,root,root,-)
%doc README LICENSE COPYRIGHT
%{_datadir}/pulp/selinux/server/*
%{_datadir}/selinux/*/pulp-server.pp
%{_datadir}/selinux/*/pulp-celery.pp
%{_datadir}/selinux/*/pulp-streamer.pp
%{_datadir}/selinux/devel/include/apps/pulp-server.if
%{_datadir}/selinux/devel/include/apps/pulp-celery.if
%{_datadir}/selinux/devel/include/apps/pulp-streamer.if

%endif # End selinux if block

%if %{pulp_server}
%package -n python-pulp-repoauth
Summary: Framework for cert-based repo authentication
Group: Development/Languages
Requires: httpd
Requires: mod_ssl
Requires: mod_wsgi >= 3.4-1.pulp
Requires: openssl
Requires: python-%{name}-common = %{pulp_version}
Requires: python-rhsm
Requires: python-setuptools

%description -n python-pulp-repoauth
Cert-based repo authentication for Pulp

%files -n python-pulp-repoauth
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/pulp/repo_auth.conf
%{_datadir}/%{name}/wsgi/repo_auth.wsgi
%{python_sitelib}/%{name}/repoauth/
%{python_sitelib}/pulp_repoauth*.egg-info

%package -n python-pulp-oid_validation
Summary: Cert-based repo authentication for Pulp
Group: Development/Languages
Requires: python-rhsm
Requires: python-pulp-repoauth = %{pulp_version}

%description -n python-pulp-oid_validation
Cert-based repo authentication for Pulp

%files -n python-pulp-oid_validation
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/oid_validation/
%{python_sitelib}/pulp_oid_validation*.egg-info

%endif # End pulp_server if block for repoauth

%changelog
* Tue Jun 14 2016 Jeremy Cline <jcline@redhat.com> 2.8.4-2
- Add python-importlib dependency for pulp-server

* Mon Jun 13 2016 Jeremy Cline <jcline@redhat.com> 2.8.4-1
- Import spec file from upstream
