# define required pulp platform version.
%global pulp_version 2.8.4

Name: pulp-rpm
Version: 2.8.4
Release: 1%{?dist}

License:   GPLv2+
Summary:   Support for RPM content in the Pulp platform
URL:       https://github.com/pulp/pulp_rpm
Source0:   %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires:  python-rpm-macros
BuildRequires:  python2-rpm-macros
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx


%description
Provides a collection of platform plugins, client extensions and agent
handlers that provide RPM support.


%prep
%autosetup -n %{name}-%{version}


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

install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d
install -d %{buildroot}/%{_sysconfdir}/pki/pulp/content
install -d %{buildroot}/%{_sysconfdir}/pulp/agent/conf.d
install -d %{buildroot}/%{_sysconfdir}/pulp/vhosts80
install -d %{buildroot}/%{_sysconfdir}/yum/pluginconf.d
install -d %{buildroot}/%{_sysconfdir}/yum.repos.d
install -d %{buildroot}/%{_usr}/lib/pulp/admin/extensions
install -d %{buildroot}/%{_usr}/lib/pulp/agent/handlers
install -d %{buildroot}/%{_usr}/lib/pulp/consumer/extensions
install -d %{buildroot}/%{_usr}/lib/pulp/plugins
install -d %{buildroot}/%{_usr}/lib/yum-plugins
install -d %{buildroot}/%{_var}/lib/pulp/published/yum/http
install -d %{buildroot}/%{_datadir}/pulp-rpm
install -d %{buildroot}/%{_var}/lib/pulp/published/yum/https

install -pm644 handlers/etc/pulp/agent/conf.d/* %{buildroot}/%{_sysconfdir}/pulp/agent/conf.d/
install -pm644 handlers/etc/yum/pluginconf.d/pulp-profile-update.conf \
    %{buildroot}/%{_sysconfdir}/yum/pluginconf.d/
install -pm644 plugins/etc/httpd/conf.d/pulp_rpm.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -pm644 plugins/etc/pulp/vhosts80/rpm.conf %{buildroot}/%{_sysconfdir}/pulp/vhosts80/
install -pm644 handlers/usr/lib/yum-plugins/* %{buildroot}/%{_usr}/lib/yum-plugins/
install -pm644 plugins/usr/share/pulp-rpm/pulp_distribution.xsd %{buildroot}/%{_datadir}/pulp-rpm

# Ghost repository file for consumers
touch %{buildroot}/%{_sysconfdir}/yum.repos.d/pulp.repo


# ---- Admin Extensions --------------------------------------------------------
%package admin-extensions
Summary: The RPM admin client extensions
Requires: pulp-admin-client = %{pulp_version}
Requires: python-pulp-rpm-common = %{version}


%description admin-extensions
A collection of extensions that supplement and override generic admin
client capabilities with RPM specific features.


%files admin-extensions
%license LICENSE COPYRIGHT
%doc AUTHORS
%{python_sitelib}/pulp_rpm/extensions/admin/
%{python_sitelib}/pulp_rpm_extensions_admin*.egg-info


# ---- Consumer Extensions -----------------------------------------------------
%package consumer-extensions
Summary: The RPM consumer client extensions
Requires: pulp-consumer-client = %{pulp_version}
Requires: python-pulp-rpm-common = %{version}


%description consumer-extensions
A collection of extensions that supplement and override generic consumer
client capabilities with RPM specific features.


%files consumer-extensions
%license LICENSE COPYRIGHT
%doc AUTHORS
%{python_sitelib}/pulp_rpm/extensions/consumer/
%{python_sitelib}/pulp_rpm_extensions_consumer*.egg-info


# ---- Development package -----------------------------------------------------
%package devel
Summary: Pulp RPM devel package
Requires: python-pulp-rpm-common = %{version}


%description devel
A collection of development utilities useful for developing pulp-rpm.


%files devel
%license COPYRIGHT LICENSE
%doc AUTHORS
%{python_sitelib}/pulp_rpm/devel/
%{python_sitelib}/pulp_rpm_devel*.egg-info


# ---- Documentation ----------------------------------------------------------
%package doc
Summary: Pulp RPM documentation


%description doc
Documentation for the Pulp RPM plugins.


%files doc
%license COPYRIGHT LICENSE
%doc AUTHORS
%doc docs/_build/html/*


# ---- Agent Handlers ----------------------------------------------------------
%package handlers
Summary: Pulp agent rpm handlers
Requires: python-rhsm
Requires: python-pulp-agent-lib = %{pulp_version}
Requires: python-pulp-rpm-common = %{version}
Requires: yum


%description handlers
A collection of handlers that provide both Linux and RPM specific
functionality within the Pulp agent.  This includes RPM install, update,
uninstall; RPM profile reporting; binding through yum repository
management and Linux specific commands such as system reboot.


%files handlers
%license COPYRIGHT LICENSE
%doc AUTHORS
%{_sysconfdir}/pulp/agent/conf.d/bind.conf
%{_sysconfdir}/pulp/agent/conf.d/linux.conf
%{_sysconfdir}/pulp/agent/conf.d/rpm.conf
%ghost %{_sysconfdir}/yum.repos.d/pulp.repo
%{python_sitelib}/pulp_rpm/handlers/
%{python_sitelib}/pulp_rpm_handlers*.egg-info


# ---- Plugins -----------------------------------------------------------------
%package plugins
Summary: Pulp RPM plugins
Requires: createrepo >= 0.9.9-21
Requires: createrepo_c >= 0.4.1-1
Requires: genisoimage
Requires: m2crypto
Requires: pulp-server = %{pulp_version}
Requires: pyliblzma
Requires: python-lxml
Requires: python-nectar >= 1.2.1
Requires: python-rhsm >= 1.8.0
Requires: python2-pulp-oid_validation >= 2.7.0
Requires: python2-pulp-rpm-common = %{pulp_version}


%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide RPM specific support.


%files plugins
%license COPYRIGHT LICENSE
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_rpm.conf
%attr(-, apache, apache) %{_sysconfdir}/pki/pulp/content/
%{_sysconfdir}/pulp/vhosts80/rpm.conf
%{python_sitelib}/pulp_rpm/plugins/
%{python_sitelib}/pulp_rpm/yum_plugin/
%{python_sitelib}/pulp_rpm_plugins*.egg-info
%{_usr}/share/pulp-rpm/
%attr(-, apache, apache) %{_var}/lib/pulp/published/yum/


# ---- YUM Plugins -------------------------------------------------------------
%package yumplugins
Summary: Yum plugins supplementing in Pulp consumer operations
Requires: python-rhsm >= 1.8.0
Requires: python2-pulp-bindings = %{pulp_version}
Requires: yum


%description yumplugins
A collection of yum plugins supplementing Pulp consumer operations.


%files yumplugins
%license COPYRIGHT LICENSE
%doc AUTHORS
%{_sysconfdir}/yum/pluginconf.d/pulp-profile-update.conf
%{_usr}/lib/yum-plugins/pulp-profile-update.py*


# ---- RPM Common --------------------------------------------------------------
%package -n python2-pulp-rpm-common
Summary: Pulp RPM support common library
Group: Development/Languages
Requires: python-pulp-common = %{pulp_version}
%{?python_provide:%python_provide python2-pulp-rpm-common}


%description -n python2-pulp-rpm-common
A collection of modules shared among all RPM components.


%files -n python2-pulp-rpm-common
%license LICENSE COPYRIGHT
%doc AUTHORS
%dir %{python_sitelib}/pulp_rpm
%{python_sitelib}/pulp_rpm/__init__.py*
%{python_sitelib}/pulp_rpm/common/
%dir %{python_sitelib}/pulp_rpm/extensions/
%{python_sitelib}/pulp_rpm/extensions/__init__.py*
%{python_sitelib}/pulp_rpm_common*.egg-info


%changelog
* Mon Jun 06 2016 Jeremy Cline <jcline@redhat.com> 2.8.4-1
- Bump version to 2.8.4

* Mon May 09 2016 Randy Barlow <rbarlow@redhat.com> 2.8.2-1
- Initial import from Fedora 24.
