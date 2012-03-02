# coding: utf-8
from setuptools import setup, find_packages
import os

version = '0.1'
tests_require = ['plone.app.testing']

setup(name='mooball.plone.activecampaign',
      version=version,
      description="Active Campaign integration",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "CHANGES.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Róman Joost',
      author_email='roman@mooball.net',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mooball', 'mooball.plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.directives.form',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      extras_require=dict(tests=tests_require),
      )
