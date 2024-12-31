{
  description = "A simple Python script flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          requests
        ]);
      in
      {
        packages.default = pkgs.writeScriptBin "hello-world" ''
          #!${pythonEnv}/bin/python
          ${builtins.readFile ./hello_world.py}
        '';

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/hello-world";
        };
      }
    );
}
