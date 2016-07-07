%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-qpid
Version:        0.18
Release:        10%{?dist}
Group:          Development/Languages
Summary:        Python client library for AMQP
License:        ASL 2.0
URL:            https://qpid.apache.org
Source0:        https://github.com/apache/qpid/archive/%{version}.tar.gz

Patch0:         mrg.patch
Patch1:         mrg-2.3.3-python.patch
Patch2:         mrg-2.4.4-python.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python-saslwrapper >= 0.10
BuildRequires:  python-devel

%description
The Apache Qpid Python client library for AMQP.


%prep
%setup -q -n qpid-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
cd qpid/python
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf %{buildroot}
cd qpid/python
%{__python} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/mllib
%{python_sitelib}/qpid
%{_bindir}/qpid-python-test
%doc qpid/python/LICENSE.txt qpid/python/NOTICE.txt qpid/python/README.txt qpid/python/examples/


%changelog
* Wed Jun 15 2016 Jeremy Cline <jcline@redhat.com> 0.18-10
- Import spec file
