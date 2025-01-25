{ pkgs, ... }:

let
  pythonPackages = ps: with ps; [
    jupyterlab
    ipython
    dash
    matplotlib
    pandas
    numpy
  ];
in
{
  environment.systemPackages = [
    (pkgs.python3.withPackages pythonPackages)
  ];
}
