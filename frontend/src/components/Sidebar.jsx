/**
 * Sidebar navigation component.
 * Loaded by index.html as a Babel-standalone script BEFORE App.jsx and
 * exposed on `window` (Babel standalone does not resolve ES module paths
 * when running from file:// inside Electron).
 */
function Sidebar() {
  return (
    <aside className="app__sidebar">
      <nav className="sidebar__nav">
        {/* Home — active item */}
        <button type="button" className="sidebar__item sidebar__item--active">
          {/* \uFE0E forces monochrome (text) presentation of the emoji,
              so the icon can be tinted with CSS like the other glyphs */}
          <span className="sidebar__icon">{'\u{1F3E0}\uFE0E'}</span>
          <span className="sidebar__label">Home</span>
        </button>

        {/* Settings */}
        <button type="button" className="sidebar__item">
          <span className="sidebar__icon">{'\u2699\uFE0E'}</span>
          <span className="sidebar__label">Settings</span>
        </button>

        {/* Restart */}
        <button type="button" className="sidebar__item">
          <span className="sidebar__icon">{'\u21BB'}</span>
          <span className="sidebar__label">Restart</span>
        </button>
      </nav>
    </aside>
  );
}

window.Sidebar = Sidebar;
