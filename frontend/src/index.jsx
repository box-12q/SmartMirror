/**
 * React entry point.
 * `React` and `ReactDOM` come from the UMD builds loaded in index.html,
 * and `App` is attached to `window` by App.jsx before this file runs.
 */
const container = document.getElementById('root');
ReactDOM.createRoot(container).render(<App />);
