Quick Start
=======================

The main feature of ``v2raycli`` is listed as below

.. literalinclude:: v2raycli_help.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: v2raycli_help.demo.sh.txt
    :language: text
    :linenos:


List Proxy Sites in Subscription
------------------------------------------

Before starting using ``v2raycli``, you need a subscription url from your proxy service
(such as `justmysocks <https://justmysocks.net/members/>`_). Then put this url
into ``V2RAY_SUBSCRIPTION`` environment (e.g. in linux)

.. code-block:: shell
    :linenos:

    # Use your own subscription url
    export V2RAY_SUBSCRIPTION='https://jmssub.net/members/getsub.php?service=777777&id=4c646243-6c01-42f4-a4f1-eef212b2e659'

Then you can see the proxy sites in subscription you given.

.. literalinclude:: v2raycli_list_1_show.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: v2raycli_list_1.demo.sh.txt
    :language: text
    :linenos:


Or using the ``-s`` argument

.. literalinclude:: v2raycli_list_2.demo.sh
    :language: shell
    :linenos:


Other arguments can be shown with ``-h`` argument.

.. literalinclude:: v2raycli_list_help.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: v2raycli_list_help.demo.sh.txt
    :language: text
    :linenos:


Start Local Proxy Service
------------------------------------------

Before starting the proxy service locally, you need to configure the executable file of v2ray
(you can download this from `v2ray/dist on Github <https://github.com/v2ray/dist/>`_):

.. code-block:: shell
    :linenos:

    # Use your own v2ray binary executable
    export V2RAY_BIN=./bin/v2ray

After the configuration is complete, the service can be started locally

.. code-block:: shell
    :linenos:

    v2raycli run                   # Start the proxy (socks5 protocol, port 17777)
    v2raycli run -P http -p 16384  # Start at port 16384 with http protocol
    v2raycli run -R                # DO NOT ASK ME! Just randomly use one site

The other arguments can be shown with ``-h`` argument.

.. literalinclude:: v2raycli_run_help.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: v2raycli_run_help.demo.sh.txt
    :language: text
    :linenos:

