---
title: JS入门（1）JSON对象的修改 | aoao.life
date: 2016-05-02 12:10:49
updated: 2026-03-01 06:20:12
---

题目描述，给定一个JSON对象，对它进行增删，更新等操作。

原本的程序是这样的：

```
// Setup
var collection = {
    2548: {
      album: "Slippery When Wet",
      artist: "Bon Jovi",
      tracks: [ 
        "Let It Rock", 
        "You Give Love a Bad Name" 
      ]
    },
    2468: {
      album: "1999",
      artist: "Prince",
      tracks: [ 
        "1999", 
        "Little Red Corvette" 
      ]
    },
    1245: {
      artist: "Robert Palmer",
      tracks: [ ]
    },
    5439: {
      album: "ABBA Gold"
    }
};

// Keep a copy of the collection for tests
var collectionCopy = JSON.parse(JSON.stringify(collection));

// Only change code below this line
function updateRecords(id, prop, value) {


  return collection;
}

// Alter values below to test your code
updateRecords(5439, "artist", "ABBA");
```

要求是这样的：

> For the given id in collection:

> If value is non-blank (value !== “”) and prop is not “tracks” then update or set the value for the prop.

> If the prop is “tracks” and value is non-blank, push the value onto the end of the tracks array.

> If value is blank, delete that prop.

> Always return the entire collection object.

我经过一番思考，写出的程序是这样的：

```
var collection = {
    2548: {
      album: "Slippery When Wet",
      artist: "Bon Jovi",
      tracks: [ 
        "Let It Rock", 
        "You Give Love a Bad Name" 
      ]
    },
    2468: {
      album: "1999",
      artist: "Prince",
      tracks: [ 
        "1999", 
        "Little Red Corvette" 
      ]
    },
    1245: {
      artist: "Robert Palmer",
      tracks: [ ]
    },
    5439: {
      album: "ABBA Gold"
    }
};
// Keep a copy of the collection for tests
var collectionCopy = JSON.parse(JSON.stringify(collection));

// Only change code below this line
function updateRecords(id, prop, value) {
if(value!==""&& prop!=="tracks"){
  collection.id.prop=value;
 
}
  
  else if(prop=="tracks"&&value!==""){
    collection.id.tracks.push(value);
  }
  else if(value===""){
    collection.id.prop.delete();
  }

  return collection;
}


// Alter values below to test your code
updateRecords(5439, "artist", "ABBA");
```

出现的错误提示是：  
 TypeError: Cannot set property ‘artist’ of undefined

个人其实在之前判断这个应该就是传递参数时遇到的问题，但是不知道怎么解决。在  
 collection.id.prop=value;  
   
这一行代码修改了很多遍，也看过一些例程。比如修改成：  
   
 collection.[id].[prop]=value  
又或者是：  
   
 collection.[“id”].prop=value

反正就是来回用[]试探了。 无效  
最后还是用谷歌搜索了一下，得到了[issues/5920](https://github.com/FreeCodeCamp/FreeCodeCamp/issues/5920)

有个网友回答的很到位：

> The problem is that id is not a property of collection. id is a variable that contains the name of a property of collection. You must use bracket notation to access it. IE collection[id]

所以我分析得多少还有几分道理，只是忘记了collection与[id] 之间是不能有符号. 的。这个时候使用[]也正是为了区分prop。

当然，我还发现了我的代码的其他问题，比如在一个array里面删除一个元素，可以用delete，但是我之前的用法：

```
collection.id.prop.delete();
```

显然是不对的，我是受到了上一个push命令的影响。实际上应该使用：  
   
 delete collection[id][prop]

修改后的代码为：

```
// Setup
var collection = {
    2548: {
      album: "Slippery When Wet",
      artist: "Bon Jovi",
      tracks: [ 
        "Let It Rock", 
        "You Give Love a Bad Name" 
      ]
    },
    2468: {
      album: "1999",
      artist: "Prince",
      tracks: [ 
        "1999", 
        "Little Red Corvette" 
      ]
    },
    1245: {
      artist: "Robert Palmer",
      tracks: [ ]
    },
    5439: {
      album: "ABBA Gold"
    }
};
// Keep a copy of the collection for tests
var collectionCopy = JSON.parse(JSON.stringify(collection));

// Only change code below this line
function updateRecords(id, prop, value) {
if(value!==""&& prop!=="tracks"){
  collection[id][prop]=value;
 
}
  
  
  else if(prop=="tracks"&&value!==""){
    collection[id][prop].push(value);
  }
  else if(value===""){
   delete  collection[id][prop];
  }

  return collection;
}


// Alter values below to test your code
updateRecords(2548, "artist", "");
```