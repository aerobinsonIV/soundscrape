## Genius parse helper function
- `a`
- `i`
- `br`
- `span` or `div`
- `\n`
- everything else

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