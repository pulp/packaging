%{?scl:%scl_package python-anyjson}
%{!?scl:%global pkg_name %{name}}

%global srcname anyjson

Name:		%{?scl_prefix}python-anyjson
Version:	0.3.3
Release:	1%{?dist}
Summary:	Wraps the best available JSON implementation available

License:	BSD
URL:		http://pypi.python.org/pypi/anyjson
Source0:	http://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:	%{?scl_prefix_python}python-devel
BuildRequires:	%{?scl_prefix_python}python-setuptools
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

%{?scl:Requires:	%{scl}-runtime}

%description
Anyjson loads whichever is the fastest JSON module installed and
provides a uniform API regardless of which JSON implementation is used.

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
%doc CHANGELOG README LICENSE
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}*.egg-info

%changelog
* Wed Nov 09 2016 Patrick Creech <pcreech@redhat.com> - 0.3.3-1
- Initial build


