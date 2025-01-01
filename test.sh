
#!/bin/bash

# Initialize variables
neovim=1
kewlPrint=1

# Process command-line options
while getopts "nf" flag; do
    case $flag in
        n) neovim=0
        ;;
        f) kewlPrint=0
        ;;
    esac
done

# Output the values of the variables (for debugging)
echo "neovim = $neovim"
echo "kewlPrint = $kewlPrint"


# waka_c6ced30e-02f0-42f8-ab3f-0de4fabf6a2a
# 
