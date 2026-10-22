/**
 * Main application component: decorative window frame + three-part layout.
 *
 * window-frame  — outer decorative border (the app runs frameless, so we
 *                 draw our own window edge)
 * app-content   — sidebar + main column
 * main-area     — header (top) + content (rest) with the camera preview
 *
 * Sidebar, Header, VideoPlayer and WindowControls live in src/components/.
 * No ES module imports: Babel standalone transpiles JSX in the browser
 * but does not resolve module paths, so components are attached to
 * `window` by their files and referenced globally.
 */
function App() {
  return (
    <div className="window-frame">
      <div className="app-content">
        <Sidebar />

        <div className="main-area">
          <Header />
          <div className="content">
            <VideoPlayer />
          </div>
        </div>
      </div>

      {/* Minimize/close, pinned over the frame's top-right corner */}
      <WindowControls />
    </div>
  );
}

window.App = App;
