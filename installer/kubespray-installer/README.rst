kubespray-installer
====================

Set up kubernetes cluster using kubespray.

There are 3 steps in the script to complete set up the kubernetes cluster.

#. Get: get the latest kubespray release (v2.10.4 is the latest one at 
   https://github.com/kubernetes-sigs/kubespray/releases) and 
   add kubelet_max_pods to 110.::

    orchard@pengrixio-master:~$ cd ~/pengrixio/kubespray-installer
    orchard@pengrixio-master:~/..$ KS_COMMIT=v2.10.4 \
        ./setup.sh --get pengrixio

    orchard@pengrixio-master:~/..$ echo "kubelet_max_pods: 110" \
        | tee -a kubespray/roles/kubernetes/preinstall/defaults/main.yml

#. Prepare: create ansible variables and inventories for kubespray.::

    orchard@pengrixio-master:~/..$ HOST_PREFIX=pengrixio \
        REMOTE_SSH_USER=orchard \
        ./setup.sh --prepare pengrixio 192.168.10.1{0,1,2}

#. Install: run kubespray ansible playbook.::

    orchard@pengrixio-master:~/.../$ ./setup.sh --install pengrixio 

Source kubectl config file to use kubectl command.::

    orchard@pengrixio-master:~/.../$ ./setup.sh --source pengrixio
    orchard@pengrixio-master:~/.../$ source ~/.bashrc

