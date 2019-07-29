.. _installation:

Installation
------------

Install from PyPi (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install jupyter_innotater

Development install
~~~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/ideonate/innotater

    cd innotater/jupyter-innotater/js
    npm install

    cd ..
    pip install -e .

    jupyter nbextension install --py --symlink --sys-prefix jupyter_innotater
    jupyter nbextension enable --py --sys-prefix jupyter_innotater

    # Optional
    cd ../.git/hooks
    ln -s -f ../../githooks/pre-commit .

    # Maybe also:
    pip install ipywidgets
    jupyter nbextension install --py widgetsnbextension
    jupyter nbextension enable widgetsnbextension --py
