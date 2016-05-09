%global required_pulp_version 2.8.0

Name:		pulp-ostree
Version:	1.1.0
Release:	2%{?dist}

License:	GPLv2+
Summary:	Support for OSTree content in the Pulp platform
URL:		https://github.com/pulp/pulp_ostree
Source0:	https://github.com/pulp/pulp_ostree/archive/%{name}-%{version}-1.tar.gz
BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
BuildRequires:	python2-sphinx


%description
Provides a collection of platform plugins and client extensions support
for OSTree content.


%prep
%autosetup -n pulp_ostree-%{name}-%{version}-1


%build
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_build
    popd
done

pushd docs
make %{?_smp_mflags} html
# We don't want to install the objects.inf, because it is a build-time database
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
install -d %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/
install -d %{buildroot}/%{_var}/lib/pulp/published/ostree/

install -pm644 plugins/etc/httpd/conf.d/* %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -pm644 plugins/etc/pulp/server/plugins.conf.d/* \
    %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/


# --- Admin Extensions
%package admin-extensions
Summary: The OSTree admin client extensions
Requires: python2-pulp-ostree-common = %{version}
Requires: pulp-admin-client >= %{required_pulp_version}


%description admin-extensions
pulp-admin extensions for OSTree support


%files admin-extensions
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_ostree/extensions/admin/
%{python_sitelib}/pulp_ostree_extensions_admin*.egg-info


# ---- OSTree Documentation
%package doc
Summary: Pulp documentation


%description doc
Documentation for the Pulp OSTree plugins.


%files doc
%license LICENSE
%doc AUTHORS COPYRIGHT
%doc docs/_build/html/*


# ---- Plugins
%package plugins
Summary: Pulp OSTree plugins
Requires: ostree >= 2015.8
Requires: pygobject3
Requires: python2-gnupg
Requires: python2-pulp-ostree-common = %{version}
Requires: pulp-server >= %{required_pulp_version}


%description plugins
Provides a collection of platformed plugins that extend the Pulp platform
to provide OSTree specific support


%files plugins
%license LICENSE
%doc AUTHORS COPYRIGHT
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_ostree.conf
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/ostree_distributor.json
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/ostree_importer.json
%{python_sitelib}/pulp_ostree/plugins/
%{python_sitelib}/pulp_ostree_plugins*.egg-info
%attr(-, apache, apache) %dir %{_var}/lib/pulp/published/ostree


# ---- OSTree Common
%package -n python2-pulp-ostree-common
Summary: Pulp OSTree support common library
Requires: python2-pulp-common >= %{required_pulp_version}
Requires: python2-setuptools
%{?python_provide:%python_provide python2-pulp-ostree-common}


%description -n python2-pulp-ostree-common
Common libraries for python2-pulp-ostree


%files -n python2-pulp-ostree-common
%license LICENSE
%doc AUTHORS COPYRIGHT
%dir %{python_sitelib}/pulp_ostree
%{python_sitelib}/pulp_ostree/__init__.py*
%{python_sitelib}/pulp_ostree/common/
%dir %{python_sitelib}/pulp_ostree/extensions
%{python_sitelib}/pulp_ostree/extensions/__init__.py*
%{python_sitelib}/pulp_ostree_common*.egg-info


%changelog
* Mon May 09 2016 Randy Barlow <rbarlow@redhat.com> - 1.1.0-2
- Initial import from Fedora 24.
