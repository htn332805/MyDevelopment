{ config, lib, pkgs, ... }:

let
  cfg = config.myDisko;
in
{
  options.myDisko = {
    diskDevice = lib.mkOption {
      type = lib.types.str;
      description = "The disk device to use for installation";
    };
  };

  config = {
    disko.devices = {
      disk = {
        main = {
          type = "disk";
          device = cfg.diskDevice;
          content = {
            type = "gpt";
            partitions = {
              ESP = {
                size = "500M";
                type = "EF00";
                content = {
                  type = "filesystem";
                  format = "vfat";
                  mountpoint = "/boot";
                  mountOptions = [
                    "defaults"
                  ];
                };
              };
              bios_grub = {
                size = "8M";
                type = "EF02";
              };
              zfs = {
                size = "100%";
                content = {
                  type = "zfs";
                  pool = "rpool";
                };
              };
            };
          };
        };
      };
      zpool = {
        rpool = {
          type = "zpool";
          rootFsOptions = {
            acltype = "posixacl";
            canmount = "off";
            compression = "zstd";
            devices = "off";
            normalization = "formD";
            relatime = "on";
            xattr = "sa";
            "com.sun:auto-snapshot" = "false";
          };
          options = {
            ashift = "12";
            autotrim = "on";
          };
          datasets = {
            "local" = {
              type = "zfs_fs";
              options = {
                canmount = "off";
              };
            };
            "local/nix" = {
              type = "zfs_fs";
              mountpoint = "/nix";
            };
            "local/log" = {
              type = "zfs_fs";
              mountpoint = "/var/log";
            };
            "safe" = {
              type = "zfs_fs";
              options = {
                canmount = "off";
              };
            };
            "safe/home" = {
              type = "zfs_fs";
              mountpoint = "/home";
            };
            "safe/persistent" = {
              type = "zfs_fs";
              mountpoint = "/persistent";
            };
            "reserved" = {
              type = "zfs_fs";
              options = {
                canmount = "off";
                reservation = "500M";
              };
            };
          };
        };
      };
    };

    fileSystems."/nix" = {
      device = "rpool/local/nix";
      fsType = "zfs";
    };

    fileSystems."/var/log" = {
      device = "rpool/local/log";
      fsType = "zfs";
    };

    fileSystems."/home" = {
      device = "rpool/safe/home";
      fsType = "zfs";
    };

    fileSystems."/persistent" = {
      device = "rpool/safe/persistent";
      fsType = "zfs";
    };

    boot.supportedFilesystems = [ "zfs" ];
    networking.hostId = "12345678"; # Replace with a valid 8-digit hexadecimal number
  };
}
