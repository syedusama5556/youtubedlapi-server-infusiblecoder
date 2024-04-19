@echo off
rmdir /s /q "dist"
pip uninstall youtubedlapi_server_infusiblecoder -y
python setup.py sdist bdist_wheel
cd dist
for %%f in (youtubedlapi_server_infusiblecoder-*.whl) do (
    pip install "%%f[cli]" -U
)

REM Start Uvicorn server
start "Uvicorn Server" cmd /k uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191 --workers 1 --log-level info

@REM REM Start Celery worker
@REM start "Celery Worker" cmd /k celery -A youtubedlapi_server_infusiblecoder.app.mycele worker --loglevel=info

pause
