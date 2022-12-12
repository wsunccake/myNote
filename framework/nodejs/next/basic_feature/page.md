# page

## static generation

### static generation without data

```js
// pages/about.js
export default function About() {
  return <div>About</div>;
}
```

http://localhost:3000/about

### static generation with data

Scenario 1: Your page content depends on external data

```js
// pages/posts/index.js
export default function Home({ allPosts }) {
  return (
    <ul>
      {allPosts.map((post) => (
        <li>{post.title}</li>
      ))}
    </ul>
  );
}

// by getStaticProps
export async function getStaticProps() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts/");
  const posts = await res.json();
  //   const posts = [
  //     {
  //       id: 1,
  //       title: "google",
  //     },
  //     {
  //       id: 2,
  //       title: "facebook",
  //     },
  //   ];
  return { props: { allPosts: posts } };
}
```

Scenario 2: Your page paths depend on external data

```js
// pages/posts/[id].js
export default function Post({ post }) {
  return <h1>{post.title}</h1>;
}

// by getStaticProps
export async function getStaticPaths() {
  // const res = await fetch("https://jsonplaceholder.typicode.com/posts/");
  // const posts = await res.json();

  // const paths = posts.map((post) => ({
  //   params: { id: post.id.toString() },
  // }));
  const paths = [{ params: { id: "1" } }, { params: { id: "2" } }];

  // console.log(`paths: ${paths}`);
  // console.log(paths);

  return { paths, fallback: false };
}

// by getStaticProps
export async function getStaticProps(context) {
  // console.log(`context: ${context}`);
  // console.log(context);

  // const res = await fetch(
  //   `https://jsonplaceholder.typicode.com/posts/${context.params.id}`
  // );

  // const post = await res.json();
  const post = [
    {
      id: 1,
      title: "google",
    },
    {
      id: 2,
      title: "facebook",
    },
  ][context.params.id];
  return { props: { post } };
}
```

---

## server-side rendering

```js
export default function Home({ allPosts }) {
  return (
    <ul>
      {allPosts.map((post) => (
        <li>{post.title}</li>
      ))}
    </ul>
  );
}

export async function getServerSideProps() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts/");
  const posts = await res.json();

  //   const posts = [
  //     {
  //       id: 1,
  //       title: "google",
  //     },
  //     {
  //       id: 2,
  //       title: "facebook",
  //     },
  //   ];
  return { props: { allPosts: posts } };
}
```
