/**
 * Card header inside the white workspace: title on the left, overflow
 * menu on the right. Window controls live in the TitleBar above.
 * Loaded by index.html as a Babel-standalone script before App.jsx and
 * exposed on `window` (Babel standalone does not resolve ES module paths
 * when running from file:// inside Electron).
 */
function Header() {
  return (
    <header className="app__header">
      <span className="header__title">Gesture Control</span>

      <div className="header__right">
        {/* Overflow menu (vertical ellipsis) */}
        <button type="button" className="header__icon-btn" aria-label="More options">
          {'\u22EE'}
        </button>
      </div>
    </header>
  );
}

window.Header = Header;
