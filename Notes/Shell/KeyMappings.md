### Compendium of key actions on a Terminal (Atleast most of them. It's mainly tested on Gnome)
- C-a - Jump to start of the line
- C-b - Go back one character in the same line
- C-c - Cancel the current command and open a new one
- C-d - When there is no character that's been entered, it quits the terminal.
        If there are characters, works like an auto-suggest
- C-e - Go to the End of the line. Complements C-a.
- C-f - Go forward one character. Complements C-b.
- C-g - Similar to C-c
- C-h - Deletes the character behind the cursor
- C-i - When the terminal is empty(with/without leading spaces), adds a tab.
        When the last char of command is a space and the cursor is on it, shows auto suggestions
- C-j - Executes the command. Equivalent to pressing enter.
- C-k - Deletes from cursor to the end of the line.
- C-l - Clear screen
- C-m - Executes the command. Similar to C-j
- C-n - Fetches the next command in history.
- C-o - Executes the command. Similar to C-j
- C-p - Fetches the previous command in history.
- C-q - Clears current line.
- C-r - Reverse command search
- C-s - Forward command search?? 
- C-t - Swaps the last 2 characters and moves ahead by - 
        2 chars if cursor's at the start, 1 char in the middle, 0 char if at end.
- M-t - Swap the word before and after the cursor, if at end of line swap the last two words
        (This does not work with <kbd>Alt</kbd> in Gnome Terminal as it captures thsi sequence
         and does not pass it to underlying shell use <kbd>Esc</kbd> instead)
- C-u - Clears current line. Similar to C-q
- C-v - Enter the next key pressed literally
- C-w - Clears alphanumeric chars from the chars behind the cursors till it's not alphanumeric.
- M-d - Delete the next word
- C-x - Selection of text. When cursor is at the end of the line, seems to select the entire line.
        The selection is a bit more involved when the cursor is somewhere in the middle(It keeps changing)
- C-y - Undo the clear done by C-w, C-u, (Not C-q). Pastes latest entry from the kill ring
- M-y - Paste the earlier entry from the kill ring (relevant only if last command was C-y or M-y)
- C-z - Suspend the currently running process
- C-/ - Undo last text edit
- M-f - Move forward one word (On Gnome terminal use <kbd>Esc</kbd> instead of <kbd>Alt</kbd>)
- M-b - Move back one word

### Other information, or points to remember that will be forgotten.
- <kbd>Alt</kbd> is the meta key in the Gnome version that comes out of the box in Ubuntu 16.04.
- In iTerm2 (And probably in some other terminals as well), <kbd>Esc</kbd> acts as the meta key.
  To map the <kbd>Esc</kbd> to <kbd>Alt</kbd> (which is called the option key in Mac), go to preferences/profile in iTerm2 and select 'Left Option key acts as - +Esc'.
