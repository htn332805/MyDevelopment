{
  description = "Multi-platform NixOS configuration for Hai's setup";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    nixpkgs-darwin.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixos-wsl = {
      url = "github:nix-community/NixOS-WSL";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, nixpkgs-darwin, home-manager, nixos-wsl, ... }:
  let
    supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
  in
  {
    nixosConfigurations = {
      # NixOS configurations
      NixServ = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./hosts/x86_64-linux/configuration.nix
          home-manager.nixosModules.home-manager
        ]; #end of modules
    }; #end of NixServe COnfig

    Aarch64Serv = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      modules = [
        ./hosts/aarch64-linux/configuration.nix
        home-manager.nixosModules.home-manager
      ]; #end of modules
    }; #end of Aarch64Serv

    Raspi4 = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      modules = [
        ./hosts/raspberry-pi/configuration.nix
        home-manager.nixosModules.home-manager
      ]; #end of Raspi4 modules
    }; #end of raspi4 config

    wsl = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./hosts/wsl/configuration.nix
        nixos-wsl.nixosModules.wsl
        home-manager.nixosModules.home-manager
      ]; #end of wsl modules
    }; #end of wsl config

    darwinConfigurations = {
      IntelMac= nixpkgs-darwin.lib.darwinSystem {
        system = "x86_64-darwin";
        modules = [
          ./hosts/darwin/configuration.nix
          home-manager.darwinModules.home-manager
        ]; #end of intel mac modules
      }; #end of intelmac config
      MxMac = nixpkgs-darwin.lib.darwinSystem {
        system = "aarch64-darwin";
          modules = [
            ./hosts/darwin/configuration.nix
            home-manager.darwinModules.home-manager
          ]; #end of MxMac modules
      }; #end of MxMac config
    }; #end of darwin configs
    # Other outputs
    # Shared packages and modules
    packages = forAllSystems (system: {
      # Define your custom packages here
    });

    overlays = {
      # Define your custom overlays here
    };

    modules = {
      # Define your custom modules here
    };
  }; #end of top nixosConfigurations
}
