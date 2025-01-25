{ config, lib, pkgs, ... }:

{
  # Disable screen sleep
  services.xserver.serverFlagsSection = ''
    Option "BlankTime" "0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime" "0"
  '';

  # Prevent hard drives from sleeping
  powerManagement.powerUpCommands = ''
    ${pkgs.hdparm}/sbin/hdparm -B 255 /dev/sda
  '';

  # Disable hibernation
  boot.kernelParams = [ "nohibernate" ];

  # Configure power button to shut down the system
  services.logind.extraConfig = ''
    HandlePowerKey=poweroff
  '';

  # Disable automatic suspend and hibernation
  services.logind.lidSwitch = "ignore";
  services.logind.lidSwitchExternalPower = "ignore";
  powerManagement.enable = false;

  # Disable GNOME power management
  services.xserver.desktopManager.gnome = {
    extraGSettingsOverrides = ''
      [org.gnome.settings-daemon.plugins.power]
      sleep-inactive-ac-type='nothing'
      sleep-inactive-battery-type='nothing'
      power-button-action='interactive'
    '';
  };
  services.xserver.displayManager.gdm.autoSuspend = false;
  programs.dconf.enable = true;
  #environment.etc."dconf/db/local.d/disable-auto-suspend".text = ''
  #  [org/gnome/settings-daemon/plugins/power]
  #  sleep-inactive-ac-type='nothing'
  #  sleep-inactive-battery-type='nothing'
  #'';

}
