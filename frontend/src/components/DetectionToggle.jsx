/**
 * Hand-detection on/off switch rendered in the bottom-right corner of
 * the camera preview. Uses useState (React global from the UMD build —
 * Babel standalone does not process ES module imports).
 *
 * For now the state only drives styling; wiring it to the Python
 * detection pipeline will go through the preload API later.
 */
const { useState } = React;

function DetectionToggle() {
  const [enabled, setEnabled] = useState(true);

  return (
    <div className="detection-toggle">
      {/* Eye — detection on */}
      <button
        type="button"
        className={
          'detection-toggle__btn ' + (enabled ? 'detection-toggle__btn--active' : 'detection-toggle__btn--idle')
        }
        aria-label="Enable hand detection"
        aria-pressed={enabled}
        onClick={() => setEnabled(true)}
      >
        {'\u{1F441}\uFE0E'}
      </button>

      {/* Crossed circle — detection off */}
      <button
        type="button"
        className={
          'detection-toggle__btn ' + (!enabled ? 'detection-toggle__btn--active' : 'detection-toggle__btn--idle')
        }
        aria-label="Disable hand detection"
        aria-pressed={!enabled}
        onClick={() => setEnabled(false)}
      >
        {'\u{1F6AB}\uFE0E'}
      </button>
    </div>
  );
}

window.DetectionToggle = DetectionToggle;
