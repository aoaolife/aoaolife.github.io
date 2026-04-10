---
title: "解决Win32下USB转串口一次只读一字节问题 – aoao.life"
date: 2019-09-03 17:16:58
---

最近项目遇到一个问题：从串口读数据时，如果使用 USB-Serial Adapter，那么每次读取只能读到1字节，循环读取效率特别低下。而如果是接 RS232 则不会产生这个问题。

推测这个问题产生的原因，是Win32下不同驱动程序产生 COMM 事件的时机不同。RS232是在受信缓冲区中产生一定量的数据之后，才会令API产生 EV_RXCHAR，而USB转串口的驱动，一收到数据就直接发生 EV_RXCHAR 了。

基于这个推论，再找解决办法。只要“等”一小会儿就可以了。那么等多久合适呢？
实验发现，受信缓冲区中数据的大小，其实存在ClearCommError()函数的输出参数的 COMSTAT 结构体中。
COMSTAT 的文档中说得很明确：

> cbInQue
>
> The number of bytes received by the serial provider but not yet read by a ReadFile operation.

这就好办了，只要等到这个值不发生变化，那就是收完了。
下面是代码示例，只是示意，不要照抄，编不过的。其精华就在于while。

```
bool MassRead(HANDLE hFile, UINT8* pBuff, UINT* pLen) {
UINT8 tmpBuf[1024] = {0};
DWORD dwRead(0);
DOWRD dwIn(0);
DWORD Err(0);
COMSTAT cs;

ClearCommError(h_drv, &Err, &cs);
while(dwIn < cs.cbInQue &#038;&#038; cs.cbInQue < 500)//一般串口的受信buff大小是512，避免缓冲区溢出。
{
dwIn = cs.cbInQue;
::Sleep(10);
ClearCommError(h_drv, &#038;Err, &#038;cs);
}

bool fResult = ReadFile (hFile, tmpBuf, sizeof(tmpBuf), &#038;dwRead, 0);
if (fResult&#038;&#038;dwRead) {
memcpy_s(pBuff, dwRead, tmpBuf, dwRead);
*pLen = dwRead;
}
return fResult;
}

DWORD dwCommModemStatus(0);
SetCommMask (h_drv, EV_RXCHAR | EV_ERR);
WaitCommEvent (h_drv, &#038;dwCommModemStatus, 0);

if (dwCommModemStatus&#038;EV_RXCHAR)
MassRead (h_drv, read_buf, sizeof(read_buf), &#038;len);
```