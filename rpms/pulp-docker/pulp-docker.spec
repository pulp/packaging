%global required_pulp_version 2.8

Name: pulp-docker
Version: 2.0.1
Release: 1%{?dist}

License:   GPLv2+
Summary:   Support for Docker content in the Pulp platform
URL:       https://github.com/pulp/pulp_docker
Source0:   %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python2-rpm-macros
BuildRequires: python2-setuptools
BuildRequires: python-sphinx


%description
Provides a collection of Pulp server plugins and admin client extensions to
support Docker content.


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

install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -d %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/
install -d %{buildroot}/%{_var}/lib/pulp/published/docker/

install -pm644 plugins/etc/httpd/conf.d/* %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -pm644 plugins/etc/pulp/server/plugins.conf.d/* \
    %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/


# ---- Admin Extensions --------------------------------------------------------
%package admin-extensions
Summary: The Pulp Docker admin client extensions
Requires: pulp-admin-client >= %{required_pulp_version}
Requires: python2-pulp-docker-common = %{version}


%description admin-extensions
pulp-admin extensions for Docker support


%files admin-extensions
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_docker/extensions/admin/
%{python_sitelib}/pulp_docker_extensions_admin*.egg-info


# ---- Docker Documentation-----------------------------------------------------
%package doc
Summary: Pulp Docker documentation


%description doc
Documentation for the Pulp Docker plugins.


%files doc
%license LICENSE
%doc AUTHORS COPYRIGHT
%doc docs/_build/html/*


# ---- Plugins -----------------------------------------------------------------
%package plugins
Summary: Pulp Docker plugins
Requires: pulp-server >= %{required_pulp_version}
Requires: python-nectar >= 1.3.0
Requires: python2-pulp-docker-common = %{version}


%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide Docker specific support


%files plugins
%license LICENSE
%doc AUTHORS COPYRIGHT
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_docker.conf
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/docker_distributor_export.json
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/docker_distributor.json
%{python_sitelib}/pulp_docker/plugins/
%{python_sitelib}/pulp_docker_plugins*.egg-info
%attr(-, apache, apache) %dir %{_var}/lib/pulp/published/docker


# ---- Docker Common -----------------------------------------------------------
%package -n python2-pulp-docker-common
Summary: Pulp Docker support common library
Requires: python2-pulp-common >= %{required_pulp_version}
%{?python_provide:%python_provide python2-pulp-docker-common}


%description -n python2-pulp-docker-common
Common libraries for python2-pulp-docker


%files -n python2-pulp-docker-common
%license LICENSE
%doc AUTHORS COPYRIGHT
%dir %{python_sitelib}/pulp_docker
%{python_sitelib}/pulp_docker/__init__.py*
%{python_sitelib}/pulp_docker/common/
%dir %{python_sitelib}/pulp_docker/extensions
%{python_sitelib}/pulp_docker/extensions/__init__.py*
%{python_sitelib}/pulp_docker_common*.egg-info


%changelog
* Mon Jun 06 2016 Jeremy Cline <jcline@redhat.com> 2.0.1-1
- Bump version to 2.0.1

* Thu Mar 17 2016 Randy Barlow <rbarlow@redhat.com> 2.0.0-1
- Initial import, taken from Fedora 24.
