%{?scl:%scl_package python-pytz}
%{!?scl:%global pkg_name %{name}}

%global srcname pytz

Name:		%{?scl_prefix}python-pytz
Version:	2016.7
Release:	2%{?dist}
Summary:	World Timezone Definitions for Python

License:	MIT
URL:		http://pytz.sourceforge.net/
Source0:	http://pypi.io/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0: 	pytz-zoneinfo.patch

BuildRequires:  %{?scl_prefix_python}python-devel
BuildRequires:  %{?scl_prefix_python}python-setuptools
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

Requires:	tzdata
%{?scl:Requires:	%{scl}-runtime}

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Almost all (over 540) of the Olson timezones are supported.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .zoneinfo

%build
%{?scl:scl enable %{scl} "}
%{__python} setup.py build
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --no-compile --root %{buildroot} --install-purelib %{python_sitelib}
%{?scl:"}

%files
%doc LICENSE.txt CHANGES.txt README.txt
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}*.egg-info


%changelog
* Thu Nov 17 2016 Patrick Creech <pcreech@redhat.com> - 2016.7-2
- Rebuild with proper patch file

* Wed Nov 09 2016 Patrick Creech <pcreech@redhat.com> - 2016.7-1
- Initial build


