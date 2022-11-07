# Table of contents
- [Integration of SRGAN](#integration-of-srgan)
  * [Ressources](#ressources)
  * [Description](#description)
  * [What have been done](#what-have-been-done)
  * [The github repository](#the-github-repository)
- [How to use the cluster](#how-to-use-the-cluster)
  * [Connect to the cluster](#connect-to-the-cluster)
  * [Useful bash commands](#useful-bash-commands)
  * [Installing python](#installing-python)
  * [Installing python packages](#installing-python-packages)
  * [Working on the cluster](#working-on-the-cluster)
  * [Job submissions](#job-submissions)
  * [Creating aliases](#creating-aliases)
  * [Creating a key for fast access to cluster](#creating-a-key-for-fast-access-to-cluster)
# Integration of SRGAN
## Ressources
- [Main UNIL wiki for the cluster](https://wiki.unil.ch/ci/books/service-de-calcul-haute-performance-%28hpc%29)
- [Physics-Informed Resolution-Enhancing GANs (PhIRE GANs)](https://github.com/NREL/PhIRE)
## Description
This repository contains the files used during the start of my project.
## What have been done
- Create a python working environment on the cluster
- Understand and use the cluster, the terminal and slurm (language used to communicate and ask ressources from the cluster)
- Understand and recreate Leo's results, but in a different region
## The github repository
The repository is organized in a data-dev-utils structure.
- **data** : folder where the data are stored. I haven't uploaded them to the github because they are heavy (> 10 TB)
- **dev** : where we develop code, using jupyter notebooks
- **utils** : where we store tested code and functions files
# How to use the cluster
## Connect to the cluster
> The followings things are done on the cmd from windows for connecting. Once connected to the CURNAGL cluster, you are on a linux bash terminal.

You can connect to the CURNAGL cluster through your computer terminal outside from campus, you must be connected to the VPN. Once open, you must type: <br>
1. `ssh USERNAME@curnagl.dcsr.unil.ch`, and press enter.
2. Enter your UNIL password. It is normal that you don't see when you are typing the password.

Now you are connected to the cluster, and you can navigate using the bash commands.
## Useful bash commands
| Command  | What it does                               |
|----------|--------------------------------------------|
| `ls`       | lists directory contents                   |
| `touch`    | creates a file<br>ex : touch text.txt      |
| `mkdir`    | creates a directory                        |
| `pwd`      | prints working directory                   |
| `cd`       | changes directory                          |
| `mv`       | moves or rename a directory                |
| `rmdir`    | removes a directory<br>*Use with caution!* |
| `locate`   | locates a specific file or directory       |
| `exit`     | exits out of a directory                   |
| `clear`    | clears the terminal window                 |
| `cp`       | copy files and directories                 |
| `ctrl + c` | cancels the work in progress               |
| `vim`      | launches the *vim* text editor             |
## Installing python
In order to work with python on the cluster, you have to install and configure it. First of all, everything should be done inside the *working* directory, you don't have enough memory on your *user* directory.
In fact. everything code related should be done inside the *working* directory.

On the CURNAGL wiki, there is [documentation on how to install it](https://wiki.unil.ch/ci/books/service-de-calcul-haute-performance-%28hpc%29/page/using-conda-and-anaconda).
## Installing python packages
[Documentation](https://wiki.unil.ch/ci/link/569#bkmrk-installing-packages)
## Working on the cluster
When you want to work or run code on the cluster, you have to connect to it and ask for an [interactive partition](https://wiki.unil.ch/ci/link/733#bkmrk-partitions%C2%A0).
First of all, you have to connect to the cluster using a local host configuration.
1. Connect to the cluster with `ssh -L localhost:WXYZ:localhost:WXYZ USERNAME@curnagl.dcsr.unil.ch`.<br>
WXYZ should be replaced by numbers and must be the same. *Exemple : localhost:4353:localhost4353*.
2. [Ask for ressource allocation](https://wiki.unil.ch/ci/link/733#bkmrk-partitions%C2%A0) with, for exemple, `salloc -c 1 --mem 50G -J int_cpu -p interactive -t 05:00:00`.<br>**Important!** Note the *granted job allocation number* and the *node number*, you will need it later.
4. Connect to the node allocated to you with `ssh -L localhost:WXYZ:localhost:WXYZ dna066` (the node number (here dna066) could be different for you).
5. Launch your python environnment.
6. Go to your working directory
7. Start working. I will show an exemple of how to launch a jupyter notebook : `jupyter notebook --no-browser --port WXYZ`.<br>
This will return a link, hosted locally, with which you can access your notebooks in your browser.
7. When finished working, use `scancel *granted_job_allocation_number*` to terminate the interactive partition.
## Job submissions
With slurm, you can make job submissions. I will not explain it here, there are plenty of tutorials on internet.<br>
[UNIL Documentation](https://wiki.unil.ch/ci/link/569#bkmrk-running-slurm-jobs-w).
## Creating aliases
When working with command line, it is really useful to create aliases in order to be faster. *Really faster*. For instance, I created an alias for every command I had to type a lot.
Here are some tutorials :
- [How to create bash aliases](https://linuxize.com/post/how-to-create-bash-aliases/)
- [Create aliases for ssh hosts](https://www.howtogeek.com/75007/stupid-geek-tricks-use-your-ssh-config-file-to-create-aliases-for-hosts/)
<br>*Ex : an alias for `ssh -L localhost:WXYZ:localhost:WXYZ USERNAME@curnagl.dcsr.unil.ch`*
## Creating a key for fast access to cluster
If you want to avoid typing your password every time you connect, you can create an ssh key ([UNIL Documentation](https://wiki.unil.ch/ci/link/1086#bkmrk-connection-with-a-ke)).
