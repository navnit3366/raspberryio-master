.. _deployment:

Deployment
==========

This section documents the process by which we deploy Raspberry IO.
This is done on a staging site first, and then to a production site
once the code is proven to be stable and working on staging.

.. Note::
   The deployment uses SSH with agent forwarding so you'll need to
   enable agent forwarding if it is not already by adding
   ``ForwardAgent yes`` to your SSH config.


Server Provisioning
-------------------

.. Note::
   This section is only for the maintainers of Raspberry IO. If you
   wish to test out deployment, please see the next section:
   :ref:`vagrant-testing`

The first step in creating a new server is to create users on the remote server. You
will need root user access with passwordless sudo. How you specify this user will vary
based on the hosting provider.

1. For each developer, put a file in the ``conf/users`` directory
   containing their public ssh key, and named exactly the same as the
   user to create on the server, which should be the same as the
   userid on the local development system. (E.g. for user ``dickens``,
   the filename must be ``dickens``, not ``dickens.pub`` or
   ``user_dickens``.)

2. Run this command to create users on the server::

        fab -H <fresh-server-ip> -u <root-user> create_users

   This will create a project user and users for all the developers.

3. Lock down SSH connections: disable password login and move the
   default port from 22 to ``env.ssh_port``::

        fab -H <fresh-server-ip> configure_ssh

4. Add the IP to the appropriate environment function and provision it
   for its role. You can provision a new server with the
   ``setup_server`` fab command. It takes a list of roles for this
   server ('app', 'db', 'lb') or you can say 'all'. The name of the
   environment can now be used in fab commands (such as production,
   staging, and so on.) To setup a server with all roles use::

        fab staging setup_server:all

5. Deploy the latest code to the newly setup server::

        fab staging deploy

6. If a new database is desired for this environment, use ``syncdb``::

        fab staging syncdb

7. Otherwise, a database can be moved to the new environment using
   ``get_db_dump`` and ``load_db_dump`` as in the following example::

        fab production get_db_dump
        fab staging load_db_dump:production.sql


.. _vagrant-testing:

Vagrant Testing
---------------

You can test the provisioning/deployment using
`Vagrant <http://vagrantup.com/>`_. Using the Vagrantfile you can start up the
VM. This uses the ``precise64`` box::

    vagrant up

With the VM up and running, you can create the necessary users.
Put the developers' keys in ``conf/users`` as before, then
use these commands to create the users. The location of the vagrant key file might be::

    if gem installed: /usr/lib/ruby/gems/1.8/gems/vagrant-1.0.2/keys/vagrant
    if apt-get installed: /usr/share/vagrant/keys/vagrant

This may vary on your system. Running ``locate keys/vagrant`` might help find it.
Use the full path to the keys/vagrant file as the value in the ``-i`` option::

    fab -H 33.33.33.10 -u vagrant -i /usr/share/vagrant/keys/vagrant create_users
    fab vagrant setup_server:all
    fab vagrant deploy
    fab vagrant syncdb

When prompted, do not make a superuser during the syncdb, but do make a site.
To make a superuser, you'll need to run::

    fab vagrant manage_run:createsuperuser

It is not necessary to reconfigure the SSH settings on the vagrant box.

The vagrant box forwards port 80 in the VM to port 8080 on the host
box. You can view the site by visiting localhost:8080 in your browser.

You may also want to add::

    33.33.33.10 vagrant.raspberry.io

to your hosts (``/etc/hosts``) file.

You can stop the VM with ``vagrant halt`` and destroy the box
completely to retest the provisioning with ``vagrant destroy``.

For more information please review the Vagrant documentation.


Deployment
----------

For future deployments, you can deploy changes to a particular environment with
the ``deploy`` command. This takes an optional branch name to deploy. If the branch
is not given, it will use the default branch defined for this environment in
``env.branch``::

    fab staging deploy
    fab staging deploy:new-feature

New requirements or South migrations are detected by parsing the VCS changes and
will be installed/run automatically.

Releases
--------

In general, every deployment to master should be a new released
version of Raspberry IO. Currently hotfixes are an exception to this
rule. Here's the steps involved in creating a new release. Let's
assume that master is running version 0.1 and we have made a bunch of
changes on the ``develop`` branch that we want to release as version
0.2:

#. Update ``docs/CHANGELOG.rst`` on ``develop`` branch and replace
   "(unreleased)" with "(today's date)"
#. Update ``setup.py`` on ``develop`` branch and change version to the
   new number (e.g. 0.2)
#. Deploy ``develop`` to staging, ensuring that everything works
#. Merge ``develop`` into ``master``
#. Tag ``master`` on github as v0.2
#. Deploy ``master`` to production
#. Update ``docs/CHANGELOG.rst`` on ``develop`` branch, adding a new heading
   at the top: "Version 0.3 - (Unreleased)"
#. All new changes on ``develop`` should now be documented under the
   Version 0.3 heading in the CHANGELOG

SSL
---

Raspberry IO sits behind the `PSF <http://www.python.org/psf/>`_ Load
Balancer. Requests come in to the load balancer via either HTTP or
HTTPS. The load balancer terminates the SSL connection and then
forwards the request to our Django server with the
``X-Forwarded-Proto`` header set to either ``http`` or ``https``.
Django checks that header and sets ``request.is_secure()``
appropriately. Mezzanine routes any URLs beginning with ``/account``
or ``/admin`` to HTTPS. This can be configured within Mezzanine if
other URL patterns need to be secure.

The Chef recipes which control the load balancer are located at
`<https://github.com/python/psf-chef/tree/master/cookbooks/psf-loadbalancer>`_
