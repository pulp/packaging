#SELinux
%global selinux_variants mls strict targeted
%global selinux_policyver %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp 2> /dev/null)
%global moduletype apps

# Required gofer version
%global gofer_version 2.5


Name: pulp
Version: 2.8.2
Release: 1%{?dist}
BuildArch: noarch

Summary: An application for managing software repositories
License: GPLv2+
URL: https://github.com/pulp/pulp
Source0: https://github.com/pulp/pulp/archive/pulp-%{version}-1.tar.gz

BuildRequires: checkpolicy
BuildRequires: hardlink
BuildRequires: plantuml
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-rpm-macros
BuildRequires: python-sphinx >= 1.0.8
BuildRequires: selinux-policy-devel
BuildRequires: systemd


%description
Pulp provides replication, access, and accounting for software repositories.


%prep
%autosetup -n %{name}-%{name}-%{version}-1


%build
# Build Python packages.
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_build
    popd
done

# Build SELinux policies.
cd server/selinux/server
distver=fedora%{fedora}
sed -i "s/policy_module(pulp-server, [0-9]*.[0-9]*.[0-9]*)/policy_module(pulp-server, %{version})/"\
    pulp-server.te
sed -i "s/policy_module(pulp-celery, [0-9]*.[0-9]*.[0-9]*)/policy_module(pulp-celery, %{version})/"\
    pulp-celery.te
sed -i "s/policy_module(pulp-streamer, [0-9]*.[0-9]*.[0-9]*)/policy_module(pulp-streamer, %{version})/"\
    pulp-streamer.te
./build.sh ${distver}
cd -

# Build docs.
pushd docs
make %{?_smp_mflags} html
make %{?_smp_mflags} man
popd


%install
# Install the Python packages
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_install
    popd
done

# Create some common directories, used by multiple subpackages.
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -d %{buildroot}%{_sysconfdir}/pki/%{name}/content
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_usr}/lib/%{name}/plugins/types
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}/%{_datadir}/pulp/wsgi/
install -d %{buildroot}%{_var}/log/%{name}/

# agent installation
install -d %{buildroot}/%{_sysconfdir}/gofer/plugins
install -d %{buildroot}/%{_sysconfdir}/%{name}/agent/conf.d
install -d %{buildroot}/%{_usr}/lib/%{name}/agent/handlers

install -pm644 agent/etc/gofer/plugins/pulpplugin.conf %{buildroot}/%{_sysconfdir}/gofer/plugins
install -pm644 agent/etc/pulp/agent/agent.conf %{buildroot}/%{_sysconfdir}/%{name}/agent/

# pulp-admin installation
install -d %{buildroot}/%{_sysconfdir}/bash_completion.d
install -d %{buildroot}/%{_sysconfdir}/%{name}/admin/conf.d
install -d %{buildroot}/%{_usr}/lib/%{name}/admin/extensions

install -pm644 client_admin/etc/bash_completion.d/pulp-admin \
    %{buildroot}/%{_sysconfdir}/bash_completion.d/
install -pm644 client_admin/etc/pulp/admin/admin.conf %{buildroot}/%{_sysconfdir}/%{name}/admin/
install -pm644 docs/_build/man/pulp-admin.1 %{buildroot}/%{_mandir}/man1/

# pulp-consumer installation
install -d %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/server
install -d %{buildroot}/%{_sysconfdir}/%{name}/consumer/conf.d
install -d %{buildroot}/%{_usr}/lib/%{name}/consumer/extensions

install -pm644 client_consumer/etc/bash_completion.d/pulp-consumer \
    %{buildroot}/%{_sysconfdir}/bash_completion.d/
install -pm644 client_consumer/etc/pulp/consumer/consumer.conf \
    %{buildroot}/%{_sysconfdir}/%{name}/consumer/
install -pm644 docs/_build/man/pulp-consumer.1 %{buildroot}/%{_mandir}/man1

# These files get filled in during the installation
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/consumer-cert.pem
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/rsa.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/rsa_pub.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer/server/rsa_pub.key

# child nodes installation
install -d %{buildroot}%{_sysconfdir}/pulp/server/plugins.conf.d/nodes/importer/

install -pm644 nodes/child/etc/pulp/agent/conf.d/nodes.conf \
    %{buildroot}%{_sysconfdir}/pulp/agent/conf.d/
install -pm644 nodes/child/etc/pulp/server/plugins.conf.d/nodes/importer/http.conf \
    %{buildroot}%{_sysconfdir}/pulp/server/plugins.conf.d/nodes/importer/
# Types
install -pm644 nodes/child/pulp_node/importers/types/* %{buildroot}/%{_usr}/lib/pulp/plugins/types/

# common nodes installation
install -d %{buildroot}%{_sysconfdir}/pki/pulp/nodes

# The nodes.conf file contains oauth secrets, so it must not be world readable.
install -pm640 nodes/common/etc/pulp/nodes.conf %{buildroot}%{_sysconfdir}/pulp/
install -pm755 nodes/common/bin/pulp-gen-nodes-certificate %{buildroot}%{_bindir}

# parent nodes installation
install -d %{buildroot}%{_sysconfdir}/pulp/server/plugins.conf.d/nodes/distributor/
install -d %{buildroot}/%{_sharedstatedir}/%{name}/nodes/published/http
install -d %{buildroot}/%{_sharedstatedir}/%{name}/nodes/published/https
install -d %{buildroot}/%{_var}/www/%{name}/nodes

install -pm644 nodes/parent/etc/httpd/conf.d/pulp_nodes.conf \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -pm644 nodes/parent/etc/pulp/server/plugins.conf.d/nodes/distributor/http.conf \
    %{buildroot}%{_sysconfdir}/pulp/server/plugins.conf.d/nodes/distributor/

# WWW
install -d %{buildroot}/%{_datadir}/pulp/templates/

ln -s %{_sharedstatedir}/pulp/content %{buildroot}/%{_var}/www/pulp/nodes
ln -s %{_sharedstatedir}/pulp/nodes/published/http %{buildroot}/%{_var}/www/pulp/nodes
ln -s %{_sharedstatedir}/pulp/nodes/published/https %{buildroot}/%{_var}/www/pulp/nodes

install -pm644 server/usr/share/pulp/templates/* %{buildroot}/%{_datadir}/pulp/templates/

# pulp-server installation
install -d %{buildroot}%{_sysconfdir}/%{name}/content/sources/conf.d
install -d %{buildroot}%{_sysconfdir}/%{name}/server/plugins.conf.d
install -d %{buildroot}%{_sysconfdir}/%{name}/vhosts80
install -d %{buildroot}%{_sysconfdir}/default/
install -d %{buildroot}%{_usr}/lib/tmpfiles.d/
install -d %{buildroot}%{_datadir}/pulp/selinux/server
install -d %{buildroot}%{_var}/cache/%{name}
install -d %{buildroot}%{_var}/run/%{name}
install -d %{buildroot}%{_sharedstatedir}/rpm-state/pulp/old-version
install -d %{buildroot}%{_sharedstatedir}/%{name}/content
install -d %{buildroot}%{_sharedstatedir}/%{name}/published
install -d %{buildroot}%{_sharedstatedir}/%{name}/static
install -d %{buildroot}%{_sharedstatedir}/%{name}/templates
install -d %{buildroot}%{_sharedstatedir}/%{name}/uploads
install -d %{buildroot}%{_var}/www

# Install SELinux policy modules
pushd server/selinux/server
./install.sh %{buildroot}%{_datadir}
# Remove the unneeded .if files
rm %{buildroot}%{_datadir}/selinux/devel/include/apps/pulp-*.if
popd

install -pm755 server/bin/* %{buildroot}/%{_bindir}
install -pm644 server/etc/default/systemd_pulp_celerybeat \
    %{buildroot}/%{_sysconfdir}/default/pulp_celerybeat
install -pm644 server/etc/default/systemd_pulp_resource_manager \
    %{buildroot}/%{_sysconfdir}/default/pulp_resource_manager
install -pm644 server/etc/default/systemd_pulp_workers \
    %{buildroot}/%{_sysconfdir}/default/pulp_workers
install -pm644 server/etc/httpd/conf.d/pulp_apache_24.conf \
    %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp.conf
install -pm644 server/etc/httpd/conf.d/pulp_content.conf \
    %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp_content.conf
install -pm644 server/etc/pulp/* %{buildroot}/%{_sysconfdir}/%{name}
install -pm644 server/%{_unitdir}/* %{buildroot}/%{_unitdir}
install -pm644 server/usr/lib/tmpfiles.d/* %{buildroot}/%{_usr}/lib/tmpfiles.d/
install -pm755 server/selinux/server/enable.sh %{buildroot}%{_datadir}/pulp/selinux/server
install -pm755 server/selinux/server/uninstall.sh %{buildroot}%{_datadir}/pulp/selinux/server
install -pm755 server/selinux/server/relabel.sh %{buildroot}%{_datadir}/pulp/selinux/server
install -pm644 server/usr/share/pulp/wsgi/* %{buildroot}/%{_datadir}/pulp/wsgi/

# Web Content
ln -s %{_sysconfdir}/pki/pulp/rsa_pub.key %{buildroot}/%{_var}/lib/pulp/static
ln -s %{_var}/lib/pulp/published %{buildroot}/%{_var}/www/pub

# These files will be generated during installation
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/ca.crt
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/ca.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/rsa.key
touch %{buildroot}/%{_sysconfdir}/pki/%{name}/rsa_pub.key

# pulp-streamer installation
install -d %{buildroot}/%{_sysconfdir}/default/
install -d %{buildroot}/%{_sysconfdir}/%{name}/
install -d %{buildroot}/%{_datadir}/pulp/wsgi/
install -d %{buildroot}/%{_var}/www/streamer/

install -pm644 streamer/etc/default/systemd_pulp_streamer \
    %{buildroot}/%{_sysconfdir}/default/pulp_streamer
install -pm644 streamer/etc/httpd/conf.d/pulp_streamer.conf \
    %{buildroot}/%{_sysconfdir}/httpd/conf.d/pulp_streamer.conf
install -pm644 streamer/etc/pulp/streamer.conf %{buildroot}/%{_sysconfdir}/%{name}/streamer.conf
install -pm644 streamer/usr/share/pulp/wsgi/streamer_auth.wsgi \
    %{buildroot}/%{_datadir}/pulp/wsgi/
install -pm644 streamer/usr/share/pulp/wsgi/streamer.tac %{buildroot}/%{_datadir}/pulp/wsgi/
install -pm644 streamer/%{_unitdir}/* %{buildroot}/%{_unitdir}


# ---- Admin Client (CLI) ------------------------------------------------------
%package admin-client
Summary: Admin tool to administer the pulp server
Requires: python2-%{name}-common = %{version}
Requires: python2-%{name}-bindings = %{version}
Requires: python2-%{name}-client-lib = %{version}


%description admin-client
A tool used to administer the pulp server, such as repository creation and
synchronization, and to kick off remote actions on consumers.


%files admin-client
%license LICENSE
%doc README COPYRIGHT
%doc %{_mandir}/man1/pulp-admin.1*
%config %{_sysconfdir}/bash_completion.d/pulp-admin
%dir %{_sysconfdir}/%{name}/admin
%config(noreplace) %{_sysconfdir}/%{name}/admin/admin.conf
%dir %{_sysconfdir}/%{name}/admin/conf.d
%{_bindir}/%{name}-admin
%dir %{_usr}/lib/%{name}/admin
%dir %{_usr}/lib/%{name}/admin/extensions
%{python2_sitelib}/%{name}/client/admin/
%{python2_sitelib}/pulp_client_admin*.egg-info


# ---- Agent -------------------------------------------------------------------
%package agent
Summary: The Pulp agent
Requires: gofer >= %{gofer_version}
Requires: m2crypto
Requires: %{name}-consumer-client = %{version}
Requires: python-gofer >= %{gofer_version}
Requires: python2-%{name}-bindings = %{version}
Requires: python2-%{name}-agent-lib = %{version}


%description agent
The pulp agent, used to provide remote command & control and
scheduled actions such as reporting installed content profiles
on a defined interval.


%files agent
%license LICENSE
%doc README COPYRIGHT
%config(noreplace) %{_sysconfdir}/gofer/plugins/pulpplugin.conf
%config(noreplace) %{_sysconfdir}/%{name}/agent/agent.conf
%{python2_sitelib}/%{name}/agent/gofer/


# ---- Consumer Client (CLI) ---------------------------------------------------
%package consumer-client
Summary: Consumer tool to administer the pulp consumer
Requires: python2-%{name}-common = %{version}
Requires: python2-%{name}-bindings = %{version}
Requires: python2-%{name}-client-lib = %{version}


%description consumer-client
A tool used to administer a pulp consumer.


%files consumer-client
%license LICENSE
%doc README COPYRIGHT
%config %{_sysconfdir}/bash_completion.d/pulp-consumer
%dir %{_sysconfdir}/pki/%{name}/consumer
%ghost %{_sysconfdir}/pki/%{name}/consumer/rsa_pub.key
%ghost %dir %{_sysconfdir}/pki/%{name}/consumer/server
%ghost %{_sysconfdir}/pki/%{name}/consumer/server/rsa_pub.key
%ghost %{_sysconfdir}/pki/%{name}/consumer/consumer-cert.pem
%dir %{_sysconfdir}/%{name}/consumer
%dir %{_sysconfdir}/%{name}/consumer/conf.d
%config(noreplace) %{_sysconfdir}/%{name}/consumer/consumer.conf
%{_bindir}/%{name}-consumer
%dir %{_usr}/lib/%{name}/consumer
%{python2_sitelib}/%{name}/client/consumer/
%{python2_sitelib}/pulp_client_consumer*.egg-info
%doc %{_mandir}/man1/pulp-consumer.1*

%defattr(640,root,root,-)
%ghost %{_sysconfdir}/pki/%{name}/consumer/rsa.key

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


# Documentation
%package doc
Summary: Pulp documentation


%description doc
Documentation for the Pulp project.


%files doc
%license LICENSE
%doc docs/_build/html/*


# ---- Nodes Admin Extensions ------------------------------------------------------
%package nodes-admin-extensions
Summary: Pulp admin client extensions
Requires: %{name}-nodes-common = %{version}
Requires: pulp-admin-client = %{version}


%description nodes-admin-extensions
Pulp nodes admin client extensions.


%files nodes-admin-extensions
%doc README COPYRIGHT
%{python2_sitelib}/pulp_node/extensions/admin/
%{python2_sitelib}/pulp_node_admin_extensions*.egg-info


# ---- Child Nodes -----------------------------------------------------------
%package nodes-child
Summary: Pulp child nodes support
Requires: %{name}-nodes-common = %{version}
Requires: pulp-server = %{version}
Requires: python2-pulp-agent-lib = %{version}


%description nodes-child
Pulp child nodes support.


%files nodes-child
%doc README COPYRIGHT
%config(noreplace) %{_sysconfdir}/pulp/agent/conf.d/nodes.conf
%dir %{_sysconfdir}/pulp/server/plugins.conf.d/nodes/importer
%{_usr}/lib/pulp/plugins/types/nodes.json
%{python2_sitelib}/pulp_node/importers/
%{python2_sitelib}/pulp_node/handlers/
%{python2_sitelib}/pulp_node_child*.egg-info

%defattr(640,root,apache,-)
# We don't want the importer config to be world readable, since it can contain proxy passwords
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/nodes/importer/*


# ---- Nodes Common ----------------------------------------------------------------
%package nodes-common
Summary: Pulp nodes common modules
Requires: pulp-server = %{version}
Requires: python2-pulp-bindings = %{version}


%description nodes-common
Pulp nodes common modules.


%files nodes-common
%doc README COPYRIGHT
%{_bindir}/pulp-gen-nodes-certificate
%ghost %{_sysconfdir}/pki/pulp/nodes
%dir %{_sysconfdir}/pulp/server/plugins.conf.d/nodes
%dir %{python2_sitelib}/pulp_node
%{python2_sitelib}/pulp_node/*.py*
%dir %{python2_sitelib}/pulp_node/extensions
%{python2_sitelib}/pulp_node/extensions/__init__.py*
%{python2_sitelib}/pulp_node_common*.egg-info

%defattr(640,root,apache,-)
# The nodes.conf file contains OAuth secrets, so we don't want it to be world readable
%config(noreplace) %{_sysconfdir}/pulp/nodes.conf


%post nodes-common
# Generate the certificate used to access the local server.
pulp-gen-nodes-certificate


# ---- Nodes Consumer Extensions ---------------------------------------------------
%package nodes-consumer-extensions
Summary: Pulp nodes consumer client extensions
Requires: %{name}-nodes-common = %{version}
Requires: %{name}-consumer-client = %{version}


%description nodes-consumer-extensions
Pulp nodes consumer client extensions.


%files nodes-consumer-extensions
%doc README COPYRIGHT
%{python2_sitelib}/pulp_node/extensions/consumer/
%{python2_sitelib}/pulp_node_consumer_extensions*.egg-info


# ---- Parent Nodes ----------------------------------------------------------
%package nodes-parent
Summary: Pulp parent nodes support
Requires: %{name}-nodes-common = %{version}
Requires: pulp-server = %{version}


%description nodes-parent
Pulp parent nodes support.


%files nodes-parent
%license LICENSE
%doc README COPYRIGHT
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_nodes.conf
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/nodes/distributor/
%{python2_sitelib}/pulp_node/distributors/
%{python2_sitelib}/pulp_node/profilers/
%{python2_sitelib}/pulp_node_parent*.egg-info

%defattr(-,apache,apache,-)
%{_var}/lib/pulp/nodes
%{_var}/www/pulp/nodes


# --- Selinux ---------------------------------------------------------------------
%package        selinux
Summary:        Pulp SELinux policy for pulp components

Requires: python2-%{name}-common = %{version}
Requires: selinux-policy >= 3
Requires: selinux-policy-targeted
Requires(post): /usr/sbin/semodule, /sbin/fixfiles, /usr/sbin/semanage
Requires(post): policycoreutils-python
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
fi


%preun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
%{_datadir}/pulp/selinux/server/uninstall.sh
%{_datadir}/pulp/selinux/server/relabel.sh
fi
exit 0


%files selinux
%license LICENSE
%doc README COPYRIGHT
%{_datadir}/pulp/selinux
%{_datadir}/selinux/*/pulp-celery.pp
%{_datadir}/selinux/*/pulp-server.pp
%{_datadir}/selinux/*/pulp-streamer.pp
%ghost %{_localstatedir}/lib/rpm-state/%{name}


# ---- Server ------------------------------------------------------------------
%package server
Summary: The pulp platform server
Requires: acl
Requires: crontabs
Requires: genisoimage
Requires: glibc-common
Requires: httpd
Requires: httpd-filesystem
Requires: m2crypto
Requires: mod_ssl
Requires: mod_wsgi >= 3.4-1.pulp
Requires: mod_xsendfile >= 0.12
Requires: nss-tools
Requires: openssl
Requires: pulp-selinux
Requires: python-blinker
Requires: python-celery >= 3.1.11
Requires: python-celery < 3.2.0
Requires: python-django >= 1.4.0
Requires: python-gofer >= %{gofer_version}
Requires: python-httplib2
Requires: python-isodate >= 0.5.0-1
Requires: python-ldap
Requires: python-nectar >= 1.5.0
Requires: python-qpid
Requires: python-semantic_version >= 2.2.0
Requires: python2-%{name}-common = %{version}
Requires: python2-%{name}-repoauth = %{version}
Requires: python2-mongoengine >= 0.10.0
Requires: python2-oauth2 >= 1.5.211
Requires: python2-pymongo >= 3.0.0
Requires: python2-setuptools
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description server
Pulp provides replication, access, and accounting for software repositories.


%files server
%license LICENSE
%doc README COPYRIGHT
%config(noreplace) %{_sysconfdir}/default/pulp_celerybeat
%config(noreplace) %{_sysconfdir}/default/pulp_resource_manager
%config(noreplace) %{_sysconfdir}/default/pulp_workers
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_content.conf
%ghost %{_sysconfdir}/pki/%{name}/ca.crt
%ghost %{_sysconfdir}/pki/%{name}/rsa_pub.key
%{_sysconfdir}/%{name}/content
%dir %{_sysconfdir}/%{name}/server
%dir %{_sysconfdir}/%{name}/server/plugins.conf.d
%dir %{_sysconfdir}/%{name}/vhosts80
%{_bindir}/pulp-manage-db
%{_bindir}/pulp-qpid-ssl-cfg
%{_bindir}/pulp-gen-ca-certificate
%dir %{_usr}/lib/%{name}/plugins
%dir %{_usr}/lib/%{name}/plugins/types
%{_unitdir}/*
%{_usr}/lib/tmpfiles.d/*
%{python2_sitelib}/%{name}/server/
%{python2_sitelib}/%{name}/plugins/
%{python2_sitelib}/pulp_server*.egg-info
%{_datadir}/pulp/templates
%dir %{_datadir}/pulp/wsgi
%{_datadir}/pulp/wsgi/content.wsgi
%{_datadir}/pulp/wsgi/repo_auth.wsgi
%{_datadir}/pulp/wsgi/webservices.wsgi

%defattr(640,root,apache,-)
%ghost %{_sysconfdir}/pki/%{name}/ca.key
%ghost %{_sysconfdir}/pki/%{name}/rsa.key
%config(noreplace) %{_sysconfdir}/%{name}/server.conf

%defattr(-,apache,apache,-)
%{_var}/cache/%{name}/
%dir %{_var}/run/pulp
%dir %{_var}/lib/%{name}
%{_var}/lib/%{name}/content
%{_var}/lib/%{name}/published
%{_var}/lib/%{name}/static
%{_var}/lib/%{name}/uploads
%{_var}/www/pub
%{_var}/www/pulp

%defattr(640,apache,apache,750)
%dir %{_var}/log/%{name}


%pre server
# If we are upgrading
if [ $1 -gt 1 ] ; then
        /bin/systemctl stop pulp_workers > /dev/null 2>&1
        /bin/systemctl stop pulp_celerybeat > /dev/null 2>&1
        /bin/systemctl stop pulp_resource_manager > /dev/null 2>&1
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

%systemd_post pulp_workers.service
%systemd_post pulp_celerybeat.service
%systemd_post pulp_resource_manager.service
%systemd_post pulp_streamer.service


%preun server
%systemd_preun pulp_workers.service
%systemd_preun pulp_celerybeat.service
%systemd_preun pulp_resource_manager.service
%systemd_preun pulp_streamer.service


%postun server
%systemd_postun


# ---- Agent Handler Framework -------------------------------------------------
%package -n python2-pulp-agent-lib
Summary: Pulp agent handler framework
Requires: python2-%{name}-common = %{version}
%{?python_provide:%python_provide python2-pulp-agent-lib}


%description -n python2-pulp-agent-lib
A framework for loading agent handlers that provide support
for content, bind and system specific operations.


%files -n python2-pulp-agent-lib
%license LICENSE
%dir %{_sysconfdir}/%{name}/agent
%dir %{_sysconfdir}/%{name}/agent/conf.d
%dir %{_usr}/lib/%{name}/agent
%{python2_sitelib}/%{name}/agent/
%{python2_sitelib}/pulp_agent*.egg-info
%doc README COPYRIGHT


# ---- Client Bindings ---------------------------------------------------------
%package -n python2-pulp-bindings
Summary: Pulp REST bindings for python
Requires: m2crypto
Requires: python2-oauth2 >= 1.5.170-2.pulp
Requires: python2-%{name}-common = %{version}
%{?python_provide:%python_provide python2-pulp-bindings}


%description -n python2-pulp-bindings
The Pulp REST API bindings for python.


%files -n python2-pulp-bindings
%license LICENSE
%{python2_sitelib}/%{name}/bindings/
%{python2_sitelib}/pulp_bindings*.egg-info
%doc README COPYRIGHT


# ---- Client Extension Framework -----------------------------------------------------
%package -n python2-pulp-client-lib
Summary: Pulp client extensions framework
Requires: m2crypto
Requires: python-isodate >= 0.5.0-1
Requires: python-okaara >= 1.0.32
Requires: python2-%{name}-common = %{version}
Requires: python2-setuptools
%{?python_provide:%python_provide python2-client-lib}


%description -n python2-pulp-client-lib
A framework for loading Pulp client extensions.


%files -n python2-pulp-client-lib
%license LICENSE
%dir %{python2_sitelib}/%{name}/client
%{python2_sitelib}/%{name}/client/*.py
%{python2_sitelib}/%{name}/client/*.pyc
%{python2_sitelib}/%{name}/client/*.pyo
%{python2_sitelib}/%{name}/client/commands/
%{python2_sitelib}/%{name}/client/extensions/
%{python2_sitelib}/%{name}/client/upload/
%{python2_sitelib}/pulp_client_lib*.egg-info
%doc README COPYRIGHT


# ---- Common ------------------------------------------------------------------
%package -n python2-pulp-common
Summary: Pulp common python packages
Requires: python-iniparse
Requires: python-isodate >= 0.5.0-1
%{?python_provide:%python_provide python2-pulp-common}


%description -n python2-pulp-common
A collection of components that are common between the pulp server and client.


%files -n python2-pulp-common
%license LICENSE
%doc README COPYRIGHT
%dir %{_sysconfdir}/pki/%{name}
%dir %{_sysconfdir}/pulp
%dir %{_usr}/lib/%{name}
%dir %{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}/__init__.*
%{python2_sitelib}/%{name}/common/
%{python2_sitelib}/pulp_common*.egg-info
%dir %{_datadir}/pulp


# ---- Devel ------------------------------------------------------------------
%package -n python2-pulp-devel
Summary: Pulp devel python packages
Requires: python2-%{name}-common = %{version}
%{?python_provide:%python_provide python2-pulp-devel}


%description -n python2-pulp-devel
A collection of tools used for developing & testing Pulp plugins


%files -n python2-pulp-devel
%license LICENSE
%{python2_sitelib}/%{name}/devel/
%{python2_sitelib}/pulp_devel*.egg-info
%doc README COPYRIGHT


# ---- OID validation code ---------------------------------------------------
%package -n python2-pulp-oid_validation
Summary: Cert-based repository authentication for Pulp
Requires: python-rhsm
Requires: python2-pulp-repoauth = %{version}
%{?python_provide:%python_provide python2-pulp-oid_validation}


%description -n python2-pulp-oid_validation
Cert-based repository authentication for Pulp


%files -n python2-pulp-oid_validation
%doc README COPYRIGHT
%{python2_sitelib}/%{name}/oid_validation/
%{python2_sitelib}/pulp_oid_validation*.egg-info


# ---- Repo authorization ---------------------------------------------------------
%package -n python2-pulp-repoauth
Summary: Framework for cert-based repository authentication
Requires: httpd
Requires: mod_ssl
Requires: mod_wsgi >= 3.4-1.pulp
Requires: openssl
Requires: python-rhsm
Requires: python2-%{name}-common = %{version}
Requires: python2-setuptools
%{?python_provide:%python_provide python2-pulp-repoauth}


%description -n python2-pulp-repoauth
Cert-based repository authentication for Pulp


%files -n python2-pulp-repoauth
%doc README COPYRIGHT
%config(noreplace) %{_sysconfdir}/pulp/repo_auth.conf
%{python2_sitelib}/%{name}/repoauth/
%{python2_sitelib}/pulp_repoauth*.egg-info
%{_datadir}/%{name}/wsgi/repo_auth.wsgi


# ---- Lazy Streamer ---------------------------------------------------------------
%package -n python2-pulp-streamer
Summary: The pulp lazy streamer
Requires: httpd
Requires: pulp-server >= %{version}
Requires: python-twisted
Requires: python2-mongoengine
Requires(preun): systemd
Requires(postun): systemd
%{?python_provide:%python_provide python2-pulp-streamer}


%description -n python2-pulp-streamer
The streamer component of the Pulp Lazy Sync feature.


%files -n python2-pulp-streamer
%doc README COPYRIGHT
%config(noreplace) %{_sysconfdir}/default/pulp_streamer
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_streamer.conf
%config(noreplace) %{_sysconfdir}/%{name}/streamer.conf
%{_bindir}/pulp_streamer
%{python2_sitelib}/%{name}/streamer/
%{python2_sitelib}/pulp_streamer*.egg-info
%{_usr}/lib/systemd/system/pulp_streamer.service
%{_datadir}/pulp/wsgi/streamer_auth.wsgi
%{_datadir}/pulp/wsgi/streamer.tac

%defattr(-,apache,apache,-)
%{_var}/www/streamer


# Uninstall scriptlet
%preun -n python2-pulp-streamer
if [ $1 -eq 0 ] ; then
    /bin/systemctl stop pulp_streamer > /dev/null 2>&1
fi


%postun -n python2-pulp-streamer
%systemd_postun


%changelog
* Mon May 09 2016 Randy Barlow <rbarlow@redhat.com> - 2.8.2-1
- Initial import, taken from Fedora 24.
