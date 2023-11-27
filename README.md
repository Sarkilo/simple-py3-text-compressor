# simple-py3-text-compressor
This simple python program can compress only lowercase english alphabet plus 6 ASCII characters. (by default 4 chracters are used for space, dot, comma and apostrophe)
It works by changing text to bits and then saving letters 5bits each and then saving them back to numbers and ASCII characters. (for compressed text it doesn't use 'invicible' characters for easier use)
Every 5 compressed characters contains 8 characters uncompressed.
# Examples
Here's example sentence
Before compression:
`the quick, brown fox jumps over the 'lazy' dog.`
After compression:
`ēcñcIhÁĂ#ǱƇ+̎ǋnq9ɯǉu)ͱŝ\0TƝ%è[āS!`

As you can see it works pretty well
