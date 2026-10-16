"""Hand gesture control application - entry point.

This file serves as the main entry point for backward compatibility.
The application has been refactored into separate modules:
- config.py: Configuration constants
- logic_core.py: Hand gesture recognition and control logic
- ui.py: User interface components
"""
from ui import main

if __name__ == "__main__":
    main()
