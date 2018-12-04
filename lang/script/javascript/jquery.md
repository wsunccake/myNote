# jQuery


## selector


## ready

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Title</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>

<body>
<p id="ready1">input ...</p>
<p id="ready2">input ...</p>
<p id="ready3">input ...</p>
</body>

<!-- DOM -->
<script>
    <!-- load -->
    window.onload = function () {
        console.log("hello javascript !");
        document.querySelector('#ready1').textContent = 'Hello JavaScript';
</script>

<!-- jQuery -->
<script>
    <!-- ready -->
    $(document).ready(function() {
        console.log("hello jquery !");
        $('#ready2').text('Hello jQuery');

    $(function() {
        console.log("hello jquery ...");
        $('#ready3').text('Hello jQuery');
    });
</script>

</html>
```


## click

`html`

```html
<p id="msg">input ...</p>
<div>
    <input type="text" id="click"/>
    <button id="clickBtn">click</button>
</div>
```

`jQuery`

```javascript
$('#clickBtn').click(function () {
	$('#msg').text("hello " +$('#click').val() + " !");
});
```

`DOM`

```javascript
document.querySelector('#clickBtn').addEventListener('click', function () {
	document.querySelector('#msg').textContent = 'hello ' + document.querySelector('#click').value + ' !';
});
```


## radio

`html`

```html
<p id="msg">input ...</p>
<div>
    <div>
        <input type="radio" id="radio1" name="radio" value="male"/>
        <label for="radio1">male</label>
    </div>
    <div>
        <input type="radio" id="radio2" name="radio" value="female"/>
        <label for="radio2">female</label>
    </div>
    <div>
        <button id="radioBtn">click</button>
    </div>
</div>
```

`jQuery`

```javascript
$('#radioBtn').click(function () {
	$('#msg').text($('input[name=radio]:checked').val());
});
```

`DOM`

```javascript
document.querySelector('#radioBtn').addEventListener('click', function () {
	var radios = document.getElementsByName('radio');
	var radioStr = '';
	for (var i = 0; i < radios.length; i++) {
		if (radios[i].checked) {
			radioStr = radios[i].value;
		}
	}
	document.querySelector('#msg').textContent = radioStr;
});
```

## option

`html`

```html
<p id="msg">input ...</p>
<div>
    <select id="sell" size="5" multiple>
        <option>windows</option>
        <option>macos</option>
        <option>linux</option>
        <option>ios</option>
        <option>android</option>
    </select>
    <button id="selectBtn">click</button>
</div>
```

`jQuery`

```javascript
$(function () {
	$('#selectBtn').click(function () {
		var msg = 'selected: ';
		$('#sell option:selected').each(function () {
			msg += $(this).val() + " ";
		});
		$('#msg').text(msg);
	});
});
```

`DOM`

```javascript
document.querySelector('#selectBtn').addEventListener('click', function () {
	var sel = document.querySelector('#sell');
	var opts = sel.getElementsByTagName('option');
	var msg = 'selected: ';
	for (var i = 0; i < opts.length; i++) {
		if (opts[i].selected) {
			msg += opts[i].value + ' ';
		}
	}
	document.querySelector('#msg').textContent = msg;
})
```
