{ pkgs, lib, ...}:
{
  vim = {
    theme = {
      enable = true;
      name = "catppuccin";
      style = "dark";
    }; end of theme
    statusline.lualine.enable = true;
    telescope.enable = true;
    autocomplete.nvim-cmp.enable = true;
    visuals.ident-blankline.enable = true;
  }; #end of vim




}# top most brace
