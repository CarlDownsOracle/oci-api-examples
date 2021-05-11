# OCI Utilities Example 

## [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/)

[Python API](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/)

This example code will get you started accessing OCI Networking and Compute 
information using the OCI Python API. Follow the above instructions 
referenced in the link above.  


## Capabilities

This is coded as a Flask app.  The following actions are supported:

* Show Compute Instances
* Show VCNs
* Show VCN Subnets
* Show VNIC Attachments
* Show VCN & Attached Compute Summary
* Show Configuration
* Show User


Python 3 is required. Make sure you set up a proper virtual env, activate it, 
and install the requirements in your virtual env:

    my-machine $ python -m venv venv
    my-machine $ source venv/bin/activate
    (venv) my-machine $ pip install -f requirements.txt
    (venv) source start_server.sh

Start the local web server:

    (venv) my-machine $ flask run
     * Serving Flask app "app/views.py" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!

## Compartment vs Tenancy

<code>compartment</code> OCID is not required in the OCI config file.  However, this code
is looking for it as the main determiner of scope for your calls to OCI.  if
<code>compartment</code> is not defined, it will fall back to <code>tenancy</code>.
if you try to run this against an entire tenancy, you may get some 'not authorized' error codes, depending on
the level of access of your credentials.

