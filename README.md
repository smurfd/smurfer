# smurfer
Need some smurfing done?

smurfer smurfs

Idea is to create a general worker that distributes the job between server and client, and you can define what you want it todo.

# Install
Install pyenv and virtualenv through your package manager. Some examples below:
```
$ brew install pyenv virtualenv # Mac with brew
$ apt install pyenv virtualenv  # Debian / Ubuntu
$ zypper in pyenv virtualenv    # openSUSE
$ dnf install pyenv virtualenv  # RedHat / Fedora
$ emerge -vaD pyenv virtualenv  # Gentoo
```
Or grab pyenv manually:
```
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
$ echo "export PATH=\"${PYENV_ROOT}/bin:\$PATH\"" >> ~/.zshrc
$ echo "eval \"\$(pyenv init -)\"" >> ~/.zshrc
$ echo "eval \"\$(pyenv virtualenv-init -)\"" >> ~/.zshrc
```
After pyenv & virtualenv is installed go ahead and:
```
$ pyenv install 3.8.12 (3.6.x and 3.7.x not supported on Mac m1)
$ git clone https://github.com/smurfd/smurfer
$ cd smurfer
$ pyenv local 3.8.12
$ virtualenv -p $HOME/.pyenv/versions/3.8.12/bin/python3 venv
$ source ./venv/bin/activate
$ pip3 install -r requirements.txt
```
Done.

Now in one terminal, run:
```
$ python3 srv.py
```
in another terminal run:
```
$ python3 cli.py
```
# Testing
`python3 -m pytest`

# TODO
- Set pid per worker
- pools of server ips/ports to listen on
- better folder structure
