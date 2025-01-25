{
  description = "Multi-platform NixOS configuration with common development tools and Python packages";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    stable_nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
    nixpkgs-darwin.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    disko = {
      url = "github:nix-community/disko";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixos-wsl = {
      url = "github:nix-community/NixOS-WSL";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, nixpkgs-darwin, home-manager, nixos-wsl, stable_nixpkgs, disko, ... }:
  let
    supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    mkSystem = import ./lib/mkSystem.nix;
  in
  {
    nixosConfigurations = {
      X86Serv = mkSystem {
        inherit nixpkgs home-manager;
        system = "x86_64-linux";
        extraModules = [ ./hosts/x86_64-linux/configuration.nix ];
      };

      Aarch64Serv = mkSystem {
        inherit nixpkgs home-manager;
        system = "aarch64-linux";
        extraModules = [ ./hosts/aarch64-linux/configuration.nix ];
      };

      Raspi4B = mkSystem {
        inherit nixpkgs home-manager;
        system = "aarch64-linux";
        extraModules = [ ./hosts/raspberry-pi/configuration.nix ];
      };

      usb = mkSystem {
        inherit nixpkgs home-manager;
        system = "x86_64-linux";
        #pkgs = nixpkgs.legacyPackages.${system};
        extraModules = [
          disko.nixosModules.disko
          ./modules/disko-config.nix
          {
            #myDisko.diskDevice = diskDevice;
          }
          ({ modulesPath, ... }: {
            imports = [
              (modulesPath + "/installer/scan/not-detected.nix")
              (modulesPath + "/profiles/qemu-guest.nix")
            ];
          })
        ];
      };

      wsl = mkSystem {
        inherit nixpkgs home-manager;
        system = "x86_64-linux";
        extraModules = [
          ./hosts/wsl/configuration.nix
          nixos-wsl.nixosModules.wsl
        #sudo nixos-install --flake .#your-hostname --arg diskDevice '"/dev/disk/by-id/your-disk-id"'
        ];
      };

      RemInstall = mkSystem {
        inherit nixpkgs home-manager;
        system = "x86_64-linux";
        extraModules = [
          ({ modulesPath, ... }: {
            imports = [
              (modulesPath + "/installer/scan/not-detected.nix")
              (modulesPath + "/profiles/qemu-guest.nix")
            ];
          })
          ./hosts/remote/configuration.nix
        ];
      };
    };

    darwinConfigurations = {
      IntelMac = nixpkgs-darwin.lib.darwinSystem {
        system = "x86_64-darwin";
        modules = [
          ./hosts/darwin/configuration.nix
          home-manager.darwinModules.home-manager
          ./modules/common.nix
        ];
      };

      MxMac = nixpkgs-darwin.lib.darwinSystem {
        system = "aarch64-darwin";
        modules = [
          ./hosts/darwin/configuration.nix
          home-manager.darwinModules.home-manager
          ./modules/common.nix
        ];
      };
    };

    devShell = forAllSystems (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        commonModule = import ./modules/common.nix;
        pythonEnv = (pkgs.python3.withPackages (ps: with ps; [
          jupyterlab
          ipython
          dash
          matplotlib
        ]));
      in
      pkgs.mkShell {
        buildInputs = commonModule.environment.systemPackages ++ [ pythonEnv ];

        shellHook = ''
          echo "Development environment loaded with requested tools and Python packages."
        '';
      }
    );

    packages = forAllSystems (system: {
      # Define your custom packages here
    });

    overlays = {
      # Define your custom overlays here
    };

    modules = {
      # Define your custom modules here
    };
  };
}
