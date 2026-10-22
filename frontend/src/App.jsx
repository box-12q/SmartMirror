/**
 * Main application layout: title bar + sidebar + white workspace card.
 *
 * window-frame  — decorative outer border (app runs frameless)
 * titlebar      — app icon / active tab / window controls (draggable)
 * app-content   — floating cards on the darker backdrop:
 *                   sidebar card + workspace card
 * main-area     — white card with the header and the lavender content
 *
 * Components live in src/components/ and are exposed on `window`
 * (Babel standalone does not resolve ES module paths).
 */
function App() {
  return (
    <div className="window-frame">
      <TitleBar />

      <div className="app-content">
        <Sidebar />

        <div className="main-area">
          <Header />
          <div className="content">
            <VideoPlayer />
          </div>
        </div>
      </div>
    </div>
  );
}

window.App = App;
