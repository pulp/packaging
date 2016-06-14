Name: python-semantic_version
Version: 2.2.0
Release: 6%{?dist}
Summary: A library implementing the 'SemVer' scheme.

License: BSD
URL: https://github.com/rbarrois/python-semanticversion
Source0: https://github.com/rbarrois/python-semanticversion/archive/v%{version}.tar.gz
BuildArch: noarch

Provides: python-semantic-version = %{version}-%{release}
Obsoletes: python-semantic-version < %{version}-%{release}

BuildRequires: python2-devel

%description
This small python library provides a few tools to handle SemVer
(http://semver.org) in Python. It follows strictly the 2.0.0-rc1 version of the
SemVer scheme.

%prep
%setup -q -n python-semanticversion-%{version}


%build
%py2_build


%install
%py2_install


%files
%license LICENSE
%doc README
%{python_sitelib}/semantic_version
%{python_sitelib}/semantic_version*.egg-info


%changelog
* Wed Jan 06 2016 Ina Panova <ipanova@redhat.com> 2.2.0-6
- Adding Provides/Obsoletes for python-semantic-version package.
  (ipanova@redhat.com)

* Wed Jan 06 2016 Ina Panova <ipanova@redhat.com> 2.2.0-5
- Fix python-semantic_version build (ipanova@redhat.com)

* Tue Jan 05 2016 Ina Panova <ipanova@redhat.com> 2.2.0-4
- Rebuild python-semantic_version for 2.2.0-4

* Wed Sep 11 2013 Jeff Ortel <jortel@redhat.com> 2.2.0-3
- comment out the unit tests in python-semantic-version. too much of a pain to
  add the dep in brew.  We can uncomment later. (jortel@redhat.com)

* Wed Sep 11 2013 Jeff Ortel <jortel@redhat.com> 2.2.0-2
- add buildrequires: python-unittest2. (jortel@redhat.com)

* Tue Sep 10 2013 Jeff Ortel <jortel@redhat.com> 2.2.0-1
- new package built with tito



