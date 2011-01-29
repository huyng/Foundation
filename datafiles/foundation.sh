function _fdncomplete_()
{
    local cmd="${1##*/}"                    # cmd being completed         
    local word=${COMP_WORDS[COMP_CWORD]}    # gets the word that's being completed
    local line=${COMP_LINE}                 # gets the entire line being completed
    local xpat                              # custom exclusion pattern
    local subcommands='add clip cdpath compgen open doc edit help list put remove locate new bundle'
    
    if [[ $COMP_CWORD -lt 2 ]]; then
        # only complete subcommands when there are less then 3 arguments on cmdline
        COMPREPLY=($(compgen -W "${subcommands}" -- "${word}"))
    elif [[ "$line" == *help* ]]; then
        COMPREPLY=($(compgen -W "${subcommands}" -- "${word}"))
    else
        # complete from completions file
        COMPREPLY=($(compgen -f -d -X '.[^./]*' -W  "$(cat ~/.foundation/completions)" -- "${word}"))
    fi
}

function _fdncd_complete_()
{
    local word=${COMP_WORDS[COMP_CWORD]}    # gets the word that's being completed
    COMPREPLY=($(compgen -X '.[^./]*' -W  "$(cat ~/.foundation/completions)" -- "${word}"))
}

function fdncd()
{
    cd "$(fdn cdpath $@)"
}

# -d means include directories
# -f means include files
# -X means exclude the following pattern
# -F use a function
# -W a word list ie -W "`cat ~/.iqe/deployment.completions`"
complete -F _fdncomplete_ fdn
complete -F _fdncd_complete_ fdncd
