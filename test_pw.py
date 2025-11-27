try:
    from playwright.async_api import async_playwright
    print("Playwright imported successfully!")
except ImportError as e:
    print(f"Import failed: {e}")
    import sys
    print(f"Python executable: {sys.executable}")
    print(f"Sys path: {sys.path}")
