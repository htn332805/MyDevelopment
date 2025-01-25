{ pkgs, ... }:

let
  pythonPackages = ps: with ps; [
    jupyterlab
    ipython
    jupyter
    dash
    matplotlib
    pandas
    numpy
    virtualenv
  ];
in
{
  environment.systemPackages = [
    (pkgs.python3.withPackages pythonPackages)
  ];
}
