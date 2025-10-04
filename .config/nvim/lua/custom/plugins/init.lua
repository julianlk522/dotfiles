return {
  {
    'Exafunction/codeium.vim',
    event = 'BufEnter',
  },
  {
    'sindrets/diffview.nvim',
  },
  {
    'nvim-neotest/neotest',
    dependencies = {
      'nvim-neotest/nvim-nio',
      'nvim-lua/plenary.nvim',
      'antoinemadec/FixCursorHold.nvim',
      'nvim-treesitter/nvim-treesitter',
      {
        'fredrikaverpil/neotest-golang',
        version = '*',
        build = function()
          vim.system({ 'go', 'install', 'gotest.tools/gotestsum@latest' }):wait()
        end,
      },
    },
    config = function()
      ---@diagnostic disable-next-line: missing-fields
      require('neotest').setup {
        adapters = {
          require 'neotest-golang' {
            go_test_args = { '-tags=fts5' },
            dap_go_enabled = false,
          },
        },
      }
    end,
  },
}
