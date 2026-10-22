/**
 * Window controls for the frameless window: minimize and close,
 * pinned over the top-right corner of the outer frame.
 *
 * Rendered by App inside .window-frame (position: absolute anchors to
 * the frame). Talks to the main process through the preload API
 * (contextIsolation is on, so no ipcRenderer in renderer files).
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
        {'\u229F'}
      </button>

      <button
        type="button"
        className="window-controls__btn window-controls__btn--close"
        aria-label="Close"
        onClick={() => window.electronAPI && window.electronAPI.closeWindow()}
      >
        {'\u2715'}
      </button>
    </div>
  );
}

window.WindowControls = WindowControls;
