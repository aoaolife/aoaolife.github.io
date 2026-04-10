---
title: "如何让MFC的Dialog类型窗口在高度超出屏幕高度时出现比例合适的垂直滚动条 – aoao.life"
date: 2025-08-20 22:31:00
---

客户提了个需求：因为他们的显示器（32吋）大，所以经常把缩放比设成125%或者150%，希望我们的APP在这两个缩放比下能够正常显示。
但是我们干活用的只是普通的24吋，设成150%之后高度就出溢出屏幕了，这就需要加滚动条。而工作这个东西，到了二鬼子领导那里就会加码，变成100%-225%都得能正常运行，并且因为增加的高度与原来的高度相比没多太多，所以要大滑块，不要分的细碎的小滑块。
这个功能本身不难。通常的做法是取屏幕放大后的窗口新高度，然后减去桌面有效视窗高度，得到的差值除以一个系数，然后用SetScrollRange的第三个数给传进去。然后重写OnVScroll方法，从系数反推滑块位置。
但是，这样得到的是小滑块，而且最后一屏的空白部分也不准确，往往会出现大片空白。

研究了好几天，终于找到了还算不错的方案。在此分享一下。
注意，我只写了垂直滚动条，因为我们的窗体就是瘦长型，即使增加到225%也没超出屏幕宽。给公家干活的一个要务就是不干多余的事，所以要添加水平滚动条的自己酌情修改，我这里就不提供了。

开始。

## 第一步，在OnInitDialog()中，增加垂直滚动条

如需要增加则对垂直滚动条进行初始化。初始化时，不使用简化版的SetScrollRange()，而改用SetScrollInfo()。利用结构体SCROLLINFO的nPage和nMax配合实现大滑块。这里的逻辑是：nPage与nMax的比值也就是滑块占总高度的比值，比值越接近一，滑块越大。nPage和nMax都是相对值，只要二者单位统一即可。方便起见直接使用真实值。
一个很坑的点是nMax不能用窗口Rect的高，而要取最下边控件的下沿，原因未知。
下面是代码：

```
BOOL CMFCAppDemoDlg::OnInitDialog()
{
CDialogEx::OnInitDialog();

//取窗口位置
CRect rcThis;
GetWindowRect(&rcThis);

//取最下面控件的位置，如果有动态创建的控件，可以遍历取得。
CRect rcLastButton;
GetDlgItem(IDCANCEL)->GetWindowRect(rcLastButton);

//取放大倍数，96.0是100%时候的DPI
float fScale = static_cast<float>(GetDpiForWindow(m_hWnd)) / 96.0;

//取桌面工作区大小
CRect rcScreen;
::SystemParametersInfo(SPI_GETWORKAREA, 0, &rcScreen, 0);

//对话框的工作区域理想高度:比最后一个控件多一丢丢。
int nHeightImage = rcLastButton.bottom + rcLastButton.Height() * fScale;

//如果想象高度比工作区域高，那么将窗口高度设为与工作区等高。
if (nHeightImage > rcScreen.Height())
{
m_blHasVScrollBar = true; //成员变量，用于标记是否有滚动条
rcThis.bottom = rcThis.top + rcScreen.Height();
this->MoveWindow(&rcThis, TRUE); //修改Dialog自身高度
SCROLLINFO si{};
si.cbSize = sizeof SCROLLINFO;
si.fMask = SIF_RANGE | SIF_PAGE | SIF_PAGE;
si.nPage = rcScreen.Height(); //Windows桌面可利用高度作为Page高
si.nMax = nHeightImage; //窗口高度最大值。
SetScrollInfo(SB_VERT, &si, TRUE); //激活滚动条
}
//否则没用滚动条
else
{
SetScrollRange(SB_VERT, 0, 0, FALSE);
}

return TRUE;
}
```

## 第二步，重写WM_VSCROLL的消息响应函数OnVScroll()

没有难点。只要每个消息处理时，nPage与nMax的比例关系一致即可。

```
BEGIN_MESSAGE_MAP(CMFCAppDemoDlg, CDialogEx)
ON_WM_VSCROLL()
END_MESSAGE_MAP()

void CMFCAppDemoDlg::OnVScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar)
{
CDialogEx::OnVScroll(nSBCode, nPos, pScrollBar);
//取之前的滚动条信息
SCROLLINFO si{};
GetScrollInfo(SB_VERT, &si, SIF_ALL);

//滚动条上一次的位置
int nCurPos = si.nPos;
const int FACTOR(100);
switch (nSBCode)
{
case SB_LINEUP:          //Scroll one line up
nCurPos -= (si.nPage / 50); //点击一次箭头，或者按一次↑，移动页面的1/50，注意方向
break;
case SB_LINEDOWN:           //Scroll one line down
nCurPos += (si.nPage / 50); //注意方向
break;
case SB_PAGEUP:            //Scroll one page up
nCurPos -= (si.nPage / 50* 20); //PgUp键的处理。所有的响应要统一单位标准即可。注意方向
break;
case SB_PAGEDOWN:        //Scroll one page down
nCurPos += (si.nPage / 50* 20); //注意方向
break;
case SB_THUMBPOSITION:  //Scroll to the absolute position. The current position is provided in nPos
nCurPos = nPos; //从缩略图直接确认位置
break;
case SB_THUMBTRACK:     //Drag scroll box to specified position. The current position is provided in nPos
nCurPos = nPos; //从滚动条直接确认位置
break;
case SB_ENDSCROLL:
break;
default:
break;
}
//确认没有超出最小值和最大值范围。最小值一般是0，最大值是nMax - nPage。
nCurPos = max(si.nMin, min(nCurPos, si.nMax - static_cast<int>(si.nPage)));
//当位置移动时，滚动窗口内容
if (nCurPos != si.nPos)
{
int nDelta = si.nPos - nCurPos; //注意方向，原始值减目标值
si.nPos = nCurPos;
si.fMask = SIF_POS;
SetScrollInfo(SB_VERT, &si, TRUE); //设滚动条
ScrollWindow(0, nDelta); //滚动窗口
UpdateWindow();
}
}
```

## 第三步，重写WM_MOUSEWHEEL的消息响应函数OnMouseWheel()

同样没有难点，只是鼠标滚动一下会转化成多次向上或向下的消息。

```
BEGIN_MESSAGE_MAP(CMFCAppDemoDlg, CDialogEx)
ON_WM_MOUSEWHEEL()
END_MESSAGE_MAP()
BOOL CMFCAppDemoDlg::OnMouseWheel(UINT nFlags, short zDelta, CPoint pt)
{
//确认滚动条有效
if (!m_blHasVScrollBar) {
return CDialogEx::OnMouseWheel(nFlags, zDelta, pt);
}
CONST INT WHEEL_SCROLL_LINES(3);
UINT8 ucDirection(SB_LINEUP);
//根据zDelta方向确定消息重量
if (zDelta < 0) {
ucDirection = SB_LINEDOWN;
}
//把鼠标滚动值换算成N个箭头消息并发送。次数是没有方向的。
UINT unLines = (abs(zDelta) * WHEEL_SCROLL_LINES) / WHEEL_DELTA;
while (unLines--)
{
SendMessage(WM_VSCROLL, MAKEWPARAM(ucDirection, 0), 0);
}
return TRUE;
}
```

总之，最难的其实还是开头。nPage与nMax虽然设什么数都可以，但只有用真实值才是最符合拖动规律的。