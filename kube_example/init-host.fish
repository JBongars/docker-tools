#!/bin/fish

apk update
apk add k9s kubectl kubectx kubens
apk add ncurses

export PATH

kind create cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml