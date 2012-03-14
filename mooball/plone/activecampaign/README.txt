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


Managing the Tool
-----------------

We can go to the site setup and add API information:

>>> browser.handleErrors = False
>>> browser.open(portal_url)
>>> browser.getLink('Site Setup').click()
>>> browser.getLink('Active Campaign Setup').click()

Because the tool is not setup with any API information, we need to fill
out the management form first in order to retrieve any information:

>>> print browser.contents
<!DOCTYPE...
...The active campaign tool is not correctly set up...

Now we set up the tool by providing API information.

..  note::

    The information provided here is obviously only test information.
    You need to provide API details from campaign monitor. Esp. the API
    URL needs to be set to a server response with a helper method, so we
    fill only username and password.

>>> set_api_url_to_action('list_list')
>>> browser.getLink('fill in the API form').click()
>>> browser.getControl('API Username').value = 'roman'
>>> browser.getControl('API Password').value = 'secret'
>>> browser.getControl('Save').click()
>>> print browser.contents
<!DOCTYPE...
...Changes saved...

Listing Mailing Lists
---------------------

After providing the API information, we can see mailing list information
showing on the:

>>> browser.getLink('Active Campaign Setup').click()
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


Custom Fields
-------------

We can click on a mailing list to add custom fields:

>>> browser.getLink('BD TEST LIST').click()
>>> print browser.contents
<!DOCTYPE ...
...BD TEST LIST...
