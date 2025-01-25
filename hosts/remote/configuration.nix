{ config, pkgs, modulesPath, lib, ... }:

{
  imports = [
    # Hardware scan results
    (modulesPath + "/installer/scan/not-detected.nix")
    (modulesPath + "/profiles/qemu-guest.nix")
    ./disk-config.nix
    ../../modules/my_neovim.nix
    ../../modules/my_power_settings.nix
    ../../modules/my_xrdp.nix

  ];

  # Use the systemd-boot EFI boot loader
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  # Network configuration
  networking.hostName = "nixos";
  networking.networkmanager.enable = true;
  networking.hostId = "12345678";

  # Set your time zone.
  time.timeZone = "America/Los_Angeles";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";
   console = {
     font = "Lat2-Terminus16";
  #   keyMap = "us";
     useXkbConfig = true; # use xkb.options in tty.
   }; #end of console

  # Enable the X11 windowing system.
  ## X Server and i3 Configuration
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
    };
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

  # Enable SSH server
  services.openssh = {
    enable = true;
    settings = {
      PermitRootLogin = "prohibit-password";
      PasswordAuthentication = false;
    };
  };
  ## Firewall Configuration
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 69 80 3389 5900 8080];
  };
  # Define a user account. Don't forget to set a password with ‘passwd’.
   users.users.nixos = {
     initialPassword = "hai";
     isNormalUser = true;
     extraGroups = [ "wheel" ]; # Enable ‘sudo’ for the user.
     packages = with pkgs; [
       firefox chromium tree tmux screen htop nload git fio sysstat nb neovim emacs vim wget curl 
     ]; #end of packages
   }; #end of users

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  # Enable flakes
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  # System-wide environment variables
  environment.variables = {
    EDITOR = "nvim";
  };

  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It's perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  system.stateVersion = "24.11"; # Don't change this unless you know what you're doing
}
