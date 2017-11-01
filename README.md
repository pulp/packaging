Pulp Packaging
==============

DEPRECATED
----------
This repo is being deprecated in favor of pulp-packaging.  Over the 2.15 cycle, relevant items
will be moved over to pulp-packaging


This repository contains code relevant to distributing Pulp through packaging formats. It currently
supports distributing Pulp through RPMs and Docker images.


RPMS
----

This repository uses branching to differentiate spec files for different RPM Linux distributions.
Within each rpm branch you will find a folder called rpms, and within that folder will be a
subfolder named after each package that Pulp distributes in its repositories. Pulp uses the branches
f23, el7, el6, and el5 to contain the packages that Pulp distributes for Fedora 23, EL 7, EL 6 and
EL 5, respectively.
