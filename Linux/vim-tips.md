# Vim Commands Cheatsheet

## Modes

- **Normal Mode**: Default mode for navigation and commands
- **Insert Mode**: For typing text (`i`, `a`, `o`)
- **Visual Mode**: For selecting text (`v`, `V`, `Ctrl+v`)
- **Command Mode**: For ex commands (`:`)

## Basic Navigation

### Character Movement
- `h` - Left
- `j` - Down
- `k` - Up
- `l` - Right

### Word Movement
- `w` - Next word
- `b` - Previous word
- `e` - End of word
- `ge` - End of previous word

### Line Movement
- `0` - Beginning of line
- `^` - First non-blank character
- `$` - End of line
- `g_` - Last non-blank character

### Screen Movement
- `H` - Top of screen
- `M` - Middle of screen
- `L` - Bottom of screen
- `Ctrl+f` - Page down
- `Ctrl+b` - Page up
- `Ctrl+d` - Half page down
- `Ctrl+u` - Half page up

### File Movement
- `gg` - Go to first line
- `G` - Go to last line
- `:{number}` - Go to line number
- `%` - Go to matching bracket

## Editing

### Entering Insert Mode
- `i` - Insert before cursor
- `I` - Insert at beginning of line
- `a` - Insert after cursor
- `A` - Insert at end of line
- `o` - Open new line below
- `O` - Open new line above

### Deleting
- `x` - Delete character under cursor
- `X` - Delete character before cursor
- `dw` - Delete word
- `dd` - Delete line
- `D` - Delete to end of line
- `d$` - Delete to end of line
- `d0` - Delete to beginning of line

### Copying (Yanking)
- `yw` - Yank word
- `yy` - Yank line
- `Y` - Yank line
- `y$` - Yank to end of line

### Pasting
- `p` - Paste after cursor
- `P` - Paste before cursor

### Changing
- `cw` - Change word
- `cc` - Change line
- `C` - Change to end of line
- `r` - Replace single character
- `R` - Replace mode

### Undo/Redo
- `u` - Undo
- `Ctrl+r` - Redo
- `U` - Undo all changes on line

## Visual Mode

- `v` - Character visual mode
- `V` - Line visual mode
- `Ctrl+v` - Block visual mode
- `gv` - Reselect last visual selection
- `o` - Move to other end of selection

## Search and Replace

### Searching
- `/pattern` - Search forward
- `?pattern` - Search backward
- `n` - Next search result
- `N` - Previous search result
- `*` - Search for word under cursor (forward)
- `#` - Search for word under cursor (backward)

### Replace
- `:s/old/new/` - Replace first occurrence in line
- `:s/old/new/g` - Replace all occurrences in line
- `:%s/old/new/g` - Replace all occurrences in file
- `:%s/old/new/gc` - Replace all with confirmation

## File Operations

### Opening/Closing
- `:e filename` - Open file
- `:w` - Save file
- `:w filename` - Save as filename
- `:q` - Quit
- `:q!` - Quit without saving
- `:wq` - Save and quit
- `:x` - Save and quit (if changes)
- `ZZ` - Save and quit
- `ZQ` - Quit without saving

### Multiple Files
- `:split filename` - Open file in horizontal split
- `:vsplit filename` - Open file in vertical split
- `Ctrl+w h/j/k/l` - Navigate between splits
- `Ctrl+w c` - Close current split
- `:tabnew filename` - Open file in new tab
- `gt` - Next tab
- `gT` - Previous tab

## Buffers

- `:ls` - List buffers
- `:b{number}` - Switch to buffer number
- `:bn` - Next buffer
- `:bp` - Previous buffer
- `:bd` - Delete buffer

## Marks and Jumps

- `ma` - Set mark 'a'
- `'a` - Jump to mark 'a'
- `''` - Jump to previous position
- `Ctrl+o` - Jump to older position
- `Ctrl+i` - Jump to newer position

## Macros

- `qa` - Start recording macro 'a'
- `q` - Stop recording macro
- `@a` - Play macro 'a'
- `@@` - Repeat last macro

## Text Objects

- `iw` - Inner word
- `aw` - A word (including spaces)
- `is` - Inner sentence
- `as` - A sentence
- `ip` - Inner paragraph
- `ap` - A paragraph
- `i"` - Inner quotes
- `a"` - A quotes (including quotes)
- `i(` - Inner parentheses
- `a(` - A parentheses

## Folding

- `zf` - Create fold
- `zo` - Open fold
- `zc` - Close fold
- `za` - Toggle fold
- `zR` - Open all folds
- `zM` - Close all folds

## Useful Commands

- `.` - Repeat last command
- `J` - Join lines
- `~` - Toggle case
- `gU` - Uppercase
- `gu` - Lowercase
- `>>` - Indent line
- `<<` - Unindent line
- `=` - Auto-indent
- `Ctrl+n` - Auto-complete (in insert mode)
- `Ctrl+x Ctrl+f` - File name completion

## Settings

- `:set number` - Show line numbers
- `:set relativenumber` - Show relative line numbers
- `:set hlsearch` - Highlight search results
- `:set ignorecase` - Ignore case in searches
- `:set smartcase` - Smart case sensitivity
- `:set autoindent` - Auto-indent new lines
- `:set expandtab` - Use spaces instead of tabs
- `:set tabstop=4` - Set tab width to 4 spaces
- `:noh` - Clear search highlighting

## Quick Tips

- Use `Ctrl+[` or `Esc` to exit insert mode
- Use `:help command` to get help on any command
- Use `vimtutor` command in terminal for interactive tutorial
- Most commands can be prefixed with numbers for repetition (e.g., `5dd` deletes 5 lines)
- Combine operators with motions (e.g., `d3w` deletes 3 words)
