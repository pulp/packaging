# Fix private-shared-object-provides error
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

Name:           python-pymongo
Version:        3.2.2
Release:        2%{?dist}

# All code is ASL 2.0 except bson/time64*.{c,h} which is MIT
License:        ASL 2.0 and MIT
Summary:        Python driver for MongoDB
URL:            http://api.mongodb.org/python
Source0:        https://github.com/mongodb/mongo-python-driver/archive/%{version}.tar.gz
Patch01:        0001-Serverless-test-suite-workaround.patch
# This patch removes the bundled ssl.match_hostname library as it was vulnerable to CVE-2013-7440
# and CVE-2013-2099, and wasn't needed anyway since Fedora >= 22 has the needed module in the Python
# standard library. It also adjusts imports so that they exclusively use the code from Python.
Patch02:        0002-Use-ssl.match_hostname-from-the-Python-stdlib.patch

BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  python-tools
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

# Mongodb must run on a little-endian CPU (see bug #630898)
ExcludeArch:    ppc ppc64 %{sparc} s390 s390x


%description
The Python driver for MongoDB.


%package doc
Summary: Documentation for python-pymongo


%description doc
Documentation for python-pymongo.


%package -n python2-bson
Summary:        Python bson library
%{?python_provide:%python_provide python2-bson}


%description -n python2-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.


%package -n python3-bson
Summary:        Python bson library
%{?python_provide:%python_provide python3-bson}


%description -n python3-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.  This package
contains the python3 version of this module.


%package -n python2-pymongo
Summary:        Python driver for MongoDB

Requires:       python2-bson = %{version}-%{release}
Provides:       pymongo = %{version}-%{release}
Obsoletes:      pymongo <= 2.1.1-4
%{?python_provide:%python_provide python2-pymongo}


%description -n python2-pymongo
The Python driver for MongoDB.  This package contains the python2 version of
this module.


%package -n python3-pymongo
Summary:        Python driver for MongoDB
Requires:       python3-bson = %{version}-%{release}
%{?python_provide:%python_provide python3-pymongo}


%description -n python3-pymongo
The Python driver for MongoDB.  This package contains the python3 version of
this module.


%package -n python2-pymongo-gridfs
Summary:        Python GridFS driver for MongoDB
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       pymongo-gridfs = %{version}-%{release}
Obsoletes:      pymongo-gridfs <= 2.1.1-4
%{?python_provide:%python_provide python2-pymongo-gridfs}


%description -n python2-pymongo-gridfs
GridFS is a storage specification for large objects in MongoDB.


%package -n python3-pymongo-gridfs
Summary:        Python GridFS driver for MongoDB
Requires:       python3-pymongo%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-pymongo-gridfs}


%description -n python3-pymongo-gridfs
GridFS is a storage specification for large objects in MongoDB.  This package
contains the python3 version of this module.


%prep
%setup -q -n mongo-python-driver-%{version}
%patch01 -p1 -b .test
%patch02 -p1 -b .ssl

rm -rf %{py3dir}
cp -a . %{py3dir}


%build
CFLAGS="%{optflags}" %{__python2} setup.py build

pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd

pushd doc
make html
popd


%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
# Fix permissions
chmod 755 %{buildroot}%{python2_sitearch}/bson/*.so
chmod 755 %{buildroot}%{python2_sitearch}/pymongo/*.so

pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
# Fix permissions
chmod 755 %{buildroot}%{python3_sitearch}/bson/*.so
chmod 755 %{buildroot}%{python3_sitearch}/pymongo/*.so
popd


%files doc
%license LICENSE
%doc doc/_build/html/*


%files -n python2-bson
%license LICENSE
%doc README.rst
%{python2_sitearch}/bson


%files -n python3-bson
%license LICENSE
%doc README.rst
%{python3_sitearch}/bson


%files -n python2-pymongo
%license LICENSE
%doc README.rst
%{python2_sitearch}/pymongo
%{python2_sitearch}/pymongo-%{version}-*.egg-info


%files -n python3-pymongo
%license LICENSE
%doc README.rst
%{python3_sitearch}/pymongo
%{python3_sitearch}/pymongo-%{version}-*.egg-info


%files -n python2-pymongo-gridfs
%license LICENSE
%doc README.rst
%{python2_sitearch}/gridfs


%files -n python3-pymongo-gridfs
%license LICENSE
%doc README.rst
%{python3_sitearch}/gridfs


%check
# Exclude tests that require an active MongoDB connection
 exclude='(^test_auth_from_uri$'
exclude+='|^test_auto_auth_login$'
exclude+='|^test_auto_reconnect_exception_when_read_preference_is_secondary$'
exclude+='|^test_auto_start_request$'
exclude+='|^test_binary$'
exclude+='|^test_client$'
exclude+='|^test_collection$'
exclude+='|^test_common$'
exclude+='|^test_config_ssl$'
exclude+='|^test_connect$'
exclude+='|^test_connection$'
exclude+='|^test_constants$'
exclude+='|^test_contextlib$'
exclude+='|^test_copy_db$'
exclude+='|^test_cursor$'
exclude+='|^test_crud$'
exclude+='|^test_database$'
exclude+='|^test_database_names$'
exclude+='|^test_delegated_auth$'
exclude+='|^test_disconnect$'
exclude+='|^test_discovery_and_monitoring$'
exclude+='|^test_document_class$'
exclude+='|^test_drop_database$'
exclude+='|^test_equality$'
exclude+='|^test_fork$'
exclude+='|^test_from_uri$'
exclude+='|^test_fsync_lock_unlock$'
exclude+='|^test_get_db$'
exclude+='|^test_getters$'
exclude+='|^test_grid_file$'
exclude+='|^test_gridfs$'
exclude+='|^test_host_w_port$'
exclude+='|^test_interrupt_signal$'
exclude+='|^test_ipv6$'
exclude+='|^test_iteration$'
exclude+='|^test_json_util$'
exclude+='|^test_kill_cursor_explicit_primary$'
exclude+='|^test_kill_cursor_explicit_secondary$'
exclude+='|^test_master_slave_connection$'
exclude+='|^test_nested_request$'
exclude+='|^test_network_timeout$'
exclude+='|^test_network_timeout_validation$'
exclude+='|^test_operation_failure_with_request$'
exclude+='|^test_operation_failure_without_request$'
exclude+='|^test_operations$'
exclude+='|^test_pinned_member$'
exclude+='|^test_pooling$'
exclude+='|^test_pooling_gevent$'
exclude+='|^test_properties$'
exclude+='|^test_pymongo$'
exclude+='|^test_read_preferences$'
exclude+='|^test_replica_set_client$'
exclude+='|^test_replica_set_connection$'
exclude+='|^test_replica_set_connection_alias$'
exclude+='|^test_repr$'
exclude+='|^test_request_threads$'
exclude+='|^test_safe_insert$'
exclude+='|^test_safe_update$'
exclude+='|^test_schedule_refresh$'
exclude+='|^test_server_disconnect$'
exclude+='|^test_server_selection$'
exclude+='|^test_server_selection_rtt$'
exclude+='|^test_son_manipulator$'
exclude+='|^test_threading$'
exclude+='|^test_threads$'
exclude+='|^test_threads_replica_set_connection$'
exclude+='|^test_timeouts$'
exclude+='|^test_tz_aware$'
exclude+='|^test_uri_options$'
exclude+='|^test_use_greenlets$'
exclude+='|^test_with_start_request$'
exclude+='|^test_command_monitoring_spec$'
exclude+='|^test_gridfs_spec$'
exclude+='|^test_uri_spec$'
exclude+='|^test_legacy_api$'
exclude+='|^test_raw_bson$'
exclude+=')'
pushd test
nosetests --exclude="$exclude"
popd


%changelog
* Wed May 11 2016 Randy Barlow <rbarlow@redhat.com> - 3.2.2-2
- Depend on python-sphinx instead of python2-sphinx.

* Tue Mar 15 2016 Randy Barlow <rbarlow@redhat.com> - 3.2.2-1
- Update to 3.2.2 (#1318073).

* Wed Feb 03 2016 Randy Barlow <rbarlow@redhat.com> - 3.2.1-1
- Remove use of needless defattr macros (#1303426).
- Update to 3.2.1 (#1304137).
- Remove lots of if statements as this spec file will only be used on Rawhide.
- Remove dependency on python-backports-ssl_match_hostname as it is not needed in Fedora.
- Rework the patch for CVE-2013-7440 and CVE-2013-2099 so that it exclusively uses code from Python.

* Tue Jan 19 2016 Randy Barlow <rbarlow@redhat.com> - 3.2-1
- Update to 3.2.
- Rename the python- subpackages with a python2- prefix.
- Add a -doc subpackage with built html docs.
- Skip a few new tests that use MongoDB.
- Reorganize the spec file a bit.
- Use the license macro.
- Pull source from GitHub.

* Mon Jan 18 2016 Randy Barlow <rbarlow@redhat.com> - 3.0.3-3
- Do not use 2to3 for Python 3 (#1294130).

* Wed Nov 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.0.3-2
- Rebuilt for Python 3.5

* Thu Oct 01 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 3.0.3-1
- Upstream 3.0.3
- Fix CVE-2013-7440 (RHBZ#1231231 #1231232)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.2-2
- Bump the obsoletes version for pymongo-gridfs

* Wed Jun 12 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.2-1
- Update to pymongo 2.5.2

* Tue Jun 11 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-5
- Bump the obsoletes version

* Wed Apr 24 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-4
- Fix the test running procedure

* Wed Apr 24 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-3
- Exclude tests in pymongo 2.5 that depend on MongoDB

* Mon Apr 22 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-1
- Update to PyMongo 2.5 (bug #954152)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan  5 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-6
- Fix dependency of python3-pymongo-gridfs (bug #892214)

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-5
- Fix the name of the python-pymongo-gridfs subpackage

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-4
- Fix obsoletes for python-pymongo-gridfs subpackage

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-3
- Fix requires to include the arch, and add docs to all subpackages

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-2
- Remove preexisting egg-info

* Mon Nov 26 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-1
- Rename, update to 2.3, and add support for Python 3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Silas Sewell <silas@sewell.org> - 2.1.1-1
- Update to 2.1.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 1.11-1
- Update to 1.11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Dan Horák <dan[at]danny.cz> - 1.9-5
- add ExcludeArch to match mongodb package

* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 1.9-4
- Add comment about multi-license

* Thu Oct 21 2010 Silas Sewell <silas@sewell.ch> - 1.9-3
- Fixed tests so they actually run
- Change python-devel to python2-devel

* Wed Oct 20 2010 Silas Sewell <silas@sewell.ch> - 1.9-2
- Add check section
- Use correct .so filter
- Added python3 stuff (although disabled)

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.9-1
- Update to 1.9

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.8.1-1
- Update to 1.8.1

* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.1.2-1
- Initial build
