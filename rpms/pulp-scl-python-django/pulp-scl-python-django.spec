%{?scl:%scl_package python-django}
%{!?scl:%global pkg_name %{name}}

# Fix this build.  TODO: set this in pulp-scl properly
%global python_version 3.5

%global srcname Django

Name:		%{?scl_prefix}python-django
Version:	1.8.16
Release:	8%{?dist}
Summary:	A high-level Python Web framework

Group:		Development/Languages
License:	BSD
URL:		http://www.djangoproject.com
Source0:	https://files.pythonhosted.org/packages/source/D/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:	%{?scl_prefix_python}python-devel
BuildRequires:	%{?scl_prefix_python}python-setuptools
%{?scl:BuildRequires:	%{scl}-build %{scl}-runtime}

%{?scl:Requires:	%{scl}-runtime}

%description
Django is a high-level Python Web framework that encourages rapid
development and a clean, pragmatic design. It focuses on automating as
much as possible and adhering to the DRY (Don't Repeat Yourself)
principle.


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
%doc AUTHORS LICENSE README.rst
%{python_sitelib}/django/
%{python_sitelib}/%{srcname}-%{version}-py%{python_version}.egg-info
%{_bindir}/django-admin
%{_bindir}/django-admin.py

%changelog
* Fri Nov 11 2016 Patrick Creech <pcreech@redhat.com> - 1.8.16-8
- Addressing comments on PR https://github.com/pulp/packaging/pull/36/

* Tue Nov 08 2016 Patrick Creech <pcreech@redhat.com> - 1.8.16-7
- Initial release of pulp-scl python-django

