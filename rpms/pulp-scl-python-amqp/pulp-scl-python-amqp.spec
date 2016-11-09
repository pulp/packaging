%{?scl:%scl_package python-amqp}
%{!?scl:%global pkg_name %{name}}

%global srcname amqp

Name:		%{?scl_prefix}python-amqp
Version:	1.4.9
Release:	2%{?dist}
Summary:	Low-level AMQP client for Python (fork of amqplib)

License:	LGPLv2+
URL:		http://pypi.python.org/pypi/amqp
Source0:	http://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  %{?scl_prefix_python}python-devel
BuildRequires:  %{?scl_prefix_python}python-setuptools
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

%{?scl:Requires:	%{scl}-runtime}

%description
Low-level AMQP client for Python

This is a fork of amqplib, maintained by the Celery project.

This library should be API compatible with librabbitmq.

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
* Thu Nov 17 2016 Patrick Creech <pcreech@redhat.com> - 1.4.9-2
- Remove nose dependency

* Wed Nov 09 2016 Patrick Creech <pcreech@redhat.com> - 1.4.9-1
- Initial build


