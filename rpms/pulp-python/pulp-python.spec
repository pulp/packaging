# This is the minimum platform version we require to function.
%global pulp_version 2.8


Name: pulp-python
Version: 1.1.0
Release: 1%{?dist}

License:   GPLv2+
Summary:   Support for Python content in the Pulp platform
URL:       https://github.com/pulp/pulp_python
Source0:   %{url}/archive/%{name}-%{version}-1.tar.gz
BuildArch: noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python-sphinx


%description
Provides a collection of platform plugins and client extensions support
for Python packages.


%prep
%autosetup -n pulp_python-pulp-python-%{version}-1


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
install -d %{buildroot}/%{_var}/lib/pulp/published/python

install -pm644 plugins/etc/httpd/conf.d/pulp_python.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/


# ---- Admin Extensions --------------------------------------------------------
%package admin-extensions
Summary: The Python admin client extensions
Requires: python-pulp-python-common = %{version}
Requires: pulp-admin-client >= %{pulp_version}


%description admin-extensions
A collection of extensions that supplement and override generic admin
client capabilities with Python specific features.


%files admin-extensions
%license LICENSE
%doc COPYRIGHT AUTHORS
%{python_sitelib}/pulp_python/extensions/admin/
%{python_sitelib}/pulp_python_extensions_admin*.egg-info


# ---- Documentation-----------------------------------------------------
%package doc
Summary: Pulp Python documentation


%description doc
Documentation for the Pulp Python plugins.


%files doc
%license LICENSE
%doc AUTHORS COPYRIGHT
%doc docs/_build/html/*


# ---- Plugins -----------------------------------------------------------------
%package plugins
Summary: Pulp Python plugins
Requires: python-pulp-python-common >= %{version}
Requires: pulp-server >= %{pulp_version}


%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide Python package support.


%files plugins
%license LICENSE
%doc COPYRIGHT AUTHORS
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_python.conf
%{python_sitelib}/pulp_python/plugins/
%{python_sitelib}/pulp_python_plugins*.egg-info
%attr(-, apache, apache) %dir %{_var}/lib/pulp/published/python/


# ---- Common (check out the hilarious package name!)---------------------------
%package -n python-pulp-python-common
Summary: Pulp Python support common library
Requires: python-pulp-common >= %{pulp_version}


%description -n python-pulp-python-common
A collection of modules shared among all Pulp-Python components.


%files -n python-pulp-python-common
%license LICENSE
%doc COPYRIGHT AUTHORS
%dir %{python_sitelib}/pulp_python
%{python_sitelib}/pulp_python/__init__.py*
%{python_sitelib}/pulp_python/common/
%dir %{python_sitelib}/pulp_python/extensions
%{python_sitelib}/pulp_python/extensions/__init__.py*
%{python_sitelib}/pulp_python_common*.egg-info


%changelog
* Mon May 09 2016 Randy Barlow <rbarlow@redhat.com> 1.1.0-1
- Initial import from Fedora 24.
