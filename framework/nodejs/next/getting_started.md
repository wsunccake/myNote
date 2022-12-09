# getting started

## auto setup

```bash
linux:~ $ npx create-next-app@latest
linux:~ $ cd my-app
linux:~/my-app $ tree -L 1
.
├── next.config.js
├── next-env.d.ts
├── node_modules
├── package.json
├── package-lock.json
├── pages
├── public
├── README.md
├── styles
└── tsconfig.json

4 directories, 6 files

# dev mode
linux:~/my-app $ npm run dev

# prod mode
linux:~/my-app $ npm run build
linux:~/my-app $ npm run start

# test
linux:~ $ curl http://localhost:3000
```

## manual setup

```bash
linux:~/hello $ npm install next react react-dom
linux:~/hello $ tree -L 1
.
├── node_modules
├── package.json
└── package-lock.json

1 directory, 2 file

linux:~/hello $ vi package.json
...
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }

linux:~/hello $ cat << EOF > pages/index.js
function HomePage() {
  return <div>Welcome to Next.js!</div>
}

export default HomePage
EOF

# dev mode
linux:~/my-app $ npm run dev

# prod mode
linux:~/my-app $ npm run build
linux:~/my-app $ npm run start

# test
linux:~ $ curl http://localhost:3000
```
