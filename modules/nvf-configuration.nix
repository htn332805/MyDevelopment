{ pkgs, lib, ...}:
{
  vim = {
    theme = {
      enable = true;
      name = "catppuccin";
      style = "dark";
    }; #end of theme
    statusline.lualine.enable = true;
    telescope.enable = true;
    autocomplete.nvim-cmp.enable = true;
    visuals.ident-blankline.enable = true;
    languages = {
      enableLSP = true;
      enableTreesitter = true;
      python = {
        enable = true;
        dap.enable = true;
        format.neable = true;
        lsp.enable = true;
        lsp.server = "pyright";
      }; #end of python
      nix.enable = true;
      ts.enable  = true
      python.
    }; #end of languages
  }; #end of vim




} # top most brace
