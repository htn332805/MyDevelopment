# Edit this configuration file to define what should be installed on
# your system. Help is available in the configuration.nix(5) man page, on
# https://search.nixos.org/options and in the NixOS manual (`nixos-help`).

{ config, lib, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./labhardware-configuration.nix
      ../../modules/my_neovim.nix
      ../../modules/my_power_settings.nix
    ];

  services.my_xrdp = {
    enable = true;
    openFirewall = true;
  };
  # Use the systemd-boot EFI boot loader.
  #boot.loader.systemd-boot.enable = true;
  #boot.loader.efi.canTouchEfiVariables = true;
  boot = {
    kernelPackages =  pkgs.linuxPackages;
    initrd.verbose = true;
    plymouth.enable = false;
    consoleLogLevel = 7;
    initrd.supportedFilesystems = [ "zfs" ];
    supportedFilesystems = [ "zfs" ];
    initrd.availableKernelModules = [ "pktgen" "xhci_pci" "usbhid" "uas" "usb_storage" ];
    loader.generic-extlinux-compatible.enable = false;
    loader.efi.canTouchEfiVariables = true;
    loader.systemd-boot.enable =  true;
    kernelParams = [
      "efi=debug"
      "ignore_loglevel"
      "console=tty0"
    ]; #end of kernel parameters
    #zfs = {
  	  #forceImportRoot = true;
  	  #extraPools = [ "zroot" ];
	  #}; #end of zfs
  };#END OF BOOT BLOCK
  
  systemd.services.zfs-import-pools = {
  	description = "Import ZFS pools";
  	wantedBy = [ "zfs.target" ];
  	before = [ "zfs.target" ];
  	serviceConfig = {
    		Type = "oneshot";
    		RemainAfterExit = true;
    		ExecStart = "${config.boot.zfs.package}/bin/zpool import -a -f";
  	};
  }; #end of sytemd
  # networking.hostName = "nixos"; # Define your hostname.
  # Pick only one of the below networking options.
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.
  # networking.networkmanager.enable = true;  # Easiest to use and most distros use this by default.

  # Set your time zone.
  time.timeZone = "America/Los_Angeles";

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";
   console = {
     font = "Lat2-Terminus16";
  #   keyMap = "us";
     useXkbConfig = true; # use xkb.options in tty.
   }; #end of console

  # Enable the X11 windowing system.
  # X Server and i3 Configuration
  services.xserver = {
    enable = true;
    displayManager = {
      lightdm.enable = true;
      defaultSession = "none+i3";
    };
    windowManager.i3 = {
      enable = true;
      extraPackages = with pkgs; [
        dmenu
        i3status
        i3lock
      ];
    }; #end of i3 window manage
  }; #end of xserver

  ## Firewall Configuration
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 69 80 3389 5900 8080 ];
  };

  ## Nix Package Manager Configuration
  nix = {
    package = pkgs.nixVersions.stable;
    extraOptions = "experimental-features = nix-command flakes";
  };
   
  # Configure keymap in X11
   services.xserver.xkb.layout = "us";
   services.xserver.xkb.options = "eurosign:e,caps:escape";

  # Enable CUPS to print documents.
  # services.printing.enable = true;

  # Enable sound.
  # hardware.pulseaudio.enable = true;
  # OR
   services.pipewire = {
     enable = true;
     pulse.enable = false;
   }; # end of pipewire

  # Enable touchpad support (enabled default in most desktopManager).
   services.libinput.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
   users.users.nixos = {
     initialPassword = "hai";
     isNormalUser = true;
     extraGroups = [ "wheel" ]; # Enable ‘sudo’ for the user.
     packages = with pkgs; [
       firefox chromium tree tmux screen htop nload git fio sysstat nb neovim emacs vim wget curl 
     ]; #end of packages
   }; #end of users

  # List packages installed in system profile. To search, run:
  # $ nix search wget
  environment.systemPackages = with pkgs; [
    firefox chromium tree tmux screen htop nload git fio sysstat nb neovim emacs vim wget curl 
   ];

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  programs.mtr.enable = true;
  programs.gnupg.agent = {
     enable = true;
     enableSSHSupport = true;
   }; #end of programs
  #programs.nvf = {
  #  enable = true;
  #  settings = {
  #    vim.theme.enable = true;
  #    vim.theme.name = "catppuccin";
  #    vim.theme.style = "dark";
  #    vim.languages.nix.enable = true;
  #  };
  #};
  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  services.openssh.enable = true;

  # Open ports in the firewall.
  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  # Or disable the firewall altogether.
  # networking.firewall.enable = false;
  networking.hostId = "12345678";
  # Copy the NixOS configuration file and link it from the resulting system
  # (/run/current-system/configuration.nix). This is useful in case you
  # accidentally delete configuration.nix.
  # system.copySystemConfiguration = true;
  
  # This option defines the first version of NixOS you have installed on this particular machine,
  # and is used to maintain compatibility with application data (e.g. databases) created on older NixOS versions.
  #
  # Most users should NEVER change this value after the initial install, for any reason,
  # even if you've upgraded your system to a new NixOS release.
  #
  # This value does NOT affect the Nixpkgs version your packages and OS are pulled from,
  # so changing it will NOT upgrade your system - see https://nixos.org/manual/nixos/stable/#sec-upgrading for how
  # to actually do that.
  #
  # This value being lower than the current NixOS release does NOT mean your system is
  # out of date, out of support, or vulnerable.
  #
  # Do NOT change this value unless you have manually inspected all the changes it would make to your configuration,
  # and migrated your data accordingly.
  #
  # For more information, see `man configuration.nix` or https://nixos.org/manual/nixos/stable/options#opt-system.stateVersion .
  system.stateVersion = "24.11"; # Did you read the comment?

}
