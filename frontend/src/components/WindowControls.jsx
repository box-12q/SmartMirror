/**
 * Window controls for the frameless window: minimize, maximize and close.
 * Rendered inside the TitleBar (see TitleBar.jsx); talks to the main
 * process through the preload API (contextIsolation is on).
 *
 * Icons are inline SVG (thin 1.25px strokes, stroke="currentColor") so
 * they render crisp and pick up the idle/hover text colors from CSS —
 * no font-glyph artifacts, no per-button background boxes.
 */
function WindowControls() {
  return (
    <div className="window-controls">
      <button
        type="button"
        className="window-controls__btn window-controls__btn--minimize"
        aria-label="Minimize"
        onClick={() => window.electronAPI && window.electronAPI.minimizeWindow()}
      >
        {/* Minimize: a single thin horizontal line */}
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor"
             strokeWidth="1.25" strokeLinecap="round" aria-hidden="true">
          <line x1="4" y1="8" x2="12" y2="8" />
        </svg>
      </button>

      <button
        type="button"
        className="window-controls__btn window-controls__btn--maximize"
        aria-label="Maximize"
        onClick={() => window.electronAPI && window.electronAPI.maximizeWindow()}
      >
        {/* Maximize/restore: two overlapping squares (classic cascade icon) —
            full square in front, top+right edges of the square behind */}
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor"
             strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <rect x="3.5" y="5.5" width="7" height="7" rx="0.75" />
          <path d="M6 3.5 h6.5 v6.5" />
        </svg>
      </button>

      <button
        type="button"
        className="window-controls__btn window-controls__btn--close"
        aria-label="Close"
        onClick={() => window.electronAPI && window.electronAPI.closeWindow()}
      >
        {/* Close: a thin X */}
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor"
             strokeWidth="1.25" strokeLinecap="round" aria-hidden="true">
          <line x1="4.5" y1="4.5" x2="11.5" y2="11.5" />
          <line x1="11.5" y1="4.5" x2="4.5" y2="11.5" />
        </svg>
      </button>
    </div>
  );
}

window.WindowControls = WindowControls;
