/**
 * Custom title bar for the frameless window: app icon placeholder, the
 * active tab ("Home", mirrors the active sidebar item), and window
 * controls on the right.
 * Dragging the window is enabled via -webkit-app-region on .titlebar.
 * Loaded by index.html before App.jsx, exposed on `window`.
 */
function TitleBar() {
  return (
    <div className="titlebar">
      <div className="titlebar__left">
        {/* App icon placeholder: replace with an <img> from assets/icons */}
        <span className="titlebar__app-dot"></span>
        <span className="titlebar__tab">Home</span>
      </div>

      {/* Window controls live here, not floating over the frame */}
      <WindowControls />
    </div>
  );
}

window.TitleBar = TitleBar;
