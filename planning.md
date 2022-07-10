## Genius parse helper function
- `a`
    - Find inner `span`
    - Recurse
- `i`
    - Recurse
    - Wrap result in parens if it isn't already
- `br`
    - Ignore first break after an anchor
    - After that if we get 2 in a row (so 3 if after an anchor) do a newline.
    - Ignore all subsequent breaks
- `span` or `div`
    - Ignore, + ignore subsequent break like with anchor
- `\n`
    - If we get two in a row, put a blank line. Ignore everything after.
    - One break and one newline shouldn't result in a blank line.
- everything else
    - Strip, add to lyrics

### Preprocessing
- Replace any number of backslashes with one backslash before a newline

### Requirements
- Line spacing should be the same as it appears visually on the page
    - If there are multiple blank lines on the page, that should be reduced to one

- Anything in square brackets should be removed
- Italics should be parenthisized
- Parenthesized text should be unaltered
- Italic parenthesized text should remain singly parenthesized
- Need to properly handle annotations on the same line as non-annotated lyrics