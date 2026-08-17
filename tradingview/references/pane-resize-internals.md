# TradingView Pane Resize — Internals & Debug Path

Verified 08/01/26 on TradingView Desktop (port 42719). Standard indicator pane height: **80px**.

## Why synthetic drags fail

Dispatching `PointerEvent` / `MouseEvent` sequences on the pane handle (`.handle-pCRReYxp` or `div[class*=handle]`) does NOTHING. TradingView's drag machinery ignores untrusted (synthetic) events — the pane never moves. Two attempts failed this way (pointer events, then mouse events with movement tracking).

## What works: call the separator's internal handlers

`window.TradingViewApi._activeChartWidgetWV.value()._chartWidget._paneSeparators[N]` exposes the real drag handlers:

- `_mouseDownOrTouchStartEvent({pageY: Y})` — initializes `_resizeInfo` (startY, prevStretchTopPane, maxPaneStretch, totalStretch, pixelStretchFactor, minPaneStretch)
- `_pressedMouseOrTouchMoveEvent({pageY: Y + delta})` — clamps new stretch for top/bottom panes, calls `fullUpdate()`
- `_mouseUpOrTouchEndEvent({pageY: Y + delta})` — records undo command, clears `_resizeInfo`

The move handler math: `r = (e.pageY - startY) * pixelStretchFactor`, then `topStretch = clamp(prevTopStretch + r, minPaneStretch, maxPaneStretch)`, `bottomStretch = totalStretch - topStretch`.

## Key facts

- `startY` can be 0 — only the DELTA matters (`endY - startY` = pixels).
- Moving the separator DOWN shrinks the pane BELOW it (positive delta).
- Total chart height is fixed: shrinking one pane grows the pane ABOVE it. With 3+ panes, resize **bottom-up** (highest pane index first), then normalize each pane to 80px in sequence.
- `_resizeInfo` is null when not mid-drag — Step 1 must read separator element positions via `getBoundingClientRect()`, NOT `_resizeInfo.startY` (always null at rest).
- Pane heights are read from `.chart-markup-table.pane` elements.

## Full working expression (resize pane N+1 to 80px via separator N)

```js
(() => {
  const wv = window.TradingViewApi._activeChartWidgetWV.value();
  const cw = wv._chartWidget;
  const seps = cw._paneSeparators;
  const sep = seps[N];
  const tables = [...document.querySelectorAll('.chart-markup-table.pane')];
  const target = tables[N + 1].getBoundingClientRect();
  const delta = Math.round(target.height) - 80;
  if (delta === 0) return 'already 80px';
  const startY = 0;
  sep._mouseDownOrTouchStartEvent({pageY: startY});
  sep._pressedMouseOrTouchMoveEvent({pageY: startY + delta});
  sep._mouseUpOrTouchEndEvent({pageY: startY + delta});
  return 'resized by ' + delta + 'px';
})()
```

## Verified deltas (08/01/26)

- 95px delta: 193px pane → 98px
- 113px delta: 196px pane → 83px (with 3px rounding, then normalized to 80px)
- Two sequential separator drags: both indicator panes to exactly 80px
