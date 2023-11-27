#!/bin/fish

function cap
    tee /tmp/capture.out
end
  
function ret
    cat /tmp/capture.out
end

function recall
    if test (-f /tmp/capture.out)
        cat /tmp/capture.out
    end
end

function force_execute
    if test (count $argv) -eq 0
        echo "Usage: force_execute <command>"
        return 1
    end
    set -l command $argv[1]
    set -e argv[1]
    set -l args $argv

    if test -f $command
        dos2unix $command
    end
    chmod +x $command

    $command $args
end

function do_until_sucess
    if test (count $argv) -eq 0
        echo "Usage: do_until_sucess <command>"
        return 1
    end
    set -l command $argv
    set -l retries 0

    while true
        eval $command
        if test $status -eq 0
        break
        end
        set retries (math $retries + 1)
        echo "Retrying $command... ($retries)"
    end
end

function gb
    git for-each-ref \
        --sort='-committerdate:iso8601' \
        --format='%(committerdate:relative)|%(refname:short)|%(committername)' \
        refs/heads/ | column -s '|' -t
end

function gbh
    git for-each-ref \
        --sort='-committerdate:iso8601' \
        --format='%(committerdate:relative)|%(refname:short)|%(committername)' \
        refs/remotes/ | column -s '|' -t
end

if test -f ~/onload.sh
    . ~/onload.sh
end