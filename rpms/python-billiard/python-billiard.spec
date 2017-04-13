%{?scl:%scl_package python-billiard}
%{!?scl:%global pkg_name %{name}}

%global srcname billiard

Name:		%{?scl_prefix}python-billiard
Version:	3.5.0.2
Release:	1%{?dist}
Summary:	Multiprocessing Pool Extensions

License:	BSD
URL:		http://pypi.python.org/pypi/billiard
Source0:	http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:	%{?scl_prefix_python}python-devel
BuildRequires:	%{?scl_prefix_python}python-setuptools
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

%{?scl:Requires:	%{scl}-runtime}

%description
This package contains extensions to the multiprocessing Pool.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{?scl:scl enable %{scl} "}
%{__python} setup.py build
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --no-compile --root %{buildroot} --install-purelib %{python_sitelib}
%{?scl:"}

%files
%doc CHANGES.txt LICENSE.txt README.rst
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}*.egg-info
%exclude %{python_sitelib}/funtests/


%changelog
* Wed Apr 05 2017 Patrick Creech - 3.5.0.2-1
- new version

* Thu Nov 17 2016 Patrick Creech <pcreech@redhat.com> - 3.3.0.23-2
- rebuilt based on PR feedback

* Wed Nov 09 2016 Patrick Creech <pcreech@redhat.com> - 3.5.0.2-1
- Initial build

