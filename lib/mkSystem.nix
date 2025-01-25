{ nixpkgs, home-manager, system, extraModules ? [] }:

nixpkgs.lib.nixosSystem {
  inherit system;
  modules = [
    home-manager.nixosModules.home-manager
    ../modules/common.nix
  ] ++ extraModules;
}
