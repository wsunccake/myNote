# Vue


## Hello

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Hello Vue!</title>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>    
</head>
<body>
<div id="app">
    {{ message }}
    {{ undefineMessage }}
</div>
<script>
var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
});

console.log(app.$data.message);
</script>
      
</body>
</html>
```

---

## v-

### v-if

```html
<div id="app">
    <p v-if="score > 60">pass</p>
    <p v-if="seen">v-if seen</p>
    <p v-show="seen">v-show seen</p>
</div>
<script>
var app = new Vue({
    el: '#app',
    data: {
        score: 80,
        seen: false
    }
});
</script>
```


### v-for

```html
<div id="app">
    <p>{{ weeks[1] }}</p>
    <ul><li v-for="n in 10">{{ n * 10 }}</li></ul>
    <ul><li v-for="day in weeks">{{ day.toUpperCase() }}</li></ul>
    <ul><li v-for="(v, k) in week">{{ k }} -> {{ v }}</li></ul>
</div>
<script>
var app = new Vue({
    el: "#app",
    data: {
        weeks: ["Sunda", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        week: {
            sun: "Sunday",
            mon: "Monday",
            tues: "Tuesday",
            wed: "Wednesday",
            thur: "Thursday",
            fri: "Friday",
            sat: "Saturday"
        }
    }
});
</script>
```


### v-model

```html
<div id="app">
    <p>{{ message }}</p>
    <input v-model="message">
</div>
<script>
var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
})
</script>  
```


---
