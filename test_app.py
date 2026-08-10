from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=120)
at.run()

print("errores:", at.exception)
assert not at.exception, f"La app falló: {at.exception}"

tabs = at.tabs
print("pestañas:", [t.label for t in tabs] if hasattr(tabs, "__iter__") else len(tabs))
for tab in tabs:
    tab.run()
    print(f"[{tab.label}] errores: {len(tab.exception)}")
    assert not tab.exception, f"Pestaña {tab.label} falló: {tab.exception}"

print("APPTEST_OK")
