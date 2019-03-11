#!/bin/sh

# Read from the file words.txt and output the word frequency list to stdout.
sed 's/  */ /g' words.txt | tr ' ' '\n' | sed '/^$/d' | sort  | uniq  -c | sort -k1 -r | awk '{print$2, $1}'
