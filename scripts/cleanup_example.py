from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
SC=ROOT/"scaffold"
PKG=ROOT/"src"/"cisc217_final_game"
if PKG.exists(): shutil.rmtree(PKG)
shutil.copytree(SC/"src"/"cisc217_final_game",PKG)
TESTS=ROOT/"tests"
for p in TESTS.glob("test_*.py"): p.unlink()
shutil.copy2(SC/"tests"/"conftest.py",TESTS/"conftest.py")
marker=ROOT/"PROVIDED_EXAMPLE_CODE_PRESENT.txt"
if marker.exists(): marker.unlink()
for db in (PKG/"data").glob("*.db") if (PKG/"data").exists() else []: db.unlink()
print("Instructor Character Adventure example removed.")
print("Student scaffold installed. Add your own tests under tests/.")
