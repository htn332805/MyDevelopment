{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    htop
    tmux
    screen
    nload
    git
    fio
    sysstat
    tree
    neovim
    emacs
    vim
    nb
  ];
}
