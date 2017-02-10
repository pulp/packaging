Prerequisites on running pulp on Openshift:

* Create a new namespace for Pulp

* Create a service account should be able to run container as root.

  Run the following commands on master:
  ```
  $ sudo su
  # oc project <namespace>
  # oc create serviceaccount pulp-sa
  # oc patch scc anyuid --type=json -p '[{"op": "add", "path": "/users/0", "value":"system:serviceaccount:<namespace>:pulp-sa"}]'
  ```
  (replace `<namespace>` with expected namespace)

* Ask the cluster admin to create necessary volumes in this namespace

  For local testing:
  ```
  $ sudo su
  # mkdir -p /volumes/crane-volume /volumes/etc-pki-pulp-volume /volumes/etc-pulp-volume /volumes/pulpapi-volume /volumes/var-lib-pulp-volume
  # chown nobody:nobody /volumes/*
  # chcon -u system_u -r object_r -t svirt_sandbox_file_t -l s0 /volumes/*
  # oc project <namespace>
  # ls *-volume.yaml | xargs -n1 oc create -f
  ```
  (replace `<namespace>` with expected namespace)

* Import the template

* Build and deploy QPID and DB:
  ```
  oc start-build mongodb
  oc start-build qpid
  oc start-build crane
  ```
* After both are done build base image to trigger the chain of pulp component builds and deploys:
  ```
  oc start-build base
  ```
