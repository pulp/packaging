%global sum A WSGI app providing a docker-registry-like API with redirection
%global desc This WSGI application exposes a read-only API similar to \
docker-registry, which docker can use for "docker pull" operations. \
Requests for actual image files are responded to with 302 redirects to \
a URL formed with per-repository settings.


Name: python-crane
Version: 2.0.0
Release: 1%{?dist}

License:   GPLv2+
Summary:   %{sum}
URL:       https://github.com/pulp/crane
Source0:   https://github.com/pulp/crane/archive/python-crane-%{version}-1.tar.gz
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools


%description
%desc


%package -n python2-crane
Summary: %{sum}
Requires: python-flask >= 0.9
Requires: python-rhsm
Requires: python-setuptools
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

# This upstream issue tracks the bundling of fonts: https://pulp.plan.io/issues/1516
# Until that is resolved, we will mark the fonts as bundled.
Provides: bundled(fontawesome-fonts-web)
Provides: bundled(open-sans-fonts)
# This font does not seem to be in Fedora, so I'm guessing at its name. Accoding to
# https://www.patternfly.org/styles/typography/ it is licensed Creative Commons Attribution 4.0
# International license.
Provides: bundled(patternflyicons-fonts-web)
%{?python_provide:%python_provide python2-crane}


%description -n python2-crane
%desc


%prep
%autosetup -n crane-python-crane-%{version}-1


%build
%py2_build


%install
%py2_install

install -d %{buildroot}/%{_datadir}/crane/
install -d %{buildroot}/%{_var}/lib/crane/metadata/

install -pm644 deployment/crane.wsgi %{buildroot}/%{_datadir}/crane/

install -pm644 deployment/apache24.conf %{buildroot}/%{_datadir}/crane/apache.conf
install -pm644 deployment/crane.wsgi %{buildroot}/%{_datadir}/crane/


%files -n python2-crane
%license COPYRIGHT LICENSE
%doc AUTHORS README.rst
%{python2_sitelib}/crane
%{python2_sitelib}/crane*.egg-info
%{_datadir}/crane/
%dir %{_var}/lib/crane/


%post
if /usr/sbin/selinuxenabled; then
    semanage fcontext -a -t httpd_sys_content_t '%{_var}/lib/crane(/.*)?'
    restorecon -R -v %{_var}/lib/crane
fi


%postun
if [ $1 -eq 0 ] ; then  # final removal
    if /usr/sbin/selinuxenabled; then
        semanage fcontext -d -t httpd_sys_content_t '%{_var}/lib/crane(/.*)?'
        restorecon -R -v %{_var}/lib/crane
    fi
fi


%changelog
* Mon May 09 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-1
- Initial import from Fedora 24.
