%{?scl:%scl_package python-kombu}
%{!?scl:%global pkg_name %{name}}

%global srcname kombu

Name:		%{?scl_prefix}python-kombu
Version:	3.0.37
Release:	3%{?dist}
Summary:	An AMQP Messaging Framework for Python

License:	BSD and Python
URL:		http://pypi.python.org/pypi/%{srcname}
Source0:	http://pypi.python.org/packages/source/k/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  %{?scl_prefix_python}python-devel
BuildRequires:  %{?scl_prefix_python}python-setuptools
BuildRequires:  %{?scl_prefix}python-anyjson
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

Requires:  %{?scl_prefix}python-anyjson >= 0.3.3
Requires:  %{?scl_prefix}python-amqp >= 1.4.9, %{?scl_prefix}python-amqp < 2.0
%{?scl:Requires:	%{scl}-runtime}

%description
AMQP is the Advanced Message Queuing Protocol, an open standard protocol
for message orientation, queuing, routing, reliability and security.

One of the most popular implementations of AMQP is RabbitMQ.

The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQP protocol, and
also provide proven and tested solutions to common messaging problems.


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
%doc AUTHORS Changelog FAQ LICENSE READ* THANKS TODO examples/
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}*.egg-info


%changelog
* Thu Nov 17 2016 Patrick Creech <pcreech@redhat.com> - 3.0.37-3
- Remove nose dep

* Wed Nov 09 2016 Patrick Creech <pcreech@redhat.com> - 3.0.37-2
- Limit python-amqp to less than 2

* Wed Nov 09 2016 Parick Creech <pcreech@redhat.com> - 3.0.37-1
- Initial Build


