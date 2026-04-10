---
title: "我的小狼毫输入法备忘录 – aoao.life"
date: 2022-07-04 16:53:32
---

## 基本规则

安装以后产生一个系统目录和一个用户目录。所有有的可配置项可以在系统目录找到参考，但不要修改任何系统目录下的内容。
用户目录也不要直接修改yaml文件，而应该修改xxxx.custom.yaml，因为这些文件在升级和重装时不会被覆盖。
大多数时候修改下面三个配置文件就可以满足要求：

- 〔全局设定〕 default.yaml ⇒ default.custom.yaml
- 〔UI设定〕 weasel.yaml ⇒ weasel.custom.yaml
- 〔预设输入方案副本〕 <方案标识>.schema.yaml ⇒ <方案标识>.custom.yaml

yaml文件的修改，用两个空格作为缩进的层级标志，千万不能使用TAB。
自己修改的.custom.yaml文件是补丁性质，所以一定要出现顶格写的【patch:】,且只能出现一次。
yaml文件中引号代表字符串，单引号双引号意义相同，转义字符仍旧是反斜线。大多数时候可以不打引号。
yaml的注释是#号，可以用在句首和句中。
包括yaml在内的所有配置文件都要保存成utf-8不带头格式。
如果要修改某一项，可以在项目之间加斜线，也可以利用缩进编写。比如，

```
patch:
"menu/page_size": 9
```

也可以写成：

```
patch:
menu：
page_size: 9
```

但是，第二种写法意味着配置项【menu:】除了【page_size】以外的其它项目都被清空。所以，在不确定某一项目下是否有多个设定时，要谨慎使用第二种格式。换句话说，第一种用于修改和追加，第二种用于重新定义和删除。

### 使修改生效

每次修改后，在小狼毫图标上右键→重新部署，即可。
如果配置内容无法生效，小狼毫将使用上一次正确的配置。
如果配置有错误，可以查看【%temp%】目录下名为rime.weasel.XXXX的log文件。默认ERROR，WARINNING和INFO三种格式都有，只需查看ERROR文件即可。
用户词典的喂养也可以通过菜单里的“输出用户词典”和“合入用户词典”进行操作，跟资料同步完全不冲突。

### 资料同步

可以使用网盘同步。安装完成后，修改用户自定义目录下的「installation.yaml」，做如下修改（不加patch）：

```
installation_id: "your-unique-id"
sync_dir: 'C:\Users\dazhi\OneDrive\.waselconfig'
```

在另外的机器上设定成相同的installation_id即可实现资料同步（其实是人家网盘帮你做的。）
注意：

- 选择用户资料同步，真正同步的资料只有字典相关的字频和自定义词。
- 用户文件夹下的所有文件都会被上传到同步文件夹，覆盖原有文件。所以如果两台机器想使用相同的配置，还没配的一定要手动把配置文件拷贝到用户文件夹。否则一点击同步，云文件夹里的配置文件都没了！
- lua文件和lua文件夹不会被上传到同步文件夹，需要自己手动想办法。

## 修改「default.custom.yaml」

这个文件针对的是所有的输入方案的共通配置项。

### 侯选项个数

```
patch:
menu/page_size: 9
```

### SHIFT上屏设置

原方案对shift的处理特别恶心，必须换掉。

```
patch:
ascii_composer/switch_key:    # ctrl&&shift 切换键效果
Caps_Lock: clear            # 清屏幕
Shift_L: commit_code        # 上档code
Shift_R: commit_code        # 上档code
Control_L: noop             # 不处理
Control_R: noop             # 不处理
```

### 全局快捷键

Ctrl加点切换全角半角标点，
Ctrl+Shift+T切换简体繁体，后面简拼输入法还会再定义一次Ctrl+Shift+4。这组快捷键源自google习惯，经常冲突，争取以后改掉。

```
patch：
key_binder:
bindings:
- { when: always, accept: Control+period, toggle: ascii_punct } # 切换西文/中文标点 Ctrl + .
- { when: always, accept: Control+Shift+t, toggle: zh_simp }    # Ctrl+Shift+T 切换简繁体（caps-lock模式下）
- { when: always, accept: Control+Shift+T, toggle: zh_simp }    # Ctrl+Shift+T 切换简繁体，正常模式时本句起作用，因为Shift按下时t已经被识别成大写的T
- { when: has_menu, accept: period, send: Page_Down }           # .翻页
- { when: paging, accept: comma, send: Page_Up }                # ,翻页
```

### 优化主菜单

使用分级的方法配置实际上是删除不需要的

```
patch：
schema_list:
- {schema: luna_pinyin_simp}                            #只保留朙月拼音·简化字
switcher/caption: "【菜单】"                               #修改菜单名
switcher/option_list_separator: "/"                       #替换全角斜线
switcher/hotkeys:                                         #呼叫菜单，删除默认的F4
- "Control+grave"
```

## 修改「weasel.custom.yaml」

这个配置文件主要管整体UI。

### 设置强制英文的应用

进入时不切换成中文的应用，就是配置项左边两个斜线中间的部分，注意所有程序名都要小写。
用斜线的方式添加是为了不覆盖已经存在的cmd.exe

```
patch:
app_options/devenv.exe/ascii_mode: true   #visual studio
app_options/code.exe/ascii_mode: true     #VScode
app_options/wrwb.exe/ascii_mode: true     #workbench
app_options/fm.exe/ascii_mode: true       #足球经理
```

### 修改输入框风格

方案可以用[配色工具](https://pewae.com/gaan/aHR0cHM6Ly9iZW5ueXlpcC5naXRodWIuaW8vUmltZS1TZWUtTWUv)作成。如果手写的话一定要注意，颜色的顺序是**#BBGGRR**

```
patch:
preset_color_schemes/aaa:                 #方案名（配置用）
name: "aaa"                             #方案名（显示用）
author: "大致"                           #作者（显示用）
text_color: 0xffe8ca
candidate_text_color: 0xfff8ee
back_color: 0x8b4e01
border_color: 0x8b4e01
hilited_text_color: 0xfff8ee
hilited_back_color: 0x8b4e01
hilited_candidate_text_color: 0x7ffeff
hilited_candidate_back_color: 0xa95e01
comment_text_color: 0xc69664
"style/horizontal": true                  #横排
"style/font_face": "Microsoft YaHei"      #微软雅黑
"style/font_point": 13                    #字号
"style/layout/border_width": 1            #边框宽度
"style/color_scheme": aaa                 #与前面起的名字一致
```

## 修改「luna_pinyin_simp.custom.yaml」

为了方便维护，把自己的方案放在 atsymbols.yaml中。import_preset的意思是引入默认方案，参数是配置文件的名字。

### 自定义符号方案

```
patch:
punctuator/import_preset: atsymbols
recognizer/patterns/punct: '^[@/]([0-9]0?|[A-Za-z]+)$' #/开头输入各种符号，@开头输入数字变体，通过正则识别。
```

### 让输入框可以输入【/】

alphabet的意思是输入法可以接受的字符，这里还有两个，可以用于开头的字符和只能用于结尾的字符。但是这里用不上。

```
patch:
speller/alphabet: 'zyxwvutsrqponmlkjihgfedcba/'        #增加一个/用于符号输入
```

### 删除不需要的模糊音和错误拼写

从原版luna_pinyin_simp.schema.yaml中拷贝出来，采用分行模式，就是为了删除。这一part保留原项目，就是为了记录为什么要删。

```
patch:
speller/algebra:
#- erase/^xx$/                          #闲的没事儿干敲两个x?
- abbrev/^([a-z]).+$/$1/                #区别词里各个字的首字母，保留
- abbrev/^([zcs]h).+$/$1/               #zhchsh的精确识别，保留。“谬种流传”⇒“mzhlch”
- derive/^([nl])ve$/$1ue/               #luenue转成lvenve，保留，习惯改不掉了。
#- derive/^([jqxy])u/$1v/               #看见鱼眼要挖去，不会犯的错误。
#- derive/un$/uen/                      #不会犯的错误
#- derive/ui$/uei/                      #不会犯的错误
#- derive/iu$/iou/                      #不会犯的错误
#- derive/([aeiou])ng$/$1gn/            #不会犯的错误
#- derive/([dtngkhrzcs])o(u|ng)$/$1o/   #不会犯的错误
#- derive/ong$/on/                      #不会犯的错误
#- derive/ao$/oa/                       #不会犯的错误
#- derive/([iu])a(o|ng?)$/a$1$2/        #不会犯的错误
```

### 转换和翻译项

### 先从原版luna_pinyin_simp.schema.yaml中拷贝出来，主要是添加了lua函数显示日期时间数字大写等。

```
patch:
engine/translators:
- punct_translator                    #保留
- table_translator@custom_phrase      #自定义短语识别，保留
- script_translator                   #不知道干什么的，保留
- lua_translator@time_translator      #当前时间， time， shijian
- lua_translator@number_translator    #数字转大小写中文 IXXXXXX
- lua_translator@date_translator      #当前日期 date， riqi
- lua_translator@week_translator      #星期几 xingqi， xqj
```

## 使用lua

外部接口见上面的lua_translator，@后面是自己定义的关键字。这个关键字要写在「rime.lua」中。
lua格式的注释是两个横线–
require()函数的参数要传用户目录下**lua目录**下XXX.lua文件的名字。
当前的「rime.lua」：

```
time_translator = require("time")
number_translator = require("number")
date_translator = require("date")
week_translator = require("week")
```

lua的功能，只列一个time为例。文件名一定要是「time.lua」
input是输入键值的内容。每一个yield都是一个表示项。

```
local function translator(input, seg)
if (input == "time" or input == "now" or input == "shj" or input == "shij" or input == "shijian") then
yield(Candidate("time", seg.start, seg._end, os.date("%H:%M"), " "))
yield(Candidate("time", seg.start, seg._end, os.date("%H:%M:%S"), " "))
end
end

return translator
```

其余的lua就不贴了，github上都有。

## 修改「atsymbols.yaml」

这个文件就是前面提到修改「luna_pinyin_simp.custom.yaml」所用到的符号方案，完全可以不独立出来。独立出来只是为了清晰。
这个文件不带custom，所以没有patch！

### 符号表

自定义标点只需要定义半角的，全角基本没用，如果有需要加一个全角空格也就是了。
习惯源自谷歌输入法，只有@、~和$略作修改。
【-】开头是列表的意思，当一个按键只对应一个值是，值就会直接上到屏幕上，当有多个值时会出现选择列表。这也是之前很多教程把输入符号的开始标志改到@上的原因。

```
punctuator:
half_shape:
"!": "！"
""":
pair:
- "“"
- "”"
"#": "#"
"$":
- "$"
- "￥"
"%": "%"
"&": "&"
"'":
pair:
- "‘"
- "’"
"*": "*"
"+": "+"
",": "，"
"-": "-"
".": "。"
"/": "/"
"\": "、"
":": "："
";": "；"
"=": "="
"?": "？"
"@":
- "@"
- "•"     #中点号
- "℃"     #摄氏度
- "℉"     #华氏度
- "°"     #度
"(": "（"
")": "）"
"[": "【"
"]": "】"
"{": "「"
"}": "」"
"<": "《"
">": "》"
"^": "……"
"_": "——"
"`": "·"
"|": "|"
"~":
- "~"
- "～"
```

### 增加的特殊符号

【/】开头显示符号，正常明月输入法不能用/作为识别标志，被我用别的方法修改了，见后。
拼音输入法数字被选择功能占用，正常字母包括/号后面都不能接数字,所以另外定义一个【@】开头的快捷键,用来输入数字相关的符号。

```
symbols:
#符號、電腦
'/fh': [ ©, ®, ℗, ℠, ™, ℡, ℻, ‰, °, ÷, ×, ♩, ♪, ♫ ]
#撲克
'/pk': [ ♠, ♥, ♣, ♦, ♤, ♡, ♧, ♢ ]
#星號
'/xh': [ ★, ☆, ※, ⛤, ⛥, ⛦, ⛧, ✡, ❋, ❊, ❉, ❈, ❇, ❆, ❅, ❄, ❃, ❂, ❁, ❀, ✿, ✾, ✽, ✼, ✻, ✺, ✹, ✸, ✷, ✶, ✵, ✴, ✳, ✲, ✱, ✰, ✯, ✮, ✭, ✬, ✫, ✪, ✩, ✧, ✦, ✥, ✤, ✣, ✢ ]
#方塊
'/fk': [ ■, □, ◆, ◇, ▞ ]
#圓圈
'/yq': [ ⚪, ⚫, ◦, ◎ ]
#三角
'/sj': [ △, ▲, ▼, ▽, ∴, ∵, ▶, ▷, ◀, ◁]
#箭頭
'/jt': [ ⇒, ⇐, ↑, ↓, ←, →, ⇓, ⇑, ⇔, ↖, ↗, ↙, ↘, ↹, ↺, ↻, ⇄, ⇅, ⇋, ⇏, ⇖, ⇗, ⇘, ⇙, ⇠, ⇡, ⇢, ⇣, ⇦, ⇧, ⇨, ⇩, ⇳, ➠, ➤, ➥, ➦, ➨, ➳, ➴, ➵, ➶, ➷, ➸, ➹, ➼, ➽, ↕, ↔, ⇶, ➔, ➾ ]
#數學
'/maths': [ ±, ÷, ×, ∈, ∏, ∑, －, ＋, ＜, ≮, ＝, ≠, ＞, ≯, ∕, √, ∝, ∞, ∟, ∠, ∥, ∧, ∨, ∩, ∪, ∫, ∮, ∴, ∵, ∷, ∽, ≈, ≌, ≒, ≡, ≤, ≥, ≦, ≧, ⊕, ⊙, ⊥, ⊿, ㏑, ㏒ ]
#希臘
'/xl': [ α, β, γ, δ, ε, ζ, η, θ, ι, κ, λ, μ, ν, ξ, ο, π, ρ, σ, ς, τ, υ, φ, χ, ψ, ω ]
'/xld': [ Α, Β, Γ, Δ, Ε, Ζ, Η, Θ, Ι, Κ, Λ, Μ, Ν, Ξ, Ο, Π, Ρ, Σ, Τ, Υ, Φ, Χ, Ψ, Ω ]
#拼音、註音、聲調
'/py': [ ā, á, ǎ, à, ō, ó, ǒ, ò, ê, ê̄, ế, ê̌, ề, ē, é, ě, è, ī, í, ǐ, ì, ū, ú, ǔ, ù, ü, ǖ, ǘ, ǚ, ǜ ]
'/sd': [ ˉ, ˊ, ˇ, ˋ, ˙]

#數字、分數
'@0': [ 〇, 零, ₀, ⁰, ⓪, ⓿ , ０]
'@1': [ 一, 壹, ₁, ¹, Ⅰ, ⅰ, ①, ➀, ❶, ➊, ⓵, ⑴, ⒈, １, ㊀, ㈠, 弌, 壱, 幺, ㆒ ]
'@2': [ 二, 貳, ₂, ², Ⅱ, ⅱ, ②, ➁, ❷, ➋, ⓶, ⑵, ⒉, ２, ㊁, ㈡, 弍, 弐, 貮, 㒃, 㒳, 兩, 倆, ㆓]
'@3': [ 三, 叄, ₃, ³, Ⅲ, ⅲ, ③, ➂, ❸, ➌, ⓷, ⑶, ⒊, ３, ㊂, ㈢, 參, 参, 叁, 弎, 仨, ㆔]
'@4': [ 四, 肆, ₄, ⁴, Ⅳ, ⅳ, ④, ➃, ❹, ➍, ⓸, ⑷, ⒋, ４, ㊃, ㈣, 亖]
'@5': [ 五, 伍, ₅, ⁵, Ⅴ, ⅴ, ⑤, ➄, ❺, ➎, ⓹, ⑸, ⒌, ５, ㊄, ㈤, 㐅, 㠪, 𠄡 ]
'@6': [ 六, 陸, ₆, ⁶, Ⅵ, ⅵ, ⑥, ➅, ❻, ➏, ⓺, ⑹, ⒍, ６, ㊅, ㈥, ↅ]
'@7': [ 七, 柒, ₇, ⁷, Ⅶ, ⅶ, ⑦, ➆, ❼, ➐, ⓻, ⑺, ⒎, ７, ㊆, ㈦, 漆]
'@8': [ 八, 捌, ₈, ⁸, Ⅷ, ⅷ, ⑧, ➇, ❽, ➑, ⓼, ⑻, ⒏, ８, ㊇, ㈧ ]
'@9': [ 九, 玖, ₉, ⁹, Ⅸ, ⅸ, ⑨, ➈, ❾, ➒, ⓽, ⑼, ⒐, ９, ㊈, ㈨ ]
'@10': [ 十, 拾, ₁₀, ¹⁰, Ⅹ, ⅹ, ⑩, ➉, ❿, ➓, ⓾, ⑽, ⒑, １０, ㊉, ㈩, 什 ]
```

## 自定义短语文件「custom_phrase.txt」

明月输入已经支持了自定义短语，不用再配置生效。创建一个名为「custom_phrase.txt」utf-8的文本文件，放到用户目录下。
内容为<转换后><输入键值><权重>。这次一定要用tab分割，而且只能用一个，不能多。
自定义短语不是词典，不能简化识别。比如定义AA制的缩略码是aazhi，那么敲aaz的时候就不会被识别出来。
下面是简单例子，最后一个参数是优先级。数字越大优先级越高，优先级越高，该词越会被配在前面。

```
A片	apian	1
AA制	aazhi	1
装B	zhuangb	2
装B犯	zhuangbfan	2
```

## 相关地址

- [我的配置方案](https://pewae.com/gaan/aHR0cHM6Ly9naXRodWIuY29tL2xpZmlzaGFrZS9Eb2NQdWJsaWMvdHJlZS9tYXN0ZXIvcmltZQ==)
- [官网](https://pewae.com/gaan/aHR0cHM6Ly9yaW1lLmlt)
- [下载](https://pewae.com/gaan/aHR0cHM6Ly9naXRodWIuY29tL3JpbWUvd2Vhc2Vs)
- [官方文档](https://pewae.com/gaan/aHR0cHM6Ly9naXRodWIuY29tL3JpbWUvaG9tZS93aWtpL0N1c3RvbWl6YXRpb25HdWlkZQ==)
- [比较好的非官方参数说明](https://pewae.com/gaan/aHR0cHM6Ly94aXNoYW5zbm93LmdpdGh1Yi5pby9wb3N0cy80MWFjOTY0ZA==)
- [重要参考文档](https://pewae.com/gaan/aHR0cHM6Ly9zaC5hbHlueC5vbmUvcG9zdHMvTXktUklNRS8=)
- [参考教程](https://pewae.com/gaan/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzMTA4MDkwL2FydGljbGUvZGV0YWlscy8xMjI3NTk2NDc=)