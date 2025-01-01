#!/usr/bin/bash 

if [ ${bash_source[0]} != ${0} ]; then
    source venv/bin/activate
    # clear
    
    unset neovim kewlprint

    neovim=1 
    kewlprint=1

    while getopts "nf" flag; do
        case "${flag}" in
            n)
              neovim_var=0
              neovim=$neovim_var
            ;;
            f)
              kewlprint_var=0
              kewlprint=$kewlprint_var
            ;;
        esac
    done

    echo "kewlprint is ${kewlprint}"
    echo "nvim is ${neovim}"

    if [ ${kewlprint} -eq 1 ]; then 
      message=$(cat ~/.res/venv_message) 
      for (( i = 0; i<${#message}; i++)); do 
          echo -n "${message:$i:1}"
          sleep 0.00005
      done

      echo ""
      message="godspeed gentlemen!!!"

      for (( i = 0; i<${#message}; i++)); do 
          echo "${message:$i:1}"
          sleep 0.02
      done

      for (( i = 0; i<50; i++)); do 
          echo " "
          sleep 0.02
      done

    fi

    if [ ${kewlprint} == 0 ]; then 
      echo "fast initiated venv."
    fi
    
    if [ ${neovim} -eq 1 ]; then
        nvim
    fi
fi

if [ ${bash_source[0]} == ${0} ]; then
   p="please run this script either with \"source init_env.sh\" or \". ./init_env.sh\"" 
   echo "${p}"
fi

