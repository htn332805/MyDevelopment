{ pkgs, ... }:

let
  pythonPackages = ps: with ps; [
    jupyterlab
    ipython
    dash
    matplotlib
  ];
in
{
  environment.systemPackages = [
    (pkgs.python3.withPackages pythonPackages)
  ];
}
