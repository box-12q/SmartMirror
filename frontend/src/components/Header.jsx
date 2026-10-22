/**
 * Top header bar: menu icon + app title on the left; overflow menu and
 * window control buttons (minimize/close) on the right.
 * Loaded by index.html as a Babel-standalone script before App.jsx and
 * exposed on `window` (Babel standalone does not resolve ES module paths
 * when running from file:// inside Electron).
 *
 * Window buttons talk to the main process through the preload API
 * (contextIsolation is on, so no ipcRenderer in this file).
 */
function Header() {
  return (
    <header className="app__header">
      <div className="header__left">
        {/* Menu (hamburger) */}
        <button type="button" className="header__icon-btn" aria-label="Menu">
          {'\u2630'}
        </button>

        <span className="header__title">Gesture Control</span>
      </div>

      <div className="header__right">
        {/* Overflow menu (vertical ellipsis) */}
        <button type="button" className="header__icon-btn" aria-label="More options">
          {'\u22EE'}
        </button>

        {/* Window controls (frameless window: we handle them ourselves) */}
        <button
          type="button"
          className="header__win-btn"
          aria-label="Minimize"
          onClick={() => window.api && window.api.minimize()}
        >
          {'\u229F'}
        </button>
        <button
          type="button"
          className="header__win-btn"
          aria-label="Close"
          onClick={() => window.api && window.api.close()}
        >
          {'\u2715'}
        </button>
      </div>
    </header>
  );
}

window.Header = Header;
