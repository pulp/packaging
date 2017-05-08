Name: pulp
Version: 3.0.0
Release: 0.1.alpha%{?dist}
Summary: An application for managing software repositories

License: GPLv2+
URL:     https://github.com/pulp/pulp
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-rpm-macros
BuildRequires: python3-sphinx

%global directories platform common

%description
Pulp provides replication, access, and accounting for software repositories.

%prep
%autosetup -n %{name}-%{version}

%build
for directory in %{directories}
do
    pushd $directory
    %py3_build
    popd
done

pushd docs
#make %{?_smp_mflags} html
#make %{?_smp_mflags} man
popd

%install
for directory in %{directories}
do
    pushd $directory
    %py3_install
    popd
done

install -d %{buildroot}%{_sysconfdir}/default/
cp platform/etc/default/pulp_celerybeat %{buildroot}/%{_sysconfdir}/default/pulp_celerybeat
cp platform/etc/default/pulp_resource_manager %{buildroot}/%{_sysconfdir}/default/pulp_resource_manager
cp platform/etc/default/pulp_workers %{buildroot}/%{_sysconfdir}/default/pulp_workers

mkdir -p %{buildroot}/%{_usr}/lib/systemd/system/
cp platform/usr/lib/systemd/system/* %{buildroot}/%{_usr}/lib/systemd/system/


# ---- Doc ------------------------------------------------------------------
%package doc
Summary: Pulp documentation

%description doc
Documentation for the Pulp project.

%files doc
%license LICENSE

# ---- Platform ------------------------------------------------------------------
%package platform
Summary: The pulp platform server
Requires: python3-celery >= 4.0
Requires: python3-django >= 1.8
Requires: python3-django-filter >= 0.15
Requires: python3-django-rest-framework
Requires: python3-coreapi
Requires: python3-psycopg2
Requires: python3-PyYAML
Requires: python3-setuptools
Requires: python-%{name}-common
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description platform
Pulp provides replication, access, and accounting for software repositories.

%files platform
%license LICENSE
%doc README COPYRIGHT
%{_bindir}/pulp-manager
%config(noreplace) %{_sysconfdir}/default/pulp_celerybeat
%config(noreplace) %{_sysconfdir}/default/pulp_resource_manager
%config(noreplace) %{_sysconfdir}/default/pulp_workers
%{python3_sitelib}/%{name}
%{python3_sitelib}/pulp_platform*.egg-info

%defattr(-,root,root,-)
# list these explicitly (don't glob) to prevent pulling in extra service files
%{_usr}/lib/systemd/system/pulp_celerybeat.service
%{_usr}/lib/systemd/system/pulp_worker@.service
%{_usr}/lib/systemd/system/pulp_resource_manager.service

%post platform
%systemd_post pulp_worker@.service
%systemd_post pulp_celerybeat.service
%systemd_post pulp_resource_manager.service

# ---- Common ------------------------------------------------------------------
%package -n python-pulp-common
Summary: Pulp common python packages

Provides: python3-pulp-common

%description -n python-pulp-common
A collection of components that are common between the pulp server and client.

%files -n python-pulp-common
%{python3_sitelib}/%{name}/common
%{python3_sitelib}/pulp_common*.egg-info
%{python3_sitelib}/%{name}/__init__.*
%{python3_sitelib}/%{name}/__pycache__/*
%doc README LICENSE COPYRIGHT

%changelog
* Mon Apr 17 2017 Bihan Zhang <bizhang@redhat.com> - 3.0.0-1
- Initial Pulp3 spec file
