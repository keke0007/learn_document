@echo off

echo === 执行 git add . ===
git add .

echo === 执行 git commit ===
git commit -m "add something"

echo === 执行 git push ===
git push origin master

echo === 操作完成 ===
pause
