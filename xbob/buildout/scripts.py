#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.dos.anjos@gmail.com>
# Mon  4 Feb 14:12:24 2013 

"""Builds custom interpreters with the right paths for external Bob
"""

import os
import logging
import zc.buildout
from . import tools
from .script import Recipe as Script

class PythonInterpreter(Script):
  """Creates a nice python interpreter on the bin directory"""
  
  def __init__(self, buildout, name, options):

    self.logger = logging.getLogger(name)

    interpreter = options.setdefault('interpreter', 'python')
    if options.has_key('scripts'): del options['scripts']
    options['scripts'] = interpreter
    options['dependent-scripts'] = 'false'
    Script.__init__(self, buildout, name, options)

  def install(self):

    return Script.install(self)

  update = install

class UserScripts(Script):
  """Installs all user scripts from the eggs"""

  def __init__(self, buildout, name, options):

    self.logger = logging.getLogger(name)

    if options.has_key('interpreter'): del options['interpreter']
    if options.has_key('scripts'): del options['scripts']
    Script.__init__(self, buildout, name, options)

  def install(self):

    return Script.install(self)

  update = install

class IPythonInterpreter(Script):
  """Installs all user scripts from the eggs"""

  def __init__(self, buildout, name, options):

    self.logger = logging.getLogger(name)
    
    interpreter = options.setdefault('interpreter', 'python')
    del options['interpreter']
    options['entry-points'] = 'i%s=IPython.frontend.terminal.ipapp:launch_new_instance' % interpreter
    options['scripts'] = 'i%s' % interpreter
    options['dependent-scripts'] = 'false'
    options.setdefault('panic', 'false')
    eggs = options.get('eggs', buildout['buildout']['eggs'])
    options['eggs'] = tools.add_eggs(eggs, ['nose'])
    Script.__init__(self, buildout, name, options)

  def install(self):

    return Script.install(self)

  update = install

class NoseTests(Script):
  """Installs Nose infrastructure"""

  def __init__(self, buildout, name, options):

    self.logger = logging.getLogger(name)
    
    # Initializes nosetests, if it is available - don't panic!
    if options.has_key('interpreter'): del options['interpreter']
    if options.has_key('nose-flags'):
      # use 'options' instead of 'options' to force use
      flags = tools.parse_list(options['nose-flags'])
      init_code = ['sys.argv.append(%r)' % k for k in flags]
      options['initialization'] = '\n'.join(init_code)
    options['entry-points'] = 'nosetests=nose:run_exit'
    options['scripts'] = 'nosetests'
    options['dependent-scripts'] = 'false'
    options.setdefault('panic', 'false')
    eggs = options.get('eggs', buildout['buildout']['eggs'])
    options['eggs'] = tools.add_eggs(eggs, ['nose'])
    Script.__init__(self, buildout, name, options)

  def install(self):

    return Script.install(self)

  update = install

class Sphinx(Script):
  """Installs the Sphinx documentation generation infrastructure"""

  def __init__(self, buildout, name, options):

    self.logger = logging.getLogger(name)
    
    # Initializes the sphinx document generator - don't panic!
    if options.has_key('interpreter'): del options['interpreter']
    options['scripts'] = '\n'.join([
      'sphinx-build',
      'sphinx-apidoc', 
      'sphinx-autogen', 
      'sphinx-quickstart',
      ])
    if options.has_key('entry-points'): del options['entry-points']
    options.setdefault('panic', 'false')
    options['dependent-scripts'] = 'false'
    eggs = options.get('eggs', buildout['buildout']['eggs'])
    options['eggs'] = tools.add_eggs(eggs, ['sphinx'])
    Script.__init__(self, buildout, name, options)

  def install(self):

    return Script.install(self)

  update = install

class Recipe(object):
  """Just creates a given script with the "correct" paths
  """

  def __init__(self, buildout, name, options):

    self.logger = logging.getLogger(name.capitalize())

    self.python = PythonInterpreter(buildout, 'Python', options.copy())
    self.scripts = UserScripts(buildout, 'Scripts', options.copy())
    self.ipython = IPythonInterpreter(buildout, 'IPython', options.copy())
    self.nose = NoseTests(buildout, 'Nose', options.copy())
    self.sphinx = Sphinx(buildout, 'Sphinx', options.copy())

  def install(self):
    return \
        self.python.install() + \
        self.scripts.install() + \
        self.ipython.install() + \
        self.nose.install() + \
        self.sphinx.install()

  update = install
