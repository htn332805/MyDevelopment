{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.my_xrdp;
in {
  options = {
    services.my_xrdp = {
      enable = mkEnableOption "Custom XRDP service";
      
      port = mkOption {
        type = types.port;
        default = 3389;
        description = "Port to listen on for RDP connections";
      };
      
      openFirewall = mkOption {
        type = types.bool;
        default = false;
        description = "Open firewall for XRDP port";
      };
    };
  };

  config = mkIf cfg.enable {
    systemd.services.my_xrdp = {
      description = "Custom XRDP Server";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      
      serviceConfig = {
        ExecStart = "${pkgs.xrdp}/bin/xrdp --nodaemon --config /home/nixos/xrdp.ini";
        Restart = "always";
        User = "root";
      };
    };

    systemd.services.my_xrdp-sesman = {
      description = "Custom XRDP Session Manager";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      
      serviceConfig = {
        ExecStart = "${pkgs.xrdp}/bin/xrdp-sesman --nodaemon --config /home/nixos/sesman.ini";
        Restart = "always";
        User = "root";
      };
    };

    networking.firewall = mkIf cfg.openFirewall {
      allowedTCPPorts = [ cfg.port ];
    };

    environment.etc = {
      "xrdp/startwm.sh" = {
        source = "/home/nixos/startwm.sh";
        mode = "0755";
      };
    };

    system.activationScripts.my_xrdp_setup = ''
      mkdir -p /home/nixos
      cp -n ${pkgs.xrdp}/etc/xrdp/{xrdp.ini,sesman.ini} /home/nixos/
      cp -n ${pkgs.xrdp}/etc/xrdp/startwm.sh /home/nixos/
      chown nixos:users /home/nixos/{xrdp.ini,sesman.ini,startwm.sh}
      chmod 644 /home/nixos/{xrdp.ini,sesman.ini}
      chmod 755 /home/nixos/startwm.sh
    '';
  };
}
