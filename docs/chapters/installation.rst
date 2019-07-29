.. _installation:

Installation
------------

Install from PyPi (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install jupyter_innotater

To enable in JupyterLab (version 1.0+ required):

::

    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter labextension install jupyter-innotater


Development install
~~~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/ideonate/innotater

    cd innotater/jupyter-innotater/js
    npm install
    npm run build

    cd ..
    pip install -e .

    jupyter nbextension install --py --symlink --sys-prefix jupyter_innotater
    jupyter nbextension enable --py --sys-prefix jupyter_innotater

    # To enable in Jupyter Lab (requires Jupyter Lab 1.0+):
    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter labextension install js

    # Maybe also:
    pip install ipywidgets
    jupyter nbextension install --py widgetsnbextension
    jupyter nbextension enable widgetsnbextension --py

    # Optional - for contributors to the main repo
    cd ../.git/hooks
    ln -s -f ../../githooks/pre-commit .