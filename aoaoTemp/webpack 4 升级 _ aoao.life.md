---
title: webpack 4 升级 | aoao.life
date: 2018-05-14 18:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/webpack.png)

---

1 html-webpack-plugin 已支持webpack 4  
2 inline-manifest-webpack-plugin 的升级替换

inline-manifest-webpack-plugin 插件本身已支持webpack 4, 但从测试看有bug，不能将生成的manifest.js 插入到frontend-js.html 文件中。

解决方案，使用webpack-inline-manifest-plugin  
<https://github.com/szrenwei/inline-manifest-webpack-plugin/issues/10>

3 extract-text-webpack-plugin 的升级替换

项目主页：<https://github.com/webpack-contrib/extract-text-webpack-plugin>

Since webpack v4 the extract-text-webpack-plugin should not be used for css. Use mini-css-extract-plugin instead.

官方推荐使用 mini-css-extract-plugin 代替

因此根据mini-css-extract-plugin(<https://github.com/webpack-contrib/mini-css-extract-plugin>) 项目介绍 ，添加了一些mini-css-extract-plugin 的高级配置

4 CommonsChunkPlugin 废弃

<https://medium.com/webpack/webpack-4-code-splitting-chunk-graph-and-the-splitchunks-optimization-be739a861366>

提取common vendor。

5 不再使用 inline-chunk-manifest-html-webpack-plugin

项目没有更新，插件不支持webpack 4，考虑到本插件优化作用不大，可以先不用。

6 统一使用url-loader 处理非js，css（scss）等资源  
webpack在处理非js和css（scss）时，统一使用url-loader 。url-loader 本身是对file-loader 的扩展，当文件大小超过规定的限制时（目前limit为3kb），则将文件资源输出到指定文件夹中。

7 优化首屏，减少网络条件差时的白屏时间

head 里面的css 阻塞进程，使用webpack 3 时的CSS文件637kb。使用webpack 4 后，将url-loader limit 限制在3kb，使转base64 的资源越少越好，尽量不占用css的的空间。目前生产环境CSS 文件大小474kb。

8 升级后变化

升级前 build Done in 34.25s.  
升级后build Done in 22.72s.