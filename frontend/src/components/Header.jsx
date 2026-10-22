/**
 * Top header bar: menu icon + app title on the left, overflow menu on
 * the right. Loaded by index.html as a Babel-standalone script before
 * App.jsx and exposed on `window` (Babel standalone does not resolve ES
 * module paths when running from file:// inside Electron).
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

      {/* Overflow menu (vertical ellipsis) */}
      <button type="button" className="header__icon-btn" aria-label="More options">
        {'\u22EE'}
      </button>
    </header>
  );
}

window.Header = Header;
