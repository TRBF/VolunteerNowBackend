#!/usr/bin/bash 

if [ ${BASH_SOURCE[0]} != ${0} ]; then
    source venv/bin/activate
    clear
    message=$(cat ~/.res/venv_message) 
    for (( i = 0; i<${#message}; i++)); do 
        echo -n "${message:$i:1}"
        sleep 0.00005
    done
    echo ""
    message="GODSPEED GENTLEMEN!!!"
    for (( i = 0; i<${#message}; i++)); do 
        echo "${message:$i:1}"
        sleep 0.02
    done
    for (( i = 0; i<50; i++)); do 
        echo " "
        sleep 0.02
    done
    neovim=1 
    while getopts "n" flag; do
        case "${flag}" in
            n) neovim=0
            ;;
        esac
    done
    if [ ${neovim} == 1 ]; then
        nvim
    fi
fi

if [ ${BASH_SOURCE[0]} == ${0} ]; then
   p = "Please run this script either with \"source init_env.sh\" or \". ./init_env.sh\"" 
   echo p
fi

