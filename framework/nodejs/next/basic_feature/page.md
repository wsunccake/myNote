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

```js
// scenario 1: page content depends on external data
export default function Home({ allPokemons }) {
  return (
    <ul>
      {allPokemons.map((poke) => (
        <li key={poke.url}>{poke.name}</li>
      ))}
    </ul>
  );
}

// getStaticProps
export async function getStaticProps() {
  //   const response = await fetch("https://pokeapi.co/api/v2/pokemon/");
  //   const data = await response.json();

  const data = {
    results: [
      {
        name: "bulbasaur",
        url: "https://pokeapi.co/api/v2/pokemon/1/",
      },
      {
        name: "ivysaur",
        url: "https://pokeapi.co/api/v2/pokemon/2/",
      },
      {
        name: "venusaur",
        url: "https://pokeapi.co/api/v2/pokemon/3/",
      },
    ],
  };

  return {
    props: { allPokemons: data.results },
  };
}
```

### page with dynamic route

---
