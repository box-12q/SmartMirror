/**
 * Placeholder main component.
 * We do not use ES module `export` here even though this looks like a
 * modern file: Babel standalone (loaded via CDN in index.html) transpiles
 * JSX in the browser but does not resolve module paths, so `import` /
 * `export` would fail at runtime when loaded via file:// inside Electron.
 * Instead, the component is exposed on `window` and referenced globally.
 */
function App() {
  return (
    <div className="app">
      <p className="app__title">Gesture Control App</p>
    </div>
  );
}

window.App = App;
