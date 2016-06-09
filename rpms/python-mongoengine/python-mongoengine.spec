%define srcname mongoengine


Name:           python-%{srcname}
Version:        0.10.5
Release:        3%{?dist}
BuildArch:      noarch

License:        MIT
Group:          Development/Libraries
Summary:        A Python Document-Object Mapper for working with MongoDB
URL:            https://github.com/MongoEngine/mongoengine
Source0:        https://github.com/MongoEngine/mongoengine/archive/v%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-blinker
Requires:       python-pymongo >= 3.2
Requires:       python-pymongo-gridfs >= 3.2


%description
MongoEngine is an ORM-like layer on top of PyMongo.


%prep
%setup -q -n %{srcname}-%{version}


%build
%py2_build


%install
%py2_install


%files
%license LICENSE
%doc docs AUTHORS README.rst
%{python_sitelib}/*


%changelog
* Tue Jun 07 2016 Jeremy Cline <jcline@redhat.com> - 0.10.5-3
- Fix dependencies for EL7

* Tue May 10 2016 Randy Barlow <rbarlow@redhat.com> - 0.10.5-2
- Remove conditionals.
- Use new Python and license macros.
- Remove unneeded build dependencies.

* Fri Jan 22 2016 Ina Panova <ipanova@redhat.com> - 0.10.5-1
- Updated to mongoengine to 0.10.5
- Remove patch that is not currently used as check phase is disabled

* Thu Jun 18 2015 Brian Bouterse <bbouters@redhat.com> - 0.9.0-1
- Updated to mongoengine to 0.9.0
- Created new patch to remove Pillow as a test requirement

* Wed Feb 18 2015 Yohan Graterol <yohangraterol92@gmail.com> - 0.8.4-3
- Built for EPEL7
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Yohan Graterol <yohangraterol92@gmail.com> - 0.8.4-1
- New Version
* Mon Aug 12 2013 Yohan Graterol <yohangraterol92@gmail.com> - 0.8.3-1
- New version
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 0.7.9-5
- Fix setup.py (add python-pillow instead python-imaging)

* Mon Jan 28 2013 Yohan Graterol <yohangraterol92@gmail.com> - 0.7.9-4
- Add Requires: pymongo, python-gridfs for f17
- Add Requires: python-pymongo, python-pymongo-gridfs for f18+
- Add Requires: python-blinker, python-imaging

* Sun Jan 27 2013 Yohan Graterol <yohangraterol92@gamil.com> - 0.7.9-3
- Built and included test
- Add BuildRequires: python-django >= 1.3

* Sun Jan 27 2013 Yohan Graterol <yohangraterol92@gmail.com> - 0.7.9-2
- Built and included sphinx docs
- Add BuildRequires: python-sphinx, python-pymongo, pymongo-gridfs
- Add BuildRequires: python-coverage, python-nose

* Thu Jan 17 2013 Yohan Graterol <yohangraterol92@gmail.com> - 0.7.9-1
- Initial packaging
