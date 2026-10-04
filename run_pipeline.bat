@echo off

echo =====================================
echo CAPTCHA AI AUTOMATION PIPELINE
echo =====================================

echo.
echo [1/2] Running stress tests...
python stress_test.py

echo.
echo [2/2] Exporting data for Power BI...
python export_for_powerbi.py

echo.
echo =====================================
echo PIPELINE COMPLETE
echo =====================================

pause