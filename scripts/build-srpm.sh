#!/usr/bin/env bash
#
# Builds an SRPM from the spec file found in the directory provided
# and any patches in the "sources" sub-directory
set -e

CHROOT=${1}
PACKAGE_NAME=${2}
PACKAGE_SPEC="${PACKAGE_NAME}.spec"

RESULT_DIR=${PWD}/SRPMS
mkdir -p "${RESULT_DIR}"

pushd "rpms/${PACKAGE_NAME}"

# Since the tarballs aren't checked into source control, download them
ARCHIVE_URL=$(rpmspec -P "${PACKAGE_SPEC}" | grep "Source0" | awk '{print $2}')
echo "Downloading archive from ${ARCHIVE_URL}"
mkdir -p sources
pushd sources
curl -sOL "${ARCHIVE_URL}"
popd

# Build the SRPM in the mock root
mock --no-clean -r "${CHROOT}" --buildsrpm --spec "${PACKAGE_SPEC}" --sources sources --resultdir "${RESULT_DIR}"
