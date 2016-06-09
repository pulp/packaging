# Required platform version
%global platform_version 2.8


Name: pulp-ostree
Version: 1.1.1
Release: 1%{?dist}
Summary: Support for OSTree content in the Pulp platform
License: GPLv2+
URL: http://pulpproject.org
Source0: https://github.com/pulp/pulp_ostree/archive/%{name}-%{version}-1.tar.gz
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: rpm-python


%description
Provides a collection of platform plugins and admin client extensions to
provide OSTree support.


%prep
%autosetup -n pulp_ostree-%{name}-%{version}-1


%build
pushd common
%py2_build
popd

pushd extensions_admin
%py2_build
popd

pushd plugins
%py2_build
popd


%install

install -d %{buildroot}/%{_sysconfdir}/pulp/
install -d %{buildroot}/%{_var}/lib/pulp/published/ostree/
install -d %{buildroot}/%{_bindir}

pushd common
%py2_install
popd

pushd extensions_admin
%py2_install
popd

pushd plugins
%py2_install
popd

install -d %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d
install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d/

install -pm640 plugins/etc/httpd/conf.d/pulp_ostree.conf \
        %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -pm640 plugins/etc/pulp/server/plugins.conf.d/* \
        %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/


# ---- Common ----------------------------------------------------------------

%package -n python-pulp-ostree-common
Summary: Pulp OSTree support common library
Group: Development/Languages
Requires: python-pulp-common >= %{platform_version}
Requires: python-setuptools

%description -n python-pulp-ostree-common
Common libraries for OSTree support.

%files -n python-pulp-ostree-common
%license LICENSE
%doc COPYRIGHT AUTHORS
%dir %{python_sitelib}/pulp_ostree
%dir %{python_sitelib}/pulp_ostree/extensions
%{python_sitelib}/pulp_ostree/__init__.py*
%{python_sitelib}/pulp_ostree/common/
%{python_sitelib}/pulp_ostree/extensions/__init__.py*
%{python_sitelib}/pulp_ostree_common*.egg-info



# ---- Plugins ---------------------------------------------------------------

%package plugins
Summary: Pulp OSTree plugins
Group: Development/Languages
Requires: python-pulp-common >= %{platform_version}
Requires: python-pulp-ostree-common = %{version}
Requires: pulp-server >= %{platform_version}
Requires: python-setuptools
Requires: ostree >= 2015.8
Requires: python-gnupg
Requires: pygobject3

%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide OSTree specific support.

%files plugins
%license LICENSE
%doc COPYRIGHT AUTHORS
%{python_sitelib}/pulp_ostree/plugins/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_ostree.conf
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/ostree_*.json
%{python_sitelib}/pulp_ostree_plugins*.egg-info
%defattr(-,apache,apache,-)
%{_var}/lib/pulp/published/ostree/



# ---- Admin Extensions ------------------------------------------------------

%package admin-extensions
Summary: The Pulp OSTree admin client extensions
Group: Development/Languages
Requires: python-pulp-common >= %{platform_version}
Requires: python-pulp-ostree-common = %{version}
Requires: pulp-admin-client >= %{platform_version}
Requires: python-setuptools

%description admin-extensions
pulp-admin extensions for OSTree support.

%files admin-extensions
%license LICENSE
%doc COPYRIGHT AUTHORS
%{python_sitelib}/pulp_ostree/extensions/admin/
%{python_sitelib}/pulp_ostree_extensions_admin*.egg-info


%changelog
* Mon Jun 13 2016 Jeremy Cline <jcline@redhat.com> 1.1.1-1
- Intial spec file import
