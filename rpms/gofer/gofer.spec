%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name: gofer
Version: 2.7.6
Release: 1%{?dist}

License: LGPLv2
Summary: A lightweight, extensible python agent
URL: https://github.com/jortel/gofer
Source0: %{url}/archive/%{name}-%{version}-1.tar.gz
BuildArch: noarch

BuildRequires: gzip
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: rpm-python
BuildRequires: systemd

Requires: python-%{name} = %{version}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
Gofer provides an extensible, light weight, universal python agent.
The gofer core agent is a python daemon (service) that provides
infrastructure for exposing a remote API and for running Recurring
Actions. The APIs contributed by plug-ins are accessible by Remote
Method Invocation (RMI). The transport for RMI is AMQP using an
AMQP message broker. Actions are also provided by plug-ins and are
executed at the specified interval.


%prep
%autosetup -n gofer-gofer-%{version}-1


%build
pushd src
%py2_build
popd


%install
pushd src
%py2_install
popd

install -d %{buildroot}/usr/bin
install -d %{buildroot}/%{_sysconfdir}/%{name}/plugins
install -d %{buildroot}/%{_sysconfdir}/%{name}/conf.d
install -d %{buildroot}/%{_sysconfdir}/init.d
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -d %{buildroot}/%{_unitdir}
install -d %{buildroot}/%{_usr}/lib/%{name}/plugins
install -d %{buildroot}/%{_usr}/share/%{name}/plugins
install -d %{buildroot}/%{_mandir}/man1

install -pm755 bin/* %{buildroot}/usr/bin/
install -pm644 etc/%{name}/*.conf %{buildroot}/%{_sysconfdir}/%{name}/
install -pm644 etc/sysconfig/%{name}d %{buildroot}/%{_sysconfdir}/sysconfig/
install -pm644 docs/man/man1/* %{buildroot}/%{_mandir}/man1/

install -pm644 plugins/demo.conf %{buildroot}/%{_sysconfdir}/%{name}/plugins/
install -pm644 plugins/demo.py %{buildroot}/%{_usr}/share/%{name}/plugins/

install -pm644 usr/lib/systemd/system/* %{buildroot}/%{_unitdir}/


%files
%license LICENSE
%doc README.md
%doc %{_mandir}/man1/goferd.1*
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/conf.d/
%dir %{_sysconfdir}/%{name}/plugins/
%dir %{_usr}/lib/%{name}/plugins/
%dir %{_usr}/share/%{name}/plugins/
%{python_sitelib}/%{name}/agent/
%{_bindir}/%{name}d
%{_unitdir}/%{name}d.service
%config(noreplace) %{_sysconfdir}/%{name}/agent.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/demo.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}d
%{_usr}/share/%{name}/plugins/demo.*

%post
%systemd_post %{name}d.service

%preun
%systemd_preun %{name}d.service

%postun
%systemd_postun_with_restart %{name}d.service


# --- python lib -------------------------------------------------------------

%package -n python-%{name}
Summary: Gofer python lib modules
BuildRequires: python2
Requires: pam

%description -n python-%{name}
Provides gofer python lib modules.

%files -n python-%{name}
%license LICENSE
%doc README.md
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/rmi/
%dir %{python_sitelib}/%{name}/messaging/
%dir %{python_sitelib}/%{name}/messaging/adapter
%{python_sitelib}/%{name}/messaging/*.py*
%{python_sitelib}/%{name}/messaging/adapter/*.py*
%{python_sitelib}/%{name}/devel/
%{python_sitelib}/%{name}-*.egg-info


# --- tools ------------------------------------------------------------------

%package -n %{name}-tools
Summary: Gofer tools
Group: Development/Languages
BuildRequires: python
Requires: python-%{name} = %{version}

%description -n%{name}-tools
Provides the gofer tools.

%files -n %{name}-tools
%license LICENSE
%doc README.md
%doc %{_mandir}/man1/gofer.*
%{python_sitelib}/%{name}/tools/
%{_bindir}/%{name}


# --- python-qpid messaging adapter ------------------------------------------

%package -n python-%{name}-qpid
Summary: Gofer Qpid messaging adapter python package
BuildRequires: python
Requires: python-%{name} = %{version}
Requires: python-qpid >= 0.18

%description -n python-%{name}-qpid
Provides the gofer qpid messaging adapter package.

%files -n python-%{name}-qpid
%license LICENSE
%doc README.md
%{python_sitelib}/%{name}/messaging/adapter/qpid


# --- python-qpid-proton messaging adapter -----------------------------------

%package -n python-%{name}-proton
Summary: Gofer Qpid proton messaging adapter python package
BuildRequires: python
Requires: python-%{name} = %{version}
Requires: python-qpid-proton >= 0.9-5

%description -n python-%{name}-proton
Provides the gofer qpid proton messaging adapter package.

%files -n python-%{name}-proton
%license LICENSE
%doc README.md
%{python_sitelib}/%{name}/messaging/adapter/proton


# --- python-amqp messaging adapter ------------------------------------------

%package -n python-%{name}-amqp
Summary: Gofer amqp messaging adapter python package
Group: Development/Languages
BuildRequires: python
Requires: python-%{name} = %{version}
Requires: python-amqp >= 1.4.5

%description -n python-%{name}-amqp
Provides the gofer amqp messaging adapter package.

%files -n python-%{name}-amqp
%license LICENSE
%doc README.md
%{python_sitelib}/%{name}/messaging/adapter/amqp


# --- changelog --------------------------------------------------------------


%changelog
* Tue Jun 07 2016 Jeremy Cline <jcline@redhat.com> 2.7.6-2
- Initial import from upstream project
