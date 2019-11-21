Developing
==========

To develop, we suggest using `virtual environments <https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>`__ together with ``pip`` or using `pipenv <https://pipenv.readthedocs.io/en/latest/>`__. Once the environment is activated, clone the repo from GitHub

.. code-block:: console

    git clone https://github.com/scikit-hep/pyhf.git

and install all necessary packages for development

.. code-block:: console

    python -m pip install --ignore-installed -U -e .[complete]

Then setup the Git pre-commit hook for `Black <https://github.com/psf/black>`__  by running

.. code-block:: console

    pre-commit install

Publishing
----------

Publishing to `PyPI <https://pypi.org/project/pyhf/>`__ and `TestPyPI <https://test.pypi.org/project/pyhf/>`__
is automated through the `PyPA's PyPI publish GitHub Action <https://github.com/pypa/gh-action-pypi-publish>`__.
Publishing a release to PyPI begins with creating a new branch :code:`release/cut-<release tag>`
and then from that branch running

.. code-block:: console

    bumpversion [major|minor|patch]

to update the release version and get a tagged commit.
Then, push only the branch to GitHub and open a PR to ensure that the code
you are going to publish is indeed stable.
Once the PR has passed all checks and has been approved, a maintainer should merge
the branch from the command line

.. code-block:: console

    git checkout master
    git merge release/cut-<release tag>

and then push the commit and tag to :code:`master` with

.. code-block:: console

    git push origin master <release tag>

which will both merge and close the PR and start the release publication workflow.
