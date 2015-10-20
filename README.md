# Event Driven Chat with Tornado

For the example you need to have [Ansible][ansible] and [Vagrant][vagrant] installed in your machine.

To try the example you can do, on the root directory of the project:

    cd ansible
    ansible-galaxy install -r requirements.yml

To install Ansible roles dependencies, after that you can create the VM with:

    vagrant up

The application will be listening, so if you want to check the web front you can go to the following URL in your browser

    http://localhost:8888

[vagrant]: https://www.vagrantup.com/
[ansible]: http://www.ansible.com/
