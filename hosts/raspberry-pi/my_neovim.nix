{ config, lib, pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    viAlias = true;
    vimAlias = true;
    defaultEditor = true;

    configure = {
      customRC = ''
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

      packages.myVimPackage = with pkgs.vimPlugins; {
        start = [
          gruvbox-nvim
          nvim-tree-lua
          lualine-nvim
          vim-fugitive
          gitsigns-nvim
          nvim-lspconfig
          nvim-cmp
          cmp-nvim-lsp
          cmp-buffer
          cmp-path
          cmp-cmdline
          luasnip
          cmp_luasnip
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
          markdown-preview-nvim
          vimtex
          indent-blankline-nvim
          nvim-ufo
          promise-async
          telescope-nvim
          telescope-fzf-native-nvim
          comment-nvim
          nvim-autopairs
        ];
      };
    };
  };

  environment.systemPackages = with pkgs; [
    nodePackages.live-server
    texlive.combined.scheme-full
    graphviz
  ];
}
