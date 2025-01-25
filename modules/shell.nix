{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    ipython
    jupyter
    numpy
    matplotlib
  ]);
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    # C/C++ development tools
    gcc
    gdb
    clang
    clang-tools
    cmake
    gnumake
    bear

    # Python environment
    pythonEnv

    # Kernel development
    linuxHeaders
    ncurses

    # Version control
    git

    # Code formatting and linting
    clang-format
    pylint
    black

    # IDE support
    ctags
    global
  ];

  shellHook = ''
    export KERNELDIR="${pkgs.linuxHeaders}/include"
    export C_INCLUDE_PATH="${pkgs.linuxHeaders}/include:$C_INCLUDE_PATH"
    export CPLUS_INCLUDE_PATH="${pkgs.linuxHeaders}/include:$CPLUS_INCLUDE_PATH"
    echo "Kernel development environment loaded."
    echo "Kernel headers are available at: $KERNELDIR"
  '';
}
