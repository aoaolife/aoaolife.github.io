---
title: "使用CMFCDynamicLayoutLayout动态修改MFC画面上控件的大小和位置 – aoao.life"
date: 2022-03-05 00:11:19
---

MFC想要实现对话框中窗口拖拽时自动改变控件的位置和大小，在Visual Studio 2015之前只能自己写方法进行计算。
Visual Studio 2015以后，MFC增加了一个叫做CMFCDynamicLayout的类，来处理画面上这些需要自适应大小的控件。
微软[官方介绍的文档](https://pewae.com/gaan/aHR0cHM6Ly9kb2NzLm1pY3Jvc29mdC5jb20vemgtY24vY3BwL21mYy9keW5hbWljLWxheW91dD92aWV3PW1zdmMtMTcw)在这里。
如果窗口是静态创建的，那么用提到的第一种方法就足够了。
但如果想用实现通过编程的手段动态修改控件的缩放方式和对齐目标，该文档的第二部分就不够用了。

可能是MFC这个东西明日黄花，2015年出的这个“新”功能明显不够重视，今天使用它的时候踩了好几个坑。索性封装成了一个CDialog类，只需实现一个方法就能实现画面控件的自动控制，岂不美哉！
类的具体内容如下：

## 头文件

```
#pragma once
#include <afxdialogex.h>

class CAdjustableDialogEx :
public CDialogEx
{
public:
CAdjustableDialogEx(UINT unIDTemplate, CWnd* pParent = NULL);
virtual ~CAdjustableDialogEx();
virtual BOOL OnInitDialog();
DECLARE_MESSAGE_MAP()
afx_msg void OnGetMinMaxInfo(MINMAXINFO* lpMMI);
typedef enum _em_align_types {
EM_ALIGN_TOPLEFT = 0,
EM_ALIGN_RIGHT,
EM_ALIGN_BOTTOM,
EM_ALIGN_BOTTOMRIGHT,
EM_ALIGN_MAX,
}EM_ALIGN_TYPES;
typedef enum _em_resize_types {
EM_RESIZE_NONE = 0,
EM_RESIZE_FULL_HEIGHT,
EM_RESIZE_FULL_WIDTH,
EM_RESIZE_FULL_FULL,
EM_RESIZE_MAX,
}EM_RESIZE_TYPES;

protected:
virtual void FillComponentList() {};
virtual void FillComplexComponentList(PVOID param) {};
void ResetLayout(PVOID param = NULL);
BOOL AddControl(
const CWnd& cwnd,
const EM_ALIGN_TYPES emAlign,
const EM_RESIZE_TYPES emResize
);
BOOL AddControl(
const int nID,
const EM_ALIGN_TYPES emAlign,
const EM_RESIZE_TYPES emResize
);
BOOL AddComponent(
const HWND hwnd,
const EM_ALIGN_TYPES emAlign,
const EM_RESIZE_TYPES emResize
);
private:
CRect               m_crOriginalDlgSize;
CMFCDynamicLayout*  m_pLayout;
};
```

## 实现文件

```
#include "stdafx.h"
#include "AdjustableDialogEx.h"
#include <afxlayout.h>

CAdjustableDialogEx::CAdjustableDialogEx(UINT unIDTemplate, CWnd* pParent)
: CDialogEx(unIDTemplate, pParent)
, m_pLayout(NULL)
, m_crOriginalDlgSize(0, 0, 0, 0)
{
}

CAdjustableDialogEx::~CAdjustableDialogEx()
{
}

BEGIN_MESSAGE_MAP(CAdjustableDialogEx, CDialogEx)
ON_WM_GETMINMAXINFO()
END_MESSAGE_MAP()

BOOL CAdjustableDialogEx::OnInitDialog()
{
CDialogEx::OnInitDialog();

this->GetWindowRect(m_crOriginalDlgSize);
this->ResetLayout();

return TRUE;

}

void CAdjustableDialogEx::OnGetMinMaxInfo(MINMAXINFO* lpMMI)
{
lpMMI->ptMinTrackSize.x = m_crOriginalDlgSize.Width();
lpMMI->ptMinTrackSize.y = m_crOriginalDlgSize.Height();
CDialogEx::OnGetMinMaxInfo(lpMMI);
}

void CAdjustableDialogEx::ResetLayout(PVOID param)
{
if (this->IsDynamicLayoutEnabled())
{
this->EnableDynamicLayout(FALSE);
m_pLayout = NULL;
}
this->EnableDynamicLayout(TRUE);
m_pLayout = this->GetDynamicLayout();
if (!m_pLayout)
{
return;
}
m_pLayout->Create(this);
if (param)
{
FillComplexComponentList(param);
}
else
{
FillComponentList();
}
if (m_pLayout->IsEmpty())
{
this->EnableDynamicLayout(FALSE);
m_pLayout = NULL;
}
}

BOOL CAdjustableDialogEx::AddControl(
const CWnd& cwnd,
const EM_ALIGN_TYPES emAlign,
const EM_RESIZE_TYPES emResize
)
{
return AddComponent(
cwnd.GetSafeHwnd(),
emAlign,
emResize);
}

BOOL CAdjustableDialogEx::AddControl(
const int nID,
const EM_ALIGN_TYPES emAlign,
const EM_RESIZE_TYPES emResize
)
{
return AddComponent(
this->GetDlgItem(nID)->GetSafeHwnd(),
emAlign,
emResize);
}

BOOL CAdjustableDialogEx::AddComponent(
const HWND hwnd,
const EM_ALIGN_TYPES emAlign,
const EM_RESIZE_TYPES emResize
)
{
if (!::IsWindow(hwnd) || !m_pLayout)
{
return FALSE;
}
if (m_pLayout->HasItem(hwnd))
{
return TRUE;
}
CMFCDynamicLayout::MoveSettings ms = CMFCDynamicLayout::MoveNone();
CMFCDynamicLayout::SizeSettings ss = CMFCDynamicLayout::SizeNone();
switch (emAlign)
{
case EM_ALIGN_RIGHT:
ms = CMFCDynamicLayout::MoveHorizontal(100);
break;
case EM_ALIGN_BOTTOM:
ms = CMFCDynamicLayout::MoveVertical(100);
break;
case EM_ALIGN_BOTTOMRIGHT:
ms = CMFCDynamicLayout::MoveHorizontalAndVertical(100, 100);
break;
default:
//SizeNone
break;
}
switch (emResize)
{
case EM_RESIZE_FULL_HEIGHT:
ss = CMFCDynamicLayout::SizeVertical(100);
break;
case EM_RESIZE_FULL_WIDTH:
ss = CMFCDynamicLayout::SizeHorizontal(100);
break;
case EM_RESIZE_FULL_FULL:
ss = CMFCDynamicLayout::SizeHorizontalAndVertical(100, 100);
break;
default:
//MoveNone
break;
}

return m_pLayout->AddItem(hwnd, ms, ss);
}
```

## 使用要点

1. 创建CDialog，并且把继承的基类改为CAdjustableDialogEx
2. 提供两个函数FillComponentList()/FillComplexComponentList()供子类重写。在这两个子函数中可以调用基类方法AddControl()和AddComponent()追加要自动变换位置和大小的控件。第一个参数是控件ID/控件CWnd类/控件句柄，第二个参数是控件相对位移的基准点/边，第三个参数是控件缩放相对父窗口的哪个边。
3. 如果调用该基类的OnInitDialog，那么FillComponentList()函数会被自动调用一次。也可以自己手动调用ResetLayout()函数使控件的设置生效。如果给ResetLayout()函数传非空参数，那么基类将调用FillComplexComponentList函数，并将该参数传回，用以实现切换控件对其方式等功能。否则将调用FillComponentList()。如果两个函数都未被重写，则视为关闭功能。
4. 重写OnGetMinMaxInfo()函数跟DynamicLayout功能并无直接关系。这是维护窗口原始大小的常规操作。CMFCDynamicLayout::SetMinSize()虽然可以保证控件不再缩小，但无法控制父画面。
5. ResetLayout()必须在基类的OnInitDialog之后调用。而如果使用MoveWindow之类的函数动态修改了控件的大小或者位置，一定要重新调用ResetLayout()以记录新位置。
6. 为什么使用蹩脚的方式实现ResetLayout()？
因为CMFCDynamicLayout本身没有Reset功能，控件也只能加不能删除，一经追加也无法修改变化方式。
官方文档的第一步pDialog->GetDynamicLayout();就有问题。实际情况是如果该窗口的IsDynamicLayoutEnabled()为TRUE，那么将返回一个有效指针，**否则返回空指针**。
而这个指针取得之后，也不能像文档中说的那样在第五步直接使用。实际情况是，如果动态激活（而不是静态在RC里设好）窗口的EnableDynamicLayout()，那么这样取得的pLayout里什么没有，必须使用CMFCDynamicLayout::Create()绑定父窗口才行。
所以，反过来想，如果想抹掉已经添加的Layout，只要Disable再Enable，不就全没了吗？

## 使用例子：

```
#pragma once
#include "..\class\AdjustableDialogEx.h"
#include "afxwin.h"

class CDemoAppDlg : public CAdjustableDialogEx
{

public:
CDemoAppDlg(CWnd* pParent = NULL);

#ifdef AFX_DESIGN_TIME
enum { IDD = IDD_DEMOAPP_DIALOG };
#endif

protected:
virtual void DoDataExchange(CDataExchange* pDX);

protected:
virtual BOOL OnInitDialog();
DECLARE_MESSAGE_MAP()
void FillComplexComponentList(PVOID param);
public:
afx_msg void OnBnClickedButton1();
private:
BOOL m_mode;
};
```

```
#include "stdafx.h"
#include "DemoAppDlg.h"
#include "afxdialogex.h"

CDemoAppDlg::CDemoAppDlg(CWnd* pParent /*=NULL*/)
: CAdjustableDialogEx(IDD_DEMOAPP_DIALOG, pParent)
: m_mode(FALSE)
{
}

void CDemoAppDlg::DoDataExchange(CDataExchange* pDX)
{
CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CDemoAppDlg, CAdjustableDialogEx)
ON_BN_CLICKED(IDC_BUTTON1, &CDemoAppDlg::OnBnClickedButton1)
END_MESSAGE_MAP()

void CDemoAppDlg::FillComplexComponentList(PVOID param)
{
BOOL mode(FALSE);
if (param)
{
mode = *(BOOL*)param;
}
if (mode)
{
__super::AddControl(IDC_EDIT1, EM_ALIGN_TOPLEFT, EM_RESIZE_FULL_WIDTH);
}
else
{
__super::AddControl(IDC_EDIT1, EM_ALIGN_TOPLEFT, EM_RESIZE_FULL_HEIGHT);
}

__super::AddControl(IDC_BUTTON1, EM_ALIGN_BOTTOM, EM_RESIZE_NONE);

}

BOOL CDemoAppDlg::OnInitDialog()
{
CAdjustableDialogEx::OnInitDialog();
__super::ResetLayout(&m_mode);
return TRUE;
}

void CDemoAppDlg::OnBnClickedButton1()
{
m_mode = !m_mode;
__super::ResetLayout(&m_mode);
}
```

详细的使用的例子请[参照我的Github](https://pewae.com/gaan/aHR0cHM6Ly9naXRodWIuY29tL2xpZmlzaGFrZS9DTUZDRHluYW1pY0xheW91dERlbW8=)。