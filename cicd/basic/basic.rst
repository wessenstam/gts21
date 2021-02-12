.. _docker_start:

---------------------------
Containerize the Fiesta App
---------------------------

In this section, you will learn how to convert the legacy (Fiesta) application into a containerized application.

High level steps:

- Use the Docker VM to build the containerized application.
- Test the application by deploying the container.

.. note::

   Estimated time **30 minutes**

Build the container
+++++++++++++++++++

Analyze the original Fiesta Application
.......................................

Let's begin by analyzing the installation of the Fiesta app, by viewing the blueprint.

#. Within Prism Central, click on :fa:`bars` **Services > Calm**.
#. Click the Blueprint |bp_icon| icon.
#. Open the *UserXX*\ [NAME OF BLUEPRINT]
#. Click on the *Fiesta_App_VM* VM, then from the right-hand pane, click on **Package > Configure Install**.

   .. figure:: images/1.png

#. Observe the three steps executed to perform the installation of the Fiesta app.

#. Click **Install npm**, and observe the *Script* portion in the right-hand pane, which includes the steps to:

   - Install required packages
   - Clone a Git repository
   - Install npm
   - Build the application
   - Install an npm dependency
   - Run steps to get the application built

   .. figure:: images/2.png

.. _basic_container:

Install container
.................

In this section, you will install the first container.

   - The building of this container will be created from the settings within our ``dockerfile``.  A *Dockerfile* is a text document that contains all the commands a user could call on the command line to assemble the Docker image. Docker can build images automatically by reading the instructions from a *Dockerfile*.

   - A *Docker image* is a read-only template that contains a set of instructions for creating a container that can run on the Docker platform.

   - Using ``docker build`` users can create an automated build that executes several command-line instructions in succession.

Here's a quick way to visualize these terms, and the overall process. As you can see in the below diagram, when the *Dockerfile* is built, it becomes a *Docker Image*. When we run the *Docker Image*, then it finally becomes a *Docker Container*.

.. figure:: images/2a.png

.. note::

   Disk space is a consideration when building any container, and as such, we are using Alpine Linux. Alpine Linux is a Linux distribution designed for security, simplicity, and resource efficiency.

#. Login to your *UserXX*\ docker VM via SSH, using **root** as the username, and **nutanix/4u** as the password.

#. Run the command ``mkdir github``, followed by ``cd github``. This will create, and change to the directory we will be using to store the Fiesta repository.

#. Run the command ``git clone https://github.com/sharonpamela/Fiesta`` to make a local copy of the Fiesta repository into the *github* directory.

#. Create a file called *dockerfile* by using the command ``vi dockerfile``. This will create a blank file using the vi text editor, and we will populate in the next step.

.. note::

   Please feel free to use Nano, as your text editor of choice, if you are more familiar with it, and its commands.

#. Hit the **Insert** key to begin inserting text into the *dockerfile* file.

#. Copy and paste the following:

   .. code-block:: dockerfile

      # Grab the needed OS image
      FROM alpine:3.11

      # Install the needed packages
      RUN apk add --no-cache --update nodejs npm mysql-client git python3 python3-dev gcc g++ unixodbc-dev curl

      # Create a location in the container for the Fiest Application Code
      RUN mkdir /code

      # Make sure that all next commands are run against the /code directory
      WORKDIR /code

      # Copy needed files into the container
      COPY runapp.sh /code

      # Make the runapp.sh executable
      RUN chmod +x /code/runapp.sh

      # Start the application
      ENTRYPOINT [ "/code/runapp.sh"]

      # Expose port 30001 and 3000 to the outside world
      EXPOSE 3001 3000

#. Hit the **ESC** key to stop editing the file, followed by **:wq!** to save and close the file.

#. Create a file called *runapp.sh* by using the command ``vi runapp.sh``. This will create a blank file, which we will populate in the next step.

#. Hit the **Insert** key to begin inserting text into the *runapp.sh* file.

   .. note::

      Before copying and pasting the below information, you must modify the *<MARIADB-IP-ADDRESS>* entry to match your UserXX*\ MariaDB VM's IP address.

#. Copy and paste the following:

   .. code-block:: bash

      #!/bin/sh

      # Clone the Repo into the container in the /code folder we already created in the dockerfile
      git clone https://github.com/sharonpamela/Fiesta /code/Fiesta

      # Change the configuration from the git clone action
      sed -i 's/REPLACE_DB_NAME/FiestaDB/g' /code/Fiesta/config/config.js
      sed -i "s/REPLACE_DB_HOST_ADDRESS/<MARIADB-IP-ADDRESS>/g" /code/Fiesta/config/config.js
      sed -i "s/REPLACE_DB_DIALECT/mysql/g" /code/Fiesta/config/config.js
      sed -i "s/REPLACE_DB_USER_NAME/fiesta/g" /code/Fiesta/config/config.js
      sed -i "s/REPLACE_DB_PASSWORD/fiesta/g" /code/Fiesta/config/config.js

      npm install -g nodemon

      # Get ready to start the application
      cd /code/Fiesta
      npm install
      cd /code/Fiesta/client
      npm install

      # Update the packages
      npm fund
      npm update
      npm audit fix

      # Build the app
      npm run build

      # Run the NPM Application
      cd /code/Fiesta
      npm start

#. Hit the **ESC** key to stop editing the file, followed by **:wq!** to save and close the file.

#. Enter **ls -al** to perform a directory listing. Ensure tour github directory looks like the below before proceeding.

   .. figure:: images/5.png

#. Run the command ``docker build .`` (including the period) to create the container. This takes approximately 1 minute.

   .. note::

       If you get a message stating **You have reached your pull limit...** ask the leading SE for the solution [SHOULD WE BE CONCERNED ABOUT THIS?]

#. Run the command ``docker image ls`` to list your images. The *docker image* command manages images.

   .. figure:: images/6.png

So we have an image ID. Great. But what does this mean to us? Let's quickly add some context.

#. Run the command ``docker build . -t fiesta_app:1.0``. This will change the existing *Repository* to *fiesta_app*, and the *tag* to *1.0*.

#. Run the command ``docker image ls`` to list your images once again.

   .. figure:: images/7.png

#. Run the command ``docker run -d --rm --name Fiesta_App fiesta_app:1.0`` to create the container.

   .. note::

      - ``--name`` give the container a name, as by default the name will be randomly generated. This makes the management of the container easier.

      - ``--rm`` Remove the container after it stops.

      - ``-d`` Run as a daemon (a background process that handles requests, but is dormant when not required).

#. Run the command ``docker logs --follow Fiesta_App`` to see the console log of the container.

   After approximately 2-3 minutes, the application will be started, and you will see something like the below.

      .. figure:: images/8.png


   Current status: the application has been started. However, if you visit the URL referenced in the screenshot, you won't get a response. This is because the IP address listed is internal to the Docker environment. To correct this, we must configure the docker engine to allow external traffic to reach port 3000.

#. Hit **<CTRL> + C** to exit the *docker logs* command, and return to the command prompt.

#. Run the command ``docker stop Fiesta_App`` to (you guessed it!) stop the container. This will not only stop the container, but as we specified on creation, will delete the container.

#. Run the command ``docker run -d --rm -p 5000:3000 --name Fiesta_App fiesta_app:1.0``. The *-p 5000:3000* parameter exposes port 5000, and maps the external port of 5000 to the internal port of 3000.

[This failed first attempt, worked second attempt.

root@xyz123-docker-vm github]# docker run -d --rm -p 5000:3000 --name Fiesta_App fiesta_app:1.0
docker: Error response from daemon: Conflict. The container name "/Fiesta_App" is already in use by container "f838ddea0f8920fde1136bb722fd97fde6605871fd3813068f0e371cf79c6e28". You have to remove (or rename) that container to be able to reuse that name.]

#. Run the command ``docker logs --follow Fiesta_App`` once again. At the same time, open a browser ``http://<DOCKER-VM-IP-ADDRESS>:5000/products``.

   .. figure:: images/9.png

#. Run the command ``docker stop Fiesta_App``, as we don't need it running for now.

.. raw:: html

    <H1><font color="#AFD135"><center>Congratulations!!!!</center></font></H1>

We have just created our initial version of the Fiesta app as a container. However, there are some things we should address, as this isn't exactly an ideal deployment.

   - Utilizing a text editor is not the most efficient method, not to mention prone to human error.

   - Variables could provide some extensibility, and would have to be set outside of the image we build.

   - Using this method is time-consuming and tedious to create a container, not to mention manage.

   - The start of the container takes a long time.

   - The image is only available as long as the Docker VM exists.

In the proceeding sections, we will show you how to address all of these concerns.

.. |proj-icon| image:: ../images/projects_icon.png
.. |bp_icon| image:: ../images/blueprints_icon.png
.. |mktmgr-icon| image:: ../images/marketplacemanager_icon.png
.. |mkt-icon| image:: ../images/marketplace_icon.png
.. |bp-icon| image:: ../images/blueprints_icon.png
