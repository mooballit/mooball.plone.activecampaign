Managing Mailing Lists
======================

Setup
-----

We need to setup a browser for testing:

>>> from plone.testing.z2 import Browser
>>> browser = Browser(layer['app'])
>>> portal = layer['portal']
>>> portal_url = portal.absolute_url()

We log in as a manager:

>>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
>>> browser.addHeader('Authorization', 'Basic %s:%s' %(SITE_OWNER_NAME, SITE_OWNER_PASSWORD))


..  note::

    In order to test the tool, we're loading pre-defined data from the
    filesystem by using a helper function ``set_api_url_to_action``
    which sets the api_url of the tool to a text file.


Getting a list of Mailinglists
------------------------------

Getting a list of mailing lists invokes the ``list_list`` api action:

>>> set_api_url_to_action('list_list')

Once the administrator logs in, he can open the management interface:

>>> browser.handleErrors = False
>>> browser.open(portal_url + '/portal_activecampaign/@@managemailinglists')
>>> print browser.contents
<!DOCTYPE ...
...Manage Mailing Lists...
...BD TEST LIST...
