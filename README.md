# simple-py3-text-compressor
This simple Python program can olny compress the English alphabet (upper and lower case), most special symbols, space, newline, and digits (it is possible to exchange codes as needed, with the possibility to add tiers past 1, which increases the capacity to an infinite number of characters; however each additional tier decreases compression efficiency, which can easily go negative).<br>
It works by changing letters, symbols, and tiers into 5-bit codes, which then are written to the file as raw binary data. The CLI mode uses hex for easier demonstration due to the nature of some ASCII characters. <br>  
Every 5 compressed characters represent 8 uncompressed characters (when using only lowercase letters, space, colon, period, and newline, which is the most efficient for compression).<br>
You can use the CLI (with hex) or input a file.<br>
# Examples
Here's an example sentence.<br>
Before compression:<br>
`The quick, brown fox jumps over the 'lazy' dog!!!`<br>
After compression:<br>
`000000317f1ea2214542711da2b34d177775a2ec49ed2a897a1ea23d5820630ff470c60f3ffc00`<br>
As you can see, it works pretty well!<br>

> [!WARNING]
> **Character limit:** This program can compress texts up to only **4,294,967,295 characters** (2³²−1) — the max value a 4-byte header can store. Anything longer will raise a `struct.error` when compressing.
