%{?scl:%scl_package python-celery}
%{!?scl:%global pkg_name %{name}}

%global srcname celery

Name:		%{?scl_prefix}python-celery
Version:	4.0.2
Release:	4%{?dist}
Summary:	Distributed Task Queue

License:	BSD
URL:		http://celeryproject.org
Source0:	https://github.com/celery/celery/archive/v%{version}.tar.gz

BuildRequires:  %{?scl_prefix_python}python-devel
BuildRequires:  %{?scl_prefix_python}python-setuptools
BuildRequires:  %{?scl_prefix}python-billiard
BuildRequires:  %{?scl_prefix}python-kombu
%{?scl:BuildRequires:   %{scl}-build %{scl}-runtime}

Requires:  %{?scl_prefix}python-billiard >= 3.5.0.2, %{?scl_prefix}python-billiard < 3.6
Requires:  %{?scl_prefix}python-kombu >= 4.0.2, %{?scl_prefix}python-kombu < 5.0
Requires:  %{?scl_prefix}python-pytz
Requires:  %{?scl_prefix_python}python-setuptools
%{?scl:Requires:        %{scl}-runtime}

%description
An open source asynchronous task queue/job queue based on
distributed message passing. It is focused on real-time
operation, but supports scheduling as well.

The execution units, called tasks, are executed concurrently
on one or more worker nodes using multiprocessing, Eventlet
or gevent. Tasks can execute asynchronously (in the background)
or synchronously (wait until ready).

Celery is used in production systems to process millions of
tasks a day.

Celery is written in Python, but the protocol can be implemented
in any language. It can also operate with other languages using
web hooks.

The recommended message broker is RabbitMQ, but limited support
for Redis, Beanstalk, MongoDB, CouchDB and databases
(using SQLAlchemy or the Django ORM) is also available.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{?scl:scl enable %{scl} "}
%{__python} setup.py build
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --no-compile --root %{buildroot} --install-purelib %{python_sitelib} --install-scripts %{_bindir}
%{?scl:"}

%files
%doc README.rst TODO CONTRIBUTORS.txt examples
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}*.egg-info
%{_bindir}/celery*



%changelog
* Thu Apr 13 2017 Patrick Creech - 4.0.2-4
- Remove amqp dep, since it's pulled in by kombu

* Thu Apr 13 2017 Patrick Creech - 4.0.2-3
- Add missing scl build and runtime requirements

* Wed Apr 05 2017 Patrick Creech - 4.0.2-2
- Fix Requires

* Wed Apr 05 2017 Patrick Creech - 4.0.2-1
- new version

* Thu Nov 17 2016 Patrick Creech <pcreech@redhat.com> - 3.1.24-2
- Removing python-nose dep

* Wed Nov 09 2016 Patrick Creech <pcreech@redhat.com> - 3.1.24-1
- Initial build


