%global srcname itypes

Name:		python-itypes
Version:	1.1.0
Release:	1%{?dist}
Summary:	Basic immutable container types for Python.

Provides: python3-itypes

License:	BSD
URL:		http://pypi.python.org/pypi/itypes/1.1.0
Source0:	http://pypi.python.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-rpm-macros

Requires: python3-jinja2

%description
Basic immutable container types for Python.

%global debug_package %{nil}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files
%doc README.md
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/%{srcname}*.egg-info
%{python3_sitelib}/__pycache__/itypes*

%changelog
* Tue Apr 18 2017 Bihan Zhang- 1.1.0
- Initial Build