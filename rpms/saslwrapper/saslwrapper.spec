%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

Name:           saslwrapper
Version:        0.10
Release:        8%{?dist}
Summary:        Ruby and Python wrappers for the cyrus sasl library.
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            https://qpid.apache.org
Source0:        https://github.com/apache/qpid/archive/%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         bz638775.patch

BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python
BuildRequires: python-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
BuildRequires: swig

%description
A simple wrapper for cyrus-sasl that permits easy binding into
scripting languages.

%package devel
Summary: Header files for developing with saslwrapper.
Group: System Environment/Libraries
Requires: %name = %version-%release

%description devel
The header files for developing with saslwrapper.

%package -n python-saslwrapper
Summary: Python bindings for saslwrapper.
Group: System Environment/Libraries
Requires: %name = %version-%release
Requires: python

%description -n python-saslwrapper
Python bindings for the saslwrapper library.

%package -n ruby-saslwrapper
Summary: Ruby bindings for saslwrapper.
Group: System Environment/Libraries
Requires: %name = %version-%release
Requires: ruby

%description -n ruby-saslwrapper
Ruby bindings for the saslwrapper library.


%prep
%setup -q -n qpid-%{version}
cd qpid/extras/sasl
%patch0


%build
cd qpid/extras/sasl
./bootstrap
%configure
make %{?_smp_mflags}


%install
cd qpid/extras/sasl
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name "*.la" | xargs rm


%clean
rm -rf %{buildroot}


%check
cd qpid/extras/sasl
make check


%files
%defattr(-,root,root,-)
%doc qpid/extras/sasl/LICENSE
%_libdir/libsaslwrapper.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%doc qpid/extras/sasl/LICENSE
%_libdir/libsaslwrapper.so
%_includedir/saslwrapper.h

%files -n python-saslwrapper
%defattr(-,root,root,-)
%doc qpid/extras/sasl/LICENSE
%python_sitearch/saslwrapper.py*
%python_sitearch/_saslwrapper.so

%files -n ruby-saslwrapper
%defattr(-,root,root,-)
%doc qpid/extras/sasl/LICENSE
%ruby_sitearch/saslwrapper.so

%changelog
* Thu Jun 16 2016 Jeremy Cline <jcline@redhat.com> 0.10-8
- Import spec file
