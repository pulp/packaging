%{?scl:%scl_package python-vine}
%{!?scl:%global pkg_name %{name}}

%global srcname vine

Name:		%{?scl_prefix}python-vine
Version:	1.1.3
Release:	1%{?dist}
Summary:	Celery vine

License:	BSD
URL:		http://pypi.python.org/pypi/vine
Source0:	http://pypi.python.org/packages/source/v/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  %{?scl_prefix_python}python-devel
BuildRequires:  %{?scl_prefix_python}python-setuptools
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

%{?scl:Requires:	%{scl}-runtime}

%description
Celery Vine

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
%doc Changelog LICENSE README.rst
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}*.egg-info

%changelog
* Wed Apr 05 2017 Patrick Creech - 1.1.3
- Initial Build

