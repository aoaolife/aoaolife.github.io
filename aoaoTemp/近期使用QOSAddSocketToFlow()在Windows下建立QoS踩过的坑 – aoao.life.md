---
title: "近期使用QOSAddSocketToFlow()在Windows下建立QoS踩过的坑 – aoao.life"
date: 2025-12-25 15:18:20
---

客户要求给原有Socket 通信增加QoS 功能，包括了Server 端和Client 端。示例代码似乎平平无奇，实装却花了三周半。尤其是最后的那个问题，困扰了我半个月。今天终于解决了，简单记录一下，希望能帮到需要的人。

## 第①个问题

现象：CreateQosHandle() 失败，GetLastError() = ERROR_NOT_SUPPORTED（50）
原因：CreateQosHandle()只有两个参数，出现这个错误是因为有的例子太老了，给第一个参传了{1, 1}。实际上进入Win10 时代之后第一个参就只能传{1, 0}。
解决办法：CreateQosHandle()第一个参传{1, 0}。

## 第②个问题

现象：QoSAddSocketToFlow() 失败，GetLastError() = WSA_INVALID_PARAMETER（87）
原因：
1）某些例子太老，第5个参传了0。新版本函数只能传两个定义好的宏：QOS_NON_ADAPTIVE_FLOW 和QOS_QUERYFLOW_FRESH，不能传0。本例的使用场景实际只能传QOS_NON_ADAPTIVE_FLOW。
2）我的PC上有两块网卡，连接内网环境的是第二块网卡。因此第2个参不能传NULL，而要通过给一个SOCKADDR结构体赋值IP 地址和Port 的方式，指定使用的网卡。
解决办法：第2个参在握手成功后过CAsyncSocket 的 GetPeerName() 取得连接用的IP地址和端口号，第5个参固定传QOS_NON_ADAPTIVE_FLOW。

## 第③个问题

现象：同时启动Server 和Client，Client 调用QoSAddSocketToFlow() 失败，GetLastError() = ERROR_NOT_FOUND（1168）
原因：添加QoS 的Socket 不支持用自己的Client 连接自己的Server。
解决办法：再找一台开发器。
P.S: 这个就是我上次吐槽AI的事件。

## 第④个问题

现象：在确定Socket握手成功的回调函数中添加QoS，Client 调用QoSAddSocketToFlow() 失败，GetLastError() = ERROR_ACCESS_DENIED（5）
原因：添加了QoS 的Server 需要管理员权限运行。
解决办法：调试时Server 端用管理员执行Visual Studio，或者给工程属性–Linker–Manifest File–UAC level 改成【requireAdministrator(/level=’requireAdministrator’)】。

## 第⑤个问题

现象：Client 的OnConnect(int nErrorCode) 回调中，有时nErrorCode = WSAEWOULDBLOCK（10035）
原因：这不是问题。只是Socket握手过程发生了延时。
解决办法：点两滴眼药水。

## 第⑥个问题

现象：Socket 连接建立后，Server 端立刻收到OnClose() 回调，并且传入的参数 = WSAECONNABORTED（10053）。
原因：既存的工程在Client创建socket的时候，立刻调用了SetSockOpt()设置了SO_LINGER，并且设定的值是{1, 0}，目地是Socket Close 时不等待缓存，直接进行硬关闭。但是这个属性如果在socket握手成功前被设定，那么在调用QoSAddSocketToFlow() 的同时就会产生这样的关闭。
解决办法：将SetSockOpt 的调用时机改到socket 连接建立之后，亦即，Client 端在OnConnect(0)后调用，Server 端在OnAccept(0) 后调用。

## 其它说明

10035本身不用管，但是跟10053长得太像了。
Server 端也不能用127.0.0.1，不知是否跟多网卡有关。
问题③、④和问题⑥干扰的选项太多，一度非常怀疑杀毒软件、防火墙、域策略，非常混乱。
问题①、②都是通过比较不同的例子找到的破绽。
问题③靠的是CSDN上的一句吐槽。
问题④最终解决靠的是在Git上广搜例子，在一个示例的说明里看到Server侧需要在管理员权限下运行的提示，方解决。
问题⑥最后是用了排除法编程，逐行注代码的笨办法筛出来的。全网没有人遇到同样的问题。可能就没有人提前设SO_LINGER 吧……

## 示例代码

共通类，继承CAsyncSocket：

```
#pragma once
#include <afxsock.h>
#include <qossp.h>
#include <winsock2.h>
#include <qos2.h>
#include <iostream>

#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "qwave.lib")

class CCommonQosSocket : public CAsyncSocket
{
public:
CCommonQosSocket()
: m_hQos(NULL)
, m_dwFlowId(0)
, m_ver({1, 0}){}
virtual ~CCommonQosSocket() {
CloseWithQos();
}

BOOL CreateQosHandle() {
if (m_hQos) {
QOSCloseHandle(m_hQos);
m_hQos = NULL;
}
if (!QOSCreateHandle(&m_ver, &m_hQos)) {
int nLastError = GetLastError();
return FALSE;
}
return TRUE;
}

BOOL GetPeerAddr(SOCKADDR_IN& peerAddr) {
int len = sizeof(peerAddr);
if (!GetPeerName((SOCKADDR*)&peerAddr, &len)) {
int n = GetLastError();
return FALSE;
}
return TRUE;
}

BOOL AddQosFlow(QOS_TRAFFIC_TYPE trafficType, SOCKADDR* pAddr) {
if (!m_hQos || !m_dwFlowId) {
return FALSE;
}

SOCKADDR* pTgtAddr(pAddr);
SOCKADDR_IN peerAddr{};
if (!pTgtAddr) {
if (!GetPeerAddr(peerAddr)) {
return FALSE;
}
pTgtAddr = static_cast<SOCKADDR*>(&peerAddr);
}

BOOL bRet = QOSAddSocketToFlow(m_hQos,
static_cast<SOCKET>(*this),
pTgtAddr,
trafficType,
QOS_NON_ADAPTIVE_FLOW,
&m_dwFlowId);
int nLastError = GetLastError();
return bRet;
}

void CloseWithQos() {
if (m_dwFlowId && m_hQos) {
QOSRemoveSocketFromFlow(m_hQos,
static_cast<SOCKET>(*this),
m_dwFlowId,
0);
}

if (m_hQos) {
QOSCloseHandle(m_hQos);
m_hQos = NULL;
}
m_dwFlowId = 0;
__super::Close();
}

private:
HANDLE      m_hQos;
DWORD       m_dwFlowId;
QOS_VERSION m_ver;
};
```

Server端部分代码：

```
#include "CommonQosSocket.h"

class CClientSocket: public CCommonQoSSocket {
};

class CListenSockt : public CCommonQoSSocket {
public:
virtual void OnAccept(int nErrorCode) override {
CAsyncSocket::OnAccept(nErrorCode);
CClientSocket* pNewClient = new CClientSocket;
sockaddr addr;
int iAddrLen = sizeof(addr);
if (Accept(*pNewClient, &addr, &iAddrLen)) {
pNewClient->CreateQosHandle();
if (pNewClient->AddQosFlow(QOSTrafficTypeBestEffort, &addr))
//sccess;
linger closeLinger{1,0};
(void)pNewClient->SetSockOpt(SO_LINGER, (const void*)&closeLinger, sizeof linger);
else {
//failed
}
}
};
};

void CQoSServerDlg::OnBnClickedButtonStart()
{
CClientSocket* pListen = new CClientSocket;
CString csLocalIP(L"192.168.8.4");
int nListenPort(32000);

if (!pListen->Create(nListenPort,
SOCK_STREAM, FD_READ | FD_WRITE | FD_ACCEPT | FD_CLOSE,
csLocalIP)) {
int nError = GetLastError();
AfxMessageBox(L"Listen Failed.");
return;
}

if (!m_ListenSock.Listen()) {
AfxMessageBox(L"Listen Failed.");
return;
}
}
```

Client端部分代码：

```
#include "CommonQosSocket.h"

class CClientSocket: public CCommonQoSSocket {
public:
virtual void OnConnect(int nErrorCode) overwride {
CAsyncSocket::OnConnect(nErrorCode);
if (nErrorCode) {
return;
}
CreateQosHandle();
if (this->AddQosFlow(QOSTrafficTypeBestEffort, nullptr)) {
//success
linger closeLinger{1,0};
(void)this->SetSockOpt(SO_LINGER, (const void*)&closeLinger, sizeof linger);
}
else {
//failed
}
}
};

void CQoSClientDlg::OnBnClickedButtonConnect()
{
CClientSocket* pClient = new CClientSocket;
pClient->CreateQosHandle();
CString csLocal(L"192.168.8.11");
CString csServer(L"192.168.8.4");
int nPort(32000);
pClient->Create(0, SOCK_STREAM, FD_READ | FD_WRITE | FD_CONNECT | FD_CLOSE,
csLocal);
if (m_sock.Connect(csServer, nPort)) {
}
else {
}
}
```

就酱紫，找到问题⑥的原因花了13天，改掉只需要5分钟。