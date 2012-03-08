Introduction
============

This package integrates Plone with Active Campaign.

Setup
-----

We need the tool to perform any tasks:

>>> import zope.component
>>> from mooball.plone.activecampaign.interfaces import IActiveCampaignTool
>>> tool = zope.component.getUtility(IActiveCampaignTool)


..  note::

    Currently no exceptions will be raised if something goes wrong on
    during any call. The only way to see what's going on is to look in
    the error log (``var/log/instance.log``) of your Zope instance.

Subscribing new Users
---------------------

You can subscribe new users by creating a new ActiveCampaignSubscriber
first. It is enough to subscriber a user just with his e-mail address:

>>> from mooball.plone.activecampaign.tool import ActiveCampaignSubscriber
>>> subscriber = ActiveCampaignSubscriber('tom@mooball.net')
>>> tool.add_subscriber(subcriber, [1])
