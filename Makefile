.PHONY: all help srpm mock-build copr-build clean


SRPM_DIR=${PWD}/SRPMS/
RPM_DIR=${PWD}/RPMS/
SPECS_DIR=${PWD}/rpms/
DEFAULT_CHROOT=epel-5-x86_64
CHROOTS = epel-5-x86_64 epel-5-i386

# The important dependencies are:
# 	python-kombu BuildRequires python-amqp
BUILD_ORDER = gofer \
			  pulp \
			  pulp-puppet \
			  pulp-rpm \
			  python-isodate \
			  python-qpid \
			  saslwrapper

all: help


help:
	@echo "Usage: make <target>"
	@echo "Available targets are:"
	@echo " srpm                    build srpms in the ${DEFAULT_CHROOT} mock root"
	@echo " copr-build              build rpms in COPR; defaults to building in the ${CHROOTS}"
	@echo "                         chroots (define CHROOTS to override)"
	@echo " mock-build              build rpms in the ${DEFAULT_CHROOT} mock root"
	@echo " clean                   remove all build files"



srpm:
	# Build each SRPM in a mock root
	# Skips if the files in SRPMS/ equal the dirs in rpms/
	mkdir -p ${SRPM_DIR}
	if [ $$(ls -l rpms | wc -l) -ne $$(ls -l SRPMS | wc -l) ]; then \
		for p in $$(ls rpms); do \
			scripts/build-srpm.sh ${DEFAULT_CHROOT} $${p} || exit 1 ; \
		done; \
		rm ${SRPM_DIR}*log; \
	fi


mock-build: srpm
	# The current user should be part of the ``mock`` group
	#
	# Build leaf dependencies first and install them in the chroot
	# in order to avoid build dependency problems.
	mkdir -p ${RPM_DIR}
	for p in ${BUILD_ORDER}; do \
		PACKAGE=$$(ls SRPMS/ | grep "$${p}-[0-9]"); \
		echo "Building $${PACKAGE}"; \
		mock -r ${DEFAULT_CHROOT} --no-clean --resultdir ${RPM_DIR} SRPMS/"$${PACKAGE}" || exit 1 ; \
	done


copr-build: srpm
	# Specify variables with VARIABLE=value. For example:
	# ``make copr-build PROJECT=2.8-nightly``
	for c in ${CHROOTS} ; do \
		for p in ${BUILD_ORDER}; do \
			PACKAGE=$$(ls SRPMS/ | grep "$${p}-[0-9]"); \
			echo "Building $${PACKAGE}"; \
			copr-cli build --nowait -r $${c} "@pulp/${PROJECT}" SRPMS/"$${PACKAGE}"; \
		done ; \
	done


clean:
	rm -rf ${SRPM_DIR} ${RPM_DIR}
	find . -name "*.tar.gz" -delete
	mock --clean
