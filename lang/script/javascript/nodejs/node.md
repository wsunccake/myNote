# node

## install

### node.js 20

```bash
# nvm / node version manager
linux:~ # curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
linux:~ # nvm install 22
linux:~ # node -v
linux:~ # npm -v

# binary
linux:~ # curl -LO https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz
linux:~ # xz -dc node-v22.12.0-linux-x64.tar.xz | tar xf - -C /usr/local/
linux:~ # ln -s /usr/local/node-v22.12.0-linux-x64/bin/{node,npm,npx} /usr/local/bin/.
```

### node.js 18

```bash
linux:~ # xz -dc node-v18.12.0-linux-x64.tar.xz | tar xf - -C /usr/local
linux:~ # ln -s /usr/local/node-v18.12.0-linux-x64/bin/{node,npm,npx} /usr/local/bin/.
```

---

## project

```bash
liunx:~ $ node -v

liunx:~ $ mkdir demo
liunx:~ $ cd demo
liunx:~/demo $ npm init -f
liunx:~/demo $ cat package.json
{
  "name": "demo",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
liunx:~/demo $ sed -i '6a"start": "node index.js",' package.json
liunx:~/demo $ echo 'console.log("hello js");' > index.js
liunx:~/demo $ npm start
```

---

## nvm

```bash
# install
linux:~ $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
linux:~ $ vi ~/.bashrc
...
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# uninstall
linux:~ $ nvm unload

# usage
linux:~ $ nvm --version
linux:~ $ nvm ls
linux:~ $ nvm ls-remote
linux:~ $ nvm install [--lts] [<version>]
linux:~ $ nvm use <version>

# example
linux:~ $ nvm install --lts [v18.12.0]
linux:~ $ nvm install v18.12.0
```
