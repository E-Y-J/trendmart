// COLOR PALETTE - from logo
// DARK_BLUE: #0a1f44
// emphasis: #135c8b
// SPLASH: #00aef0
// HIGHLIGHT: #9fcecb
// EGGSHELL_: #f3f3ea

export const colorPalette = {
  light: {
    contrast: '#0a1f44',
    emphasis: '#135c8b',
    splash: '#00aef0',
    highlight: '#9fcecb',
    bg: '#f3f3ea',
    text: '#fffffb',
  },
  dark: {
    contrast: '#f3f3ea',
    emphasis: '#9fcecb',
    splash: '#00aef0',
    highlight: '#0a1f44',
    bg: '#135c8b',
    text: '#00aef0',
  },
};

const baseBtn = {
  border: 'rem solid transparent',
  borderRadius: '.5rem',
  padding: '.3rem 0rem',
  cursor: 'pointer',
  fontWeight: 700,
};

const contrast = (mode) => ({
  background: colorPalette[mode].contrast,
  borderColor: colorPalette[mode].splash,
  color: colorPalette[mode].text,
});

const splash = (mode) => ({
  background: colorPalette[mode].splash,
  borderColor: colorPalette[mode].contrast,
  color: colorPalette[mode].contrast,
});

const muted = (mode) => ({
  background: colorPalette[mode].highlight,
  color: colorPalette[mode].contrast,
  borderColor: colorPalette[mode].splash,
});

const highlight = (mode) => ({
  background: colorPalette[mode].highlight,
  color: colorPalette[mode].contrast,
  borderColor: colorPalette[mode].splash,
});

const emphasis = (mode) => ({
  background: colorPalette[mode].emphasis,
  color: colorPalette[mode].text,
  borderColor: colorPalette[mode].splash,
});

const darkText = (mode) => ({
  background: colorPalette[mode].bg,
  color: colorPalette[mode].contrast,
  borderColor: colorPalette[mode].splash,
});

const lightText = (mode) => ({
  background: colorPalette[mode].bg,
  color: colorPalette[mode].text,
  borderColor: colorPalette[mode].splash,
});

export const buildTheme = (mode) => ({
  colors: colorPalette[mode],
  buttons: {
    contrast: { ...contrast(mode), ...baseBtn },
    splash: { ...splash(mode), ...baseBtn },
    muted: { ...muted(mode), ...baseBtn },
    highlight: { ...highlight(mode), ...baseBtn },
    emphasis: { ...emphasis(mode), ...baseBtn },
  },
  schemes: {
    contrast: contrast(mode),
    splash: splash(mode),
    muted: muted(mode),
    highlight: highlight(mode),
    emphasis: emphasis(mode),
    darkText: darkText(mode),
    lightText: lightText(mode),
  },
});
