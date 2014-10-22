# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
 config.vm.box = "hashicorp/precise64"
 dirname = File.basename(Dir.getwd)

 config.vm.network "forwarded_port", guest: 5000, host: 5000
 config.vm.network "forwarded_port", guest: 8080, host: 8089


 config.vm.hostname = dirname

$script = <<SCRIPT
echo "Provisioning Flask, Tornado, Zeroconf"
sudo apt-get update
sudo apt-get -y install python avahi-daemon python-pip git curl
sudo pip install -r /vagrant/requirements.txt
SCRIPT

config.vm.provision "shell", inline: $script

end