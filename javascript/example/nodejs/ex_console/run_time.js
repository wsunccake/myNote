console.log(global); // global variable
console.log(__dirname);
console.log(__filename);

console.time('Run loop');
for (var i = 10; i > 0; i--) {
  console.log('%d loop', i);
}
console.timeEnd('Run loop');
