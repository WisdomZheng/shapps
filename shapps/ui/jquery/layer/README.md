sample:
=============================
HTML:
-----------------------------
```
It does not need set html classes or attributes
```

JS:
-----------------------------
```
normal
$("button").click(function(){
    layer.alert('title', function(index){
    //do something
    layer.close(index);
    });
});

need confirm
$("button").click(function(){
    layer.confirm('is not?', {icon: 3, title:'confirm'}, function(index){
    //do something
    layer.close(index);
    });
});

prompt input
$("button").click(function(){
    layer.prompt({
    formType: 2, //input type: 0(default): text, 1: password, 2: multi-line text
    value: 'initial value',
    title: 'enter value',
    }, function(value, index, elem){
        alert(value); //get value
        layer.close(index);
    });
});

for detail usage, see: http://www.layui.com/doc/modules/layer.html
```
