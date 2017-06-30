Installation
============

BabelFish runs on Python 3 and can be installed on Linux servers.
It might work on Windows too, but we've never tested it - Windows is evil!

To install BabelFish, you've to:

.. code-block:: bash

    # Clone the repository.
    git clone git@github.com:confirm/Mattermost-BabelFish.git
    cd Mattermost-BabelFish/babelfish/

    # Create Python virtualenv.
    virtualenv -p python3 .venv
    source .venv/bin/activate

    # Install requirements.
    pip install -r requirements.txt

