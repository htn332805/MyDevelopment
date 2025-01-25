{ config, lib, pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    viAlias = true;
    vimAlias = true;
    defaultEditor = true;

    plugins = with pkgs.vimPlugins; [
      # Theme
      gruvbox-nvim

      # File explorer
      nvim-tree-lua

      # Status line
      lualine-nvim

      # Git integration
      vim-fugitive
      gitsigns-nvim

      # LSP and autocompletion
      nvim-lspconfig
      nvim-cmp
      cmp-nvim-lsp
      cmp-buffer
      cmp-path
      cmp-cmdline

      # Snippets
      luasnip
      cmp_luasnip

      # Treesitter for better syntax highlighting
      (nvim-treesitter.withPlugins (plugins: with plugins; [
        c
        cpp
        python
        lua
        vim
        vimdoc
        query
        markdown
        latex
        dot
      ]))

      # Markdown preview
      markdown-preview-nvim

      # LaTeX support
      vimtex

      # Graphviz support
      vim-graphviz

      # Indent guides
      indent-blankline-nvim

      # Code folding
      nvim-ufo
      promise-async

      # Telescope for fuzzy finding
      telescope-nvim
      telescope-fzf-native-nvim

      # Comment toggling
      comment-nvim

      # Auto pairs
      nvim-autopairs
    ];

    extraConfig = ''
      lua << EOF
      -- Basic settings
      vim.opt.number = true
      vim.opt.relativenumber = true
      vim.opt.expandtab = true
      vim.opt.shiftwidth = 2
      vim.opt.tabstop = 2
      vim.opt.smartindent = true
      vim.opt.termguicolors = true
      vim.opt.colorcolumn = "80"
      vim.opt.foldmethod = "expr"
      vim.opt.foldexpr = "nvim_treesitter#foldexpr()"
      vim.opt.foldlevel = 99

      -- Theme
      vim.cmd('colorscheme gruvbox')

      -- LSP setup
      local lspconfig = require('lspconfig')
      local capabilities = require('cmp_nvim_lsp').default_capabilities()

      lspconfig.clangd.setup{capabilities = capabilities}
      lspconfig.pyright.setup{capabilities = capabilities}

      -- Completion setup
      local cmp = require('cmp')
      cmp.setup({
        snippet = {
          expand = function(args)
            require('luasnip').lsp_expand(args.body)
          end,
        },
        mapping = cmp.mapping.preset.insert({
          ['<C-b>'] = cmp.mapping.scroll_docs(-4),
          ['<C-f>'] = cmp.mapping.scroll_docs(4),
          ['<C-Space>'] = cmp.mapping.complete(),
          ['<C-e>'] = cmp.mapping.abort(),
          ['<CR>'] = cmp.mapping.confirm({ select = true }),
        }),
        sources = cmp.config.sources({
          { name = 'nvim_lsp' },
          { name = 'luasnip' },
        }, {
          { name = 'buffer' },
        })
      })

      -- Treesitter setup
      require('nvim-treesitter.configs').setup {
        highlight = {
          enable = true,
        },
      }

      -- Indent guides
      require("indent_blankline").setup {
        show_current_context = true,
        show_current_context_start = true,
      }

      -- Code folding
      require('ufo').setup()

      -- Telescope setup
      require('telescope').setup()

      -- Comment setup
      require('Comment').setup()

      -- Autopairs setup
      require('nvim-autopairs').setup()

      -- Markdown preview setup
      vim.g.mkdp_auto_start = 0
      vim.g.mkdp_auto_close = 1

      -- LaTeX setup
      vim.g.vimtex_view_method = 'zathura'

      -- Keymaps
      local keymap = vim.api.nvim_set_keymap
      local opts = { noremap = true, silent = true }

      keymap('n', '<C-n>', ':NvimTreeToggle<CR>', opts)
      keymap('n', '<leader>ff', ':Telescope find_files<CR>', opts)
      keymap('n', '<leader>fg', ':Telescope live_grep<CR>', opts)
      keymap('n', '<leader>fb', ':Telescope buffers<CR>', opts)
      keymap('n', '<leader>fh', ':Telescope help_tags<CR>', opts)
      EOF
    '';
  };

  # Additional system packages
  environment.systemPackages = with pkgs; [
    # For markdown preview
    nodePackages.live-server

    # For LaTeX
    texlive.combined.scheme-full

    # For Graphviz
    graphviz
  ];
}
