/**
 * Main application component: base three-part layout.
 *
 * Sidebar (left) + main column (right). The main column contains the
 * header (top) and the content area (fills the rest) with the camera
 * preview placeholder inside.
 *
 * Sidebar, Header and VideoPlayer live in src/components/.
 * No ES module imports: Babel standalone transpiles JSX in the browser
 * but does not resolve module paths, so components are attached to
 * `window` by their files and referenced globally.
 */
function App() {
  return (
    <div className="app">
      <Sidebar />

      <div className="app__main">
        <Header />
        <main className="app__content">
          <VideoPlayer />
        </main>
      </div>
    </div>
  );
}

window.App = App;
