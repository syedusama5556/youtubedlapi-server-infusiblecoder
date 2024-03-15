@echo off
rmdir /s /q "dist"
pip uninstall youtubedlapi_server_infusiblecoder -y
python setup.py sdist bdist_wheel
cd dist
for %%f in (youtubedlapi_server_infusiblecoder-*.whl) do (
    pip install "%%f[cli]" -U
)
@REM youtubedlapi-server-infusiblecoder -p 9191 --host 0.0.0.0 --number-processes 1
uvicorn youtubedlapi_server_infusiblecoder.app:app_asgi --host 0.0.0.0 --port 9191 --workers 1 --log-level info
pause
