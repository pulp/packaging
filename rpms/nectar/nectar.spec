Name:           python-nectar
Version:        1.5.2
Release:        1%{?dist}
BuildArch:      noarch

License:        GPLv2+
Group:          Development/Tools
Summary:        A download library that separates workflow from implementation details
URL:            https://github.com/pulp/nectar
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires:       python-isodate >= 0.4.9
Requires:       python-requests >= 2.4.3


%description
Nectar is a download library that abstracts the workflow of making and tracking
download requests away from the mechanics of how those requests are carried
out. It allows multiple downloaders to exist with different implementations,
such as the default "threaded" downloader, which uses the "requests" library
with multiple threads. Other experimental downloaders have used tools like
pycurl and eventlets.


%prep
%autosetup -n nectar-%{version}


%build
%py2_build


%install
%py2_install


%files
%license COPYRIGHT LICENSE.txt
%doc README.rst
%{python_sitelib}/nectar/
%{python_sitelib}/nectar*.egg-info


%changelog
* Mon Jun 06 2016 Jeremy Cline <jcline@redhat.com> - 1.5.2-1
- Bump version to 1.5.2

* Tue May 10 2016 Randy Barlow <rbarlow@redhat.com> - 1.5.1-2
- Initial import from nectar
- Use new Python and license macros.
- Remove unneeded code.
