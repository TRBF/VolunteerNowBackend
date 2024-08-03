#!/usr/bin/bash 

if [ ${BASH_SOURCE[0]} != ${0} ]; then
    source venv/bin/activate
    # clear
    
    unset neovim kewlPrint

    neovim=1 
    kewlPrint=1

    while getopts "nf" flag; do
        case "${flag}" in
            n)
              neovim_var=0
              neovim=$neovim_var
            ;;
            f)
              kewlPrint_var=0
              kewlPrint=$kewlPrint_var
            ;;
        esac
    done

    echo "KewlPrint is ${kewlPrint}"
    echo "Nvim is ${neovim}"

    if [ ${kewlPrint} -eq 1 ]; then 
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

    fi

    if [ ${kewlPrint} == 0 ]; then 
      echo "Fast initiated venv."
    fi
    
    if [ ${neovim} -eq 1 ]; then
        nvim
    fi
fi

if [ ${BASH_SOURCE[0]} == ${0} ]; then
   p="Please run this script either with \"source init_env.sh\" or \". ./init_env.sh\"" 
   echo "${p}"
fi

