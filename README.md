# OCI Utilities Example 

## [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/)

[Python API](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/)

This example code will get you started accessing OCI Networking and Compute 
information using the OCI Python API. Follow the above instructions 
referenced in the link above.  


## Capabilities

The following Web actions are supported:

* Show Compute Instances
* Show VCNs
* Show VCN Subnets
* Show VNIC Attachments
* Show VCN & Attached Compute Summary
* Show Configuration
* Show User

## Implementation

This is coded as a Flask app with Python 3 as a prerequisite. 

Set up a proper virtual env, activate it, 
and install the requirements in your virtual env:

    my-machine $ python -m venv venv
    my-machine $ source venv/bin/activate
    (venv) my-machine $ pip install -f requirements.txt


Start the local web server:

    (venv) my-machine $ source start_server.sh
     * Serving Flask app "app/views.py" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!

Access from local browser:

    http://127.0.0.1:5000/
