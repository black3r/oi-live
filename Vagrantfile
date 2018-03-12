# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  %x[mkdir -p ./output]

  config.ssh.insert_key = false

  # Two machines will be provisioned
  # First will be the OI-Live source installation
  config.vm.define "oilive", primary: true do |oilive|
    oilive.vm.box = "ogarcia/archlinux-x64"
    oilive.vm.box_check_update = false
    oilive.vm.synced_folder "./output", "/vagrant"
    oilive.vm.provider "virtualbox" do |vb|
      vb.memory = 4096
      vb.cpus = 4
    end
  end

  # Magic shell command to find location of oilive virtual disk
  disk_file = %x[[ -f .vagrant/machines/oilive/virtualbox/id ] && VBoxManage showvminfo --machinereadable `cat .vagrant/machines/oilive/virtualbox/id` | grep "IDE Controller-0-0" | awk -F'=' '{ORS=""} {print $2}' | sed -e 's/^"//' -e 's/"$//']

  # Second will contain the tools for building the image from the 
  # first one's virtual disk connected as a second drive.
  config.vm.define "builder", autostart: false do |builder|
    builder.vm.box = "archlinux/archlinux" # Use different base box to avoid boot-time UUID conflicts
    builder.vm.box_check_update = false
    builder.vm.synced_folder "./output", "/vagrant"
    builder.vm.provider "virtualbox" do |vb|
      vb.memory = 4096
      vb.cpus = 4
      if disk_file.length > 0 then
        vb.customize ['storageattach', :id, '--storagectl', 'IDE Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', disk_file]
      end
    end
  end

  config.vm.provision "shell", inline: "sudo pacman -Sy --noconfirm --needed python2"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/playbook.yml"
    ansible.groups = {
      "oilive" => ["oilive"],
      "builder" => ["builder"]
    }
  end
end
