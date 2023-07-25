.. _codestandards:

Conform to best practices
=========================

We follow these practices when developing Raspberry IO code:

#. We generally follow the `git flow
   <http://nvie.com/posts/a-successful-git-branching-model/>`_ model
   of development, which means most of your work will be on a feature
   branch off the ``develop`` branch.

#. Follow :pep:`8` style conventions. Use 4 spaces instead of tabs.

   * To learn more about writing 'pythonic' code, check out
     The Hitchhiker's Guide To Python's `Code Style guide <http://docs.python-guide.org/en/latest/writing/style.html>`_

   * Tip: `Configure your development environment for python <http://docs.python-guide.org/en/latest/dev/env.html>`_
     to make your life a bit easier.

#. Use CapitalizedCase for class names, underscored_words for method names.

#. Code using ``os.path`` must be Windows and 'NIX friendly. For example,
   don't use backslashes (``\``) as path separators.

#. Be sure every class and method has `docstrings <http://docs.python-guide.org/en/latest/writing/documentation.html#code-documentation-advice>`_.

#. Use Python logging whenever an error or exception occurs.
   Optionally include debug-level logging.

#. Write a `test <http://docs.python-guide.org/en/latest/writing/tests.html>`_
   which shows that the bug was fixed or that the feature works as expected.

#. Run the test suite to make sure nothing unexpected broke. We only
   accept pull requests with passing tests.

#. Write new or update existing :ref:`documentation <documentation>`
   to describe the changes you made.

#. Add the change to the `CHANGELOG <https://github.com/python/raspberryio/blob/develop/docs/CHANGELOG.rst>`_
   for the **next** release.

#. Add your name to the `AUTHORS file
   <https://github.com/python/raspberryio/blob/develop/AUTHORS>`_

#. Submit a `pull request <https://help.github.com/articles/using-pull-requests>`_
   and get reviews before merging your changes, even if you have authority to
   merge the changes yourself.


.. _PEP-8: http://www.python.org/dev/peps/pep-0008/
