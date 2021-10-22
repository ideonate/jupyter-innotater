.. _installation:

Installation
------------

Install from PyPi (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install jupyter_innotater

To enable in JupyterLab (version 3.0+):

::

    jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-innotater


Development install
~~~~~~~~~~~~~~~~~~~

Setup

::

    git clone https://github.com/ideonate/jupyter-innotater

    cd jupyter-innotater

    
Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

::

    # Install package in development mode
    pip install -e .

    # Link your development version of the extension with JupyterLab
    jupyter labextension develop . --overwrite

    # Rebuild extension Javascript source after making changes
    jlpm run build


You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

::

    # Watch the source directory in one terminal, automatically rebuilding when needed
    jlpm run watch

    # Run JupyterLab in another terminal
    jupyter lab


With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

::

    jupyter lab build --minimize=False


Git Config:

::

    # Optional - for contributors to the main repo
    cd ../.git/hooks
    ln -s -f ../../githooks/pre-commit .