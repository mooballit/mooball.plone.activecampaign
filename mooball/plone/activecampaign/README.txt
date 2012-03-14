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


Listing Mailing Lists
---------------------

Getting a list of mailing lists invokes the ``list_list`` api action:

>>> set_api_url_to_action('list_list')

Once the administrator logs in, he can open the management interface:

>>> browser.handleErrors = False
>>> browser.open(portal_url + '/portal_activecampaign/@@managemailinglists')
>>> print browser.contents
<!DOCTYPE ...
...Manage Mailing Lists...
...BD TEST LIST...


Deleting Mailing Lists
----------------------

The overview can be used to delete mailing lists by selecting each which
should be deleted:

>>> set_api_url_to_action('list_delete_list')
>>> browser.getControl(name='delete:list', index=0).value = ['2']
>>> browser.getControl('Delete Selected').click()
>>> print browser.contents
<!DOCTYPE ...
...Successfully deleted list(s)...


Custom Fields
-------------

We can click on a mailing list to add custom fields:

>>> browser.getLink('BD TEST LIST').click()
>>> print browser.contents
<!DOCTYPE ...
...BD TEST LIST...
