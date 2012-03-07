Introduction
============

This package integrates Plone with Active Campaign.

Development
-----------

To setup your development environment you'll need to create your own
buildout.cfg with a test environment, e.g::

    [buildout]
    extends = profiles/base.cfg

    [testenv]
    api_url = http://mailer.mydomain.com.au/admin/api.php
    api_user = admin
    api_password = secretpassword
