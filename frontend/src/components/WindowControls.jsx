/**
 * Window controls for the frameless window: minimize, maximize and close.
 * Rendered inside the TitleBar (see TitleBar.jsx); talks to the main
 * process through the preload API (contextIsolation is on).
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
        className="window-controls__btn window-controls__btn--maximize"
        aria-label="Maximize"
        onClick={() => window.electronAPI && window.electronAPI.maximizeWindow()}
      >
        {'\u229E'}
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
