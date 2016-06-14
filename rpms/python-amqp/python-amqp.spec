%global srcname amqp


Name:           python-%{srcname}
Version:        1.4.9
Release:        3%{?dist}

License:        LGPLv2+
Summary:        Low-level AMQP client for Python (fork of amqplib)
Group:          Development/Languages
URL:            https://github.com/celery/py-amqp
Source0:        https://github.com/celery/py-amqp/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose


%description
Low-level AMQP client for Python

This is a fork of amqplib, maintained by the Celery project.

This library should be API compatible with librabbitmq.


%prep
%setup -q -n py-%{srcname}-%{version}


%build
# Docs don't build on RHEL6, unfortunately, they are not built here
%py2_build


%install
%py2_install

# Remove execute bit from example scripts (packaged as doc)
chmod -x demo/*.py


%files
%license LICENSE
%doc AUTHORS Changelog README.rst demo/
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}*.egg-info


%changelog
* Mon Jun 13 2016 Jeremy Cline <jcline@redhat.com> - 1.4.9-3
- Remove documentation builds as this is a RHEL6-specific spec.

* Tue May 10 2016 Randy Barlow <rbarlow@redhat.com> - 1.4.9-2
- Remove conditionals from the spec file.
- Correct a date in the changelog.
- Move docs generation to the build step where it belongs.
- Use the py2 macros.
- Use the license macro.
- Add AUTHORS to the docs.

* Wed Feb 03 2016 Patrick Creech <pcreech@redhat.com> 1.4.9-1
- Upgrade python-amqp dep to 1.4.9 (pcreech@redhat.com)

* Fri Dec 18 2015 Brian Bouterse <bbouters@redhat.com> 1.4.7-1
- Upgrade python-amqp dep to 1.4.7 (sean.myers@redhat.com)

* Fri Dec 18 2015 Sean Myers <sean.myers@redhat.com> 1.4.7-1
- Upgrade python-amqp to 1.4.7 (sean.myers@redhat.com)

* Tue Dec 09 2014 Brian Bouterse 1.4.6-1
- Upgrade python-amqp to 1.4.6 (bbouters@redhat.com)

* Mon Apr 21 2014 Randy Barlow <rbarlow@redhat.com> 1.4.5-1
- Update to python-amqp-1.4.5. (rbarlow@redhat.com)

* Wed Mar 05 2014 Randy Barlow <rbarlow@redhat.com> 1.4.4-1
- Update to amqp-1.4.4. (rbarlow@redhat.com)
- Remove a duplicate block from the changelog on amqp. (rbarlow@redhat.com)

* Thu Feb 20 2014 Randy Barlow <rbarlow@redhat.com> 1.4.3-1
- Raise python-amqp to 1.4.3. (rbarlow@redhat.com)
- Merge pull request #787 from pulp/mhrivnak-deps (mhrivnak@hrivnak.org)
- Deleting dependencies we no longer need and adding README files to explain
  why we are keeping the others. (mhrivnak@redhat.com)
- Remove a stray space from python-amqp.spec (rbarlow@redhat.com)
- Don't build Python 3 versions of Celery and deps. (rbarlow@redhat.com)

* Mon Jan 27 2014 Randy Barlow <rbarlow@redhat.com> 1.3.3-1
- new package built with tito

* Fri Nov 15 2013 Eric Harney <eharney@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Fri Oct 25 2013 Eric Harney <eharney@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Tue Oct 08 2013 Eric Harney <eharney@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Fri Sep 20 2013 Eric Harney <eharney@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Eric Harney <eharney@redhat.com> - 1.0.11-1
- Initial package
