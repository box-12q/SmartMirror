/**
 * Main application component: base three-part layout.
 *
 * Sidebar (left) + main column (right). The main column contains the
 * header (top) and the content area (fills the rest).
 *
 * No ES module imports here: Babel standalone transpiles JSX in the
 * browser but does not resolve module paths, so the component is
 * attached to `window` and referenced globally from index.jsx.
 */
function App() {
  return (
    <div className="app">
      <aside className="app__sidebar"></aside>

      <div className="app__main">
        <header className="app__header"></header>
        <main className="app__content"></main>
      </div>
    </div>
  );
}

window.App = App;
