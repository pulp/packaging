.PHONY: all help srpm mock-build copr-build clean


SRPM_DIR=${PWD}/SRPMS/
SPECS_DIR=${PWD}/rpms/
CHROOT=fedora-23-x86_64


all: help


help:
	echo "Usage: make <target>"
	echo
	echo "Available targets are:"
	echo " clean                   all files not tracked by git (`git clean -df`)"
	echo " srpm                    build srpms"
	echo " copr-build              build rpms in COPR"
	echo " mock-build              build rpms in the default mock root"



srpm:
	# Skips if the files in SRPMS/ equal the dirs in rpms/
	mkdir -p SRPMS
	if [ $$(ls -l rpms | wc -l) -ne $$(ls -l SRPMS | wc -l) ]; then \
		for p in $$(ls rpms); do \
			pushd "${SPECS_DIR}$${p}" && \
			ARCHIVE_URL=$$(rpmspec -P "$${p}".spec | grep "Source0" | awk '{print $$2}') && \
			echo "Downloading archive from $${ARCHIVE_URL}" && \
			curl -sOL "$${ARCHIVE_URL}" && \
			rpmbuild -D="_topdir $${PWD}" -D="_specdir $${PWD}" -D="_sourcedir $${PWD}" \
				-D="_srcrpmdir ${SRPM_DIR}" -D="_rpmdir $${PWD}" -D="_builddir $${PWD}" \
				-bs "$${p}.spec" && \
			echo "" && \
			popd ; \
		done \
	fi


mock-build: srpm
	# The current user should be part of the ``mock`` group
	#
	# Build leaf dependencies first and install them in the chroot
	# in order to avoid build dependency problems.
	mkdir -p RPMS
	mock --resultdir RPMS SRPMS/python-amqp*src.rpm
	rm SRPMS/python-amqp*src.rpm

	mock -i RPMS/*rpm
	mock --no-clean --resultdir RPMS SRPMS/python-kombu*src.rpm
	rm SRPMS/python-kombu*src.rpm

	mock -i RPMS/*rpm
	mock --no-clean --resultdir RPMS SRPMS/python-pymongo*src.rpm
	rm SRPMS/python-pymongo*src.rpm

	mock -i RPMS/*rpm
	mock --no-clean --resultdir RPMS SRPMS/python-mongoengine*src.rpm
	rm SRPMS/python-mongoengine*src.rpm


	for srcrpm in $$(ls SRPMS); do \
		mock -i RPMS/*rpm ; \
		mock --no-clean --resultdir RPMS SRPMS/$$srcrpm ; \
	done


copr-build: srpm
	# Specify variables with VARIABLE=value. For example:
	# ``make copr-build PROJECT=2.8-nightly``
	copr-cli build -r ${CHROOT} "@pulp/${PROJECT}" SRPMS/*rpm


clean:
	git clean -df
	mock --clean
