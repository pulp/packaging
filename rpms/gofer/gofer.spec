%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

# Determine supported
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
%define systemd 1
%endif

Name: gofer
Version: 2.7.6
Release: 1%{?dist}
Summary: A lightweight, extensible python agent
Group:   Development/Languages
License: LGPLv2
URL: https://github.com/jortel/gofer/
Source0: https://github.com/jortel/gofer/archive/%{name}-%{version}-1.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: gzip
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: rpm-python
Requires: python-%{name} = %{version}
%if 0%{?systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
%description
Gofer provides an extensible, light weight, universal python agent.
The gofer core agent is a python daemon (service) that provides
infrastructure for exposing a remote API and for running Recurring
Actions. The APIs contributed by plug-ins are accessible by Remote
Method Invocation (RMI). The transport for RMI is AMQP using an
AMQP message broker. Actions are also provided by plug-ins and are
executed at the specified interval.

%prep
%setup -q -n %{name}-%{name}-%{version}-1


%build
pushd src
%{__python} setup.py build
popd
pushd docs/man/man1
gzip *
popd

%install
rm -rf %{buildroot}
pushd src
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/plugins
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/init.d
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins
mkdir -p %{buildroot}/%{_usr}/share/%{name}/plugins
mkdir -p %{buildroot}/%{_mandir}/man1

cp bin/* %{buildroot}/usr/bin
cp etc/%{name}/*.conf %{buildroot}/%{_sysconfdir}/%{name}
cp etc/sysconfig/%{name}d %{buildroot}/%{_sysconfdir}/sysconfig
cp docs/man/man1/* %{buildroot}/%{_mandir}/man1

cp plugins/demo.conf %{buildroot}/%{_sysconfdir}/%{name}/plugins
cp plugins/demo.py %{buildroot}/%{_usr}/share/%{name}/plugins

%if 0%{?systemd}
cp usr/lib/systemd/system/* %{buildroot}/%{_unitdir}
%else
cp etc/init.d/%{name}d %{buildroot}/%{_sysconfdir}/init.d
%endif

rm -rf %{buildroot}/%{python_sitelib}/%{name}*.egg-info

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/conf.d/
%dir %{_sysconfdir}/%{name}/plugins/
%dir %{_usr}/lib/%{name}/plugins/
%dir %{_usr}/share/%{name}/plugins/
%{python_sitelib}/%{name}/agent/
%{_bindir}/%{name}d
%if 0%{?systemd}
%attr(644,root,root) %{_unitdir}/%{name}d.service
%else
%attr(755,root,root) %{_sysconfdir}/init.d/%{name}d
%endif
%attr(644,root,root) %{_sysconfdir}/sysconfig/%{name}d
%config(noreplace) %{_sysconfdir}/%{name}/agent.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/demo.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}d
%{_usr}/share/%{name}/plugins/demo.*
%doc LICENSE
%doc %{_mandir}/man1/goferd.*

%post
%if 0%{?systemd}
%systemd_post %{name}d.service
%else
chkconfig --add %{name}d
%endif

%preun
%if 0%{?systemd}
%systemd_preun %{name}d.service
%else
if [ $1 = 0 ] ; then
   /sbin/service %{name}d stop >/dev/null 2>&1
   /sbin/chkconfig --del %{name}d
fi
%endif

%postun
%if 0%{?systemd}
%systemd_postun_with_restart %{name}d.service
%endif


# --- python lib -------------------------------------------------------------

%package -n python-%{name}
Summary: Gofer python lib modules
Group: Development/Languages
BuildRequires: python
Requires: pam
%if 0%{?rhel} && 0%{?rhel} < 6
Requires: python-ctypes
Requires: python-simplejson
Requires: python-hashlib
Requires: python-uuid
%endif

%description -n python-%{name}
Provides gofer python lib modules.

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/rmi/
%dir %{python_sitelib}/%{name}/messaging/
%dir %{python_sitelib}/%{name}/messaging/adapter
%{python_sitelib}/%{name}/messaging/*.py*
%{python_sitelib}/%{name}/messaging/adapter/*.py*
%{python_sitelib}/%{name}/devel/
%doc LICENSE


# --- tools ------------------------------------------------------------------

%package -n %{name}-tools
Summary: Gofer tools
Group: Development/Languages
BuildRequires: python
Requires: python-%{name} = %{version}

%description -n%{name}-tools
Provides the gofer tools.

%files -n %{name}-tools
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/tools/
%{_bindir}/%{name}
%doc LICENSE
%doc %{_mandir}/man1/gofer.*


# --- python-qpid messaging adapter ------------------------------------------

%package -n python-%{name}-qpid
Summary: Gofer Qpid messaging adapter python package
Group: Development/Languages
BuildRequires: python
Requires: python-%{name} = %{version}
Requires: python-qpid >= 0.18
%if 0%{?rhel} && 0%{?rhel} < 6
Requires: python-ssl
%endif

%description -n python-%{name}-qpid
Provides the gofer qpid messaging adapter package.

%files -n python-%{name}-qpid
%{python_sitelib}/%{name}/messaging/adapter/qpid
%doc LICENSE


# --- python-qpid-proton messaging adapter -----------------------------------

%package -n python-%{name}-proton
Summary: Gofer Qpid proton messaging adapter python package
Group: Development/Languages
BuildRequires: python
Requires: python-%{name} = %{version}
Requires: python-qpid-proton >= 0.9-5

%description -n python-%{name}-proton
Provides the gofer qpid proton messaging adapter package.

%files -n python-%{name}-proton
%{python_sitelib}/%{name}/messaging/adapter/proton
%doc LICENSE


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
%{python_sitelib}/%{name}/messaging/adapter/amqp
%doc LICENSE


# --- changelog --------------------------------------------------------------


%changelog
* Mon Jun 13 2016 Jeremy Cline <jcline@redhat.com> 2.7.6-1
- Initial spec import from upstream project
