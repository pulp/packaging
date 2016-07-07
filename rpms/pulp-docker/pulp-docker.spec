Name:      pulp-docker
Version:   2.0.1
Release:   1%{?dist}
Summary:   Support for Docker layers in the Pulp platform
License:   GPLv2+
URL:       https://github.com/pulp/pulp_docker
Source0:   %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  rpm-python

%description
Provides a collection of platform plugins and admin client extensions to
provide docker support

%prep
%autosetup -n %{name}-%{version}


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

pushd common
%py2_install
popd

pushd extensions_admin
%py2_install
popd

pushd plugins
%py2_install
popd

install -d %{buildroot}/%{_var}/lib/pulp/published/docker/app/
install -d %{buildroot}/%{_var}/lib/pulp/published/docker/export/
install -d %{buildroot}/%{_var}/lib/pulp/published/docker/web/

install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -pm640 plugins/etc/httpd/conf.d/pulp_docker.conf \
        %{buildroot}/%{_sysconfdir}/httpd/conf.d/


# ---- Docker Common -----------------------------------------------------------

%package -n python-pulp-docker-common
Summary: Pulp Docker support common library
Group: Development/Languages
Requires: python-pulp-common >= 2.8.0
Requires: python-setuptools

%description -n python-pulp-docker-common
Common libraries for python-pulp-docker

%files -n python-pulp-docker-common
%license LICENSE
%doc COPYRIGHT AUTHORS
%{python_sitelib}/pulp_docker/__init__.py*
%{python_sitelib}/pulp_docker/common/
%dir %{python_sitelib}/pulp_docker
%dir %{python_sitelib}/pulp_docker/extensions
%{python_sitelib}/pulp_docker/extensions/__init__.py*
%{python_sitelib}/pulp_docker_common*.egg-info


# ---- Plugins -----------------------------------------------------------------
%package plugins
Summary: Pulp Docker plugins
Group: Development/Languages
Requires: python-pulp-common >= 2.8.0
Requires: python-pulp-docker-common = %{version}
Requires: pulp-server >= 2.8.0
Requires: python-setuptools
Requires: python-nectar >= 1.3.0

%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide Docker specific support

%files plugins
%license LICENSE
%doc COPYRIGHT AUTHORS
%{python_sitelib}/pulp_docker/plugins/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_docker.conf
%{python_sitelib}/pulp_docker_plugins*.egg-info
%defattr(-,apache,apache,-)
%{_var}/lib/pulp/published/docker/



# ---- Admin Extensions --------------------------------------------------------
%package admin-extensions
Summary: The Pulp Docker admin client extensions
Group: Development/Languages
Requires: python-pulp-common >= 2.8.0
Requires: python-pulp-docker-common = %{version}
Requires: pulp-admin-client >= 2.8.0
Requires: python-setuptools

%description admin-extensions
pulp-admin extensions for docker support

%files admin-extensions
%license LICENSE
%doc COPYRIGHT AUTHORS
%{python_sitelib}/pulp_docker/extensions/admin/
%{python_sitelib}/pulp_docker_extensions_admin*.egg-info


%changelog
* Mon Jun 13 2016 Jeremy Cline <jcline@redhat.com> 2.0.0-1
- Initial spec import
