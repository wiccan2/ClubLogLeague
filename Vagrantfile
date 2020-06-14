# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "nix-wie-weg/windows10pro"
  # config.vm.box = "StefanScherer/windows_10"
  config.vm.guest = :windows
  config.vm.communicator = "winrm"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "4096"
  end

  config.vm.provision "shell", inline: <<-SHELL
    (new-object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe','C:\\python-install.exe')
    C:\\python-install.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=c:\\Python
  SHELL
end
