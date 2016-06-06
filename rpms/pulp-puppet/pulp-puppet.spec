%global required_pulp_version 2.8.4


Name:		pulp-puppet
Version:	2.8.4
Release:	1%{?dist}

License:	GPLv2+
Summary:	Support for Puppet content in the Pulp Platform
URL:		https://github.com/pulp/pulp_puppet
Source0:	https://github.com/pulp/pulp_puppet/archive/%{name}-%{version}-1.tar.gz
BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
BuildRequires:	python-sphinx


%description
Provides a collection of platform plugins, client extensions and agent
handlers that provide Puppet support


%prep
%autosetup -n pulp_puppet-%{name}-%{version}-1


%build
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_build
    popd
done

pushd docs
make %{?_smp_mflags} html
# We don't want to install the objects.inv, because it is a build-time database
rm _build/html/objects.inv
popd


%install
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_install
    popd
done

install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -d %{buildroot}/%{_sysconfdir}/pulp/admin/conf.d/
install -d %{buildroot}/%{_sysconfdir}/pulp/agent/conf.d/
install -d %{buildroot}/%{_sysconfdir}/pulp/vhosts80
install -d %{buildroot}/%{_var}/lib/pulp/published/puppet/http
install -d %{buildroot}/%{_var}/lib/pulp/published/puppet/https
install -d %{buildroot}/%{_usr}/lib/pulp/agent/handlers
install -d %{buildroot}/%{_usr}/lib/pulp/admin/extensions
install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_datadir}/pulp/wsgi/

install -pm644 pulp_puppet_plugins/etc/httpd/conf.d/* \
    %{buildroot}/%{_sysconfdir}/httpd/conf.d/

install -pm644 pulp_puppet_plugins/etc/pulp/vhosts80/* \
    %{buildroot}/%{_sysconfdir}/pulp/vhosts80

install -pm644 pulp_puppet_plugins/usr/share/pulp/wsgi/* \
    %{buildroot}/%{_datadir}/pulp/wsgi/

install -pm644 pulp_puppet_extensions_admin/etc/pulp/admin/conf.d/* \
    %{buildroot}/%{_sysconfdir}/pulp/admin/conf.d/

install -pm644 pulp_puppet_handlers/etc/pulp/agent/conf.d/* \
    %{buildroot}/%{_sysconfdir}/pulp/agent/conf.d/


# ---- Admin Extensions
%package admin-extensions
Summary:	The Pulp Puppet admin client extensions
Requires:	pulp-admin-client = %{required_pulp_version}
Requires:	python2-pulp-puppet-common = %{version}


%description admin-extensions
A collection of extensions that supplement and override generic admin
client capabilities with Puppet specific features.


%files admin-extensions
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_puppet/extensions/admin/
%{python_sitelib}/pulp_puppet_extensions_admin*.egg-info
%config(noreplace) %{_sysconfdir}/pulp/admin/conf.d/puppet.conf


# ---- Consumer Extensions
%package consumer-extensions
Summary:	The Pulp Puppet consumer client extensions
Requires:	pulp-consumer-client = %{required_pulp_version}
Requires:	python2-pulp-puppet-common = %{version}


%description consumer-extensions
A collection of extensions that supplement and generic consumer
client capabilities with Puppet specific features


%files consumer-extensions
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_puppet/extensions/consumer/
%{python_sitelib}/pulp_puppet_extensions_consumer*.egg-info


# ---- Development package
%package devel
Summary:	Pulp Puppet devel package
Requires:	python2-pulp-puppet-common = %{version}


%description devel
A collection of development utilities useful for developing pulp-puppet


%files devel
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_puppet/devel/
%{python_sitelib}/pulp_puppet_devel*.egg-info


# ---- Documentation
%package doc
Summary:	Pulp Puppet documentation


%description doc
Documentation for the Pulp Puppet plugins


%files doc
%license LICENSE
%doc AUTHORS COPYRIGHT
%doc docs/_build/html/*


# ---- Agent Handlers
%package handlers
Summary:	Pulp agent puppet handlers
Requires:	python2-pulp-agent-lib >= %{required_pulp_version}
Requires:	python2-pulp-puppet-common = %{version}
Requires:	puppet >= 2.7.14


%description handlers
A collection of handlers that provide Puppet specific
functionality within the Pulp agent.  This includes Puppet install, update,
uninstall, bind, and unbind.


%files handlers
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_puppet/handlers/
%{python_sitelib}/pulp_puppet_handlers*.egg-info
%config(noreplace) %{_sysconfdir}/pulp/agent/conf.d/puppet_bind.conf
%config(noreplace) %{_sysconfdir}/pulp/agent/conf.d/puppet_module.conf


# ---- Plugins
%package plugins
Summary:	Pulp Puppet Plugins
Requires:	python2-pulp-puppet-common = %{version}
Requires:	pulp-server = %{required_pulp_version}
Requires:	python-semantic_version >= 2.2.0
Requires:	python-pycurl


%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide Puppet specific support.


%files plugins
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_puppet/forge/
%{python_sitelib}/pulp_puppet/plugins/
%{python_sitelib}/pulp_puppet_plugins*.egg-info
%config(noreplace) %{_sysconfdir}/pulp/vhosts80/puppet.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_puppet.conf
%{_datadir}/pulp/wsgi/puppet_forge.wsgi
%attr(-, apache, apache) %dir %{_var}/lib/pulp/published/puppet


# ---- Tools
%package tools
Summary:	Pulp Puppet tools
Requires:	puppet >= 2.7
Requires:	git >= 1.7
Requires:   python2-pulp-puppet-common = %{required_pulp_version}


%description tools
A collection of tools used to manage puppet modules.


%files tools
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_puppet/tools/
%{python_sitelib}/pulp_puppet_tools*.egg-info
%{_bindir}/pulp-puppet-module-builder


# ---- Common
%package -n python2-pulp-puppet-common
Summary:	Pulp Puppet support common library
Requires:	python2-pulp-common >= %{required_pulp_version}
%{?python_provide:%python_provide python2-pulp-puppet-common}


%description -n python2-pulp-puppet-common
A collection of modules shared among all Puppet components.


%files -n python2-pulp-puppet-common
%license LICENSE
%doc AUTHORS COPYRIGHT
%dir %{python_sitelib}/pulp_puppet
%{python_sitelib}/pulp_puppet/__init__.py*
%{python_sitelib}/pulp_puppet/common/
%dir %{python_sitelib}/pulp_puppet/extensions
%{python_sitelib}/pulp_puppet/extensions/__init__.py*
%{python_sitelib}/pulp_puppet_common*.egg-info


%changelog
* Mon Jun 06 2016 Jeremy Cline <jcline@redhat.com> - 2.8.4-1
- Bump version to 2.8.4
- Fixed python2-pulp-puppet-common `provides` statement
- tools sub-package now depends on python2-pulp-puppet-common

* Mon May 09 2016 Randy Barlow <rbarlow@redhat.com> - 2.8.2-1
- Initial import from Fedora 24.
