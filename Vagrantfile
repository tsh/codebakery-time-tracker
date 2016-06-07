# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/wily64"

  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 80, host: 8081

  # config.vm.synced_folder ".", "/vagrant"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
     # name machine
     vb.name = "time_tracker"
     vb.memory = 512
  end

  config.vm.provision "shell", inline: <<-SHELL

    sudo apt-get -y install software-properties-common python-software-properties

    set -e

    if [ -x /usr/local/bin/python3.5 ]; then
      echo 'Skipping Python installation since Python 3.5 is already installed.'
    else
      echo 'Install required libraries...'
      apt-get update -yq
      apt-get install -yq libreadline-dev libsqlite3-dev libssl-dev build-essential libtool

      echo 'Install Python 3.5...'
      cd /tmp
      wget -O- https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz | tar xz
      cd Python-3.5.1
      ./configure
      make
      make altinstall

      echo 'Clean up...'
      cd && rm -rf /tmp/Python-3.5.1

      echo 'Done!'
    fi

    sudo apt-get -y install postgresql libpq-dev
    sudo -u postgres createuser vagrant
    sudo -u postgres createdb -O vagrant time-tracker

    cd /vagrant
    sudo python3.5 -m pip install -r requirements.txt

    sudo apt-get -y install golang

    export PATH=$PATH:/usr/local/go/bin
    echo "export GOPATH=/home/vagrant/work/" >> /home/vagrant/.profile
    mkdir ~vagrant/work

    go get github.com/gorilla/websocket

  SHELL

#  config.vm.provision "ansible" do |ansible|
#    ansible.playbook = "ansible/web.yml"
#    ansible.groups = {
#        "vagrant" => ["default"],
#        "dev_enviroment" => ["default"]
#    }
#  end

end
