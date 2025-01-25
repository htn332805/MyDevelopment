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
  ];
in
{
  environment.systemPackages = [
    (pkgs.python3.withPackages pythonPackages)
  ];
}
