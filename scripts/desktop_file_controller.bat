@echo off
title Desktop File and Folder Controller
color 0A
setlocal enabledelayedexpansion

:MENU
cls
echo ========================================
echo   DESKTOP FILE AND FOLDER CONTROLLER
echo ========================================
echo.
echo Current Desktop: %USERPROFILE%\Desktop
echo.
echo [1] Create New Folder
echo [2] Delete File or Folder
echo [3] Move File or Folder
echo [4] Copy File or Folder
echo [5] Rename File or Folder
echo [6] List All Files and Folders
echo [7] Organize Files by Type
echo [8] Clean Up Desktop (Move to Organized Folders)
echo [9] Search for File
echo [10] Create Multiple Folders
echo [11] Backup Desktop
echo [12] Delete Empty Folders
echo [13] Show Folder Size
echo [14] Lock Computer
echo [15] Shutdown Computer
echo [16] Restart Computer
echo [17] Switch User
echo [18] Sign Out
echo [0] Exit
echo.
set /p choice="Enter your choice (0-18): "

if "%choice%"=="1" goto CREATE_FOLDER
if "%choice%"=="2" goto DELETE
if "%choice%"=="3" goto MOVE
if "%choice%"=="4" goto COPY
if "%choice%"=="5" goto RENAME
if "%choice%"=="6" goto LIST
if "%choice%"=="7" goto ORGANIZE
if "%choice%"=="8" goto CLEANUP
if "%choice%"=="9" goto SEARCH
if "%choice%"=="10" goto CREATE_MULTIPLE
if "%choice%"=="11" goto BACKUP
if "%choice%"=="12" goto DELETE_EMPTY
if "%choice%"=="13" goto FOLDER_SIZE
if "%choice%"=="14" goto LOCK_COMPUTER
if "%choice%"=="15" goto SHUTDOWN_COMPUTER
if "%choice%"=="16" goto RESTART_COMPUTER
if "%choice%"=="17" goto SWITCH_USER
if "%choice%"=="18" goto SIGNOUT
if "%choice%"=="0" goto EXIT
goto MENU

:CREATE_FOLDER
cls
echo ========================================
echo         CREATE NEW FOLDER
echo ========================================
echo.
set /p foldername="Enter folder name: "
if exist "%USERPROFILE%\Desktop\%foldername%" (
    echo Folder already exists!
) else (
    mkdir "%USERPROFILE%\Desktop\%foldername%"
    echo Folder '%foldername%' created successfully!
)
pause
goto MENU

:DELETE
cls
echo ========================================
echo      DELETE FILE OR FOLDER
echo ========================================
echo.
set /p delname="Enter file or folder name to delete: "
if exist "%USERPROFILE%\Desktop\%delname%" (
    set /p confirm="Are you sure you want to delete '%delname%'? (Y/N): "
    if /i "!confirm!"=="Y" (
        if exist "%USERPROFILE%\Desktop\%delname%\*" (
            rmdir /s /q "%USERPROFILE%\Desktop\%delname%"
        ) else (
            del /q "%USERPROFILE%\Desktop\%delname%"
        )
        echo '%delname%' deleted successfully!
    ) else (
        echo Deletion cancelled.
    )
) else (
    echo File or folder not found!
)
pause
goto MENU

:MOVE
cls
echo ========================================
echo       MOVE FILE OR FOLDER
echo ========================================
echo.
set /p movesrc="Enter source name: "
set /p movedst="Enter destination folder: "
if exist "%USERPROFILE%\Desktop\%movesrc%" (
    if not exist "%USERPROFILE%\Desktop\%movedst%" (
        mkdir "%USERPROFILE%\Desktop\%movedst%"
    )
    move "%USERPROFILE%\Desktop\%movesrc%" "%USERPROFILE%\Desktop\%movedst%\"
    echo '%movesrc%' moved to '%movedst%' successfully!
) else (
    echo Source file or folder not found!
)
pause
goto MENU

:COPY
cls
echo ========================================
echo       COPY FILE OR FOLDER
echo ========================================
echo.
set /p copysrc="Enter source name: "
set /p copydst="Enter destination folder: "
if exist "%USERPROFILE%\Desktop\%copysrc%" (
    if not exist "%USERPROFILE%\Desktop\%copydst%" (
        mkdir "%USERPROFILE%\Desktop\%copydst%"
    )
    if exist "%USERPROFILE%\Desktop\%copysrc%\*" (
        xcopy /E /I /Y "%USERPROFILE%\Desktop\%copysrc%" "%USERPROFILE%\Desktop\%copydst%\%copysrc%"
    ) else (
        copy "%USERPROFILE%\Desktop\%copysrc%" "%USERPROFILE%\Desktop\%copydst%\"
    )
    echo '%copysrc%' copied to '%copydst%' successfully!
) else (
    echo Source file or folder not found!
)
pause
goto MENU

:RENAME
cls
echo ========================================
echo       RENAME FILE OR FOLDER
echo ========================================
echo.
set /p oldname="Enter current name: "
set /p newname="Enter new name: "
if exist "%USERPROFILE%\Desktop\%oldname%" (
    ren "%USERPROFILE%\Desktop\%oldname%" "%newname%"
    echo Renamed '%oldname%' to '%newname%' successfully!
) else (
    echo File or folder not found!
)
pause
goto MENU

:LIST
cls
echo ========================================
echo     LIST ALL FILES AND FOLDERS
echo ========================================
echo.
echo Contents of Desktop:
echo.
dir "%USERPROFILE%\Desktop" /b
echo.
pause
goto MENU

:ORGANIZE
cls
echo ========================================
echo      ORGANIZE FILES BY TYPE
echo ========================================
echo.
echo Creating organization folders...

set desktop=%USERPROFILE%\Desktop

if not exist "%desktop%\Documents" mkdir "%desktop%\Documents"
if not exist "%desktop%\Images" mkdir "%desktop%\Images"
if not exist "%desktop%\Videos" mkdir "%desktop%\Videos"
if not exist "%desktop%\Music" mkdir "%desktop%\Music"
if not exist "%desktop%\Archives" mkdir "%desktop%\Archives"
if not exist "%desktop%\Programs" mkdir "%desktop%\Programs"
if not exist "%desktop%\Others" mkdir "%desktop%\Others"

echo Moving files...

move "%desktop%\*.txt" "%desktop%\Documents\" 2>nul
move "%desktop%\*.doc" "%desktop%\Documents\" 2>nul
move "%desktop%\*.docx" "%desktop%\Documents\" 2>nul
move "%desktop%\*.pdf" "%desktop%\Documents\" 2>nul
move "%desktop%\*.xls" "%desktop%\Documents\" 2>nul
move "%desktop%\*.xlsx" "%desktop%\Documents\" 2>nul
move "%desktop%\*.ppt" "%desktop%\Documents\" 2>nul
move "%desktop%\*.pptx" "%desktop%\Documents\" 2>nul

move "%desktop%\*.jpg" "%desktop%\Images\" 2>nul
move "%desktop%\*.jpeg" "%desktop%\Images\" 2>nul
move "%desktop%\*.png" "%desktop%\Images\" 2>nul
move "%desktop%\*.gif" "%desktop%\Images\" 2>nul
move "%desktop%\*.bmp" "%desktop%\Images\" 2>nul
move "%desktop%\*.svg" "%desktop%\Images\" 2>nul

move "%desktop%\*.mp4" "%desktop%\Videos\" 2>nul
move "%desktop%\*.avi" "%desktop%\Videos\" 2>nul
move "%desktop%\*.mkv" "%desktop%\Videos\" 2>nul
move "%desktop%\*.mov" "%desktop%\Videos\" 2>nul

move "%desktop%\*.mp3" "%desktop%\Music\" 2>nul
move "%desktop%\*.wav" "%desktop%\Music\" 2>nul
move "%desktop%\*.flac" "%desktop%\Music\" 2>nul

move "%desktop%\*.zip" "%desktop%\Archives\" 2>nul
move "%desktop%\*.rar" "%desktop%\Archives\" 2>nul
move "%desktop%\*.7z" "%desktop%\Archives\" 2>nul

move "%desktop%\*.exe" "%desktop%\Programs\" 2>nul
move "%desktop%\*.msi" "%desktop%\Programs\" 2>nul

echo Desktop organized successfully!
pause
goto MENU

:CLEANUP
cls
echo ========================================
echo         CLEAN UP DESKTOP
echo ========================================
echo.
echo This will organize all files into categorized folders.
set /p confirm="Continue? (Y/N): "
if /i "!confirm!"=="Y" (
    goto ORGANIZE
) else (
    goto MENU
)

:SEARCH
cls
echo ========================================
echo          SEARCH FOR FILE
echo ========================================
echo.
set /p searchname="Enter filename to search: "
echo.
echo Searching for '%searchname%' on Desktop...
echo.
dir "%USERPROFILE%\Desktop\*%searchname%*" /s /b 2>nul
if errorlevel 1 (
    echo No files found matching '%searchname%'
)
echo.
pause
goto MENU

:CREATE_MULTIPLE
cls
echo ========================================
echo      CREATE MULTIPLE FOLDERS
echo ========================================
echo.
echo Enter folder names separated by spaces:
set /p folderlist="Folders: "
for %%f in (%folderlist%) do (
    if not exist "%USERPROFILE%\Desktop\%%f" (
        mkdir "%USERPROFILE%\Desktop\%%f"
        echo Created: %%f
    ) else (
        echo Already exists: %%f
    )
)
echo.
echo Done!
pause
goto MENU

:BACKUP
cls
echo ========================================
echo         BACKUP DESKTOP
echo ========================================
echo.
set backupname=Desktop_Backup_%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set backupname=%backupname: =0%
echo Creating backup folder: %backupname%
echo.
xcopy /E /I /Y "%USERPROFILE%\Desktop" "%USERPROFILE%\Desktop\%backupname%"
echo.
echo Backup created successfully in: %backupname%
pause
goto MENU

:DELETE_EMPTY
cls
echo ========================================
echo       DELETE EMPTY FOLDERS
echo ========================================
echo.
echo Searching for empty folders on Desktop...
for /f "delims=" %%d in ('dir "%USERPROFILE%\Desktop" /ad /b /s ^| sort /r') do (
    dir "%%d" 2>nul | find "File(s)" >nul && (
        rd "%%d" 2>nul && echo Deleted: %%d
    )
)
echo.
echo Done!
pause
goto MENU

:FOLDER_SIZE
cls
echo ========================================
echo         SHOW FOLDER SIZE
echo ========================================
echo.
set /p foldername="Enter folder name: "
if exist "%USERPROFILE%\Desktop\%foldername%" (
    echo.
    echo Calculating size of '%foldername%'...
    echo.
    dir "%USERPROFILE%\Desktop\%foldername%" /s
) else (
    echo Folder not found!
)
echo.
pause
goto MENU

:LOCK_COMPUTER
cls
echo ========================================
echo         LOCK COMPUTER
echo ========================================
echo.
set /p confirm="Are you sure you want to lock your computer? (Y/N): "
if /i "!confirm!"=="Y" (
    echo Locking computer...
    rundll32.exe user32.dll,LockWorkStation
) else (
    echo Lock cancelled.
    pause
    goto MENU
)

:SHUTDOWN_COMPUTER
cls
echo ========================================
echo       SHUTDOWN COMPUTER
echo ========================================
echo.
echo WARNING: This will shut down your computer!
echo.
echo [1] Shutdown Immediately
echo [2] Shutdown in 1 minute
echo [3] Shutdown in 5 minutes
echo [4] Shutdown in 10 minutes
echo [5] Cancel Shutdown
echo [0] Back to Menu
echo.
set /p shutdownchoice="Enter your choice (0-5): "

if "%shutdownchoice%"=="1" (
    echo Shutting down NOW...
    shutdown /s /t 0
)
if "%shutdownchoice%"=="2" (
    echo Computer will shutdown in 1 minute...
    shutdown /s /t 60
    echo To cancel, run: shutdown /a
    pause
    goto MENU
)
if "%shutdownchoice%"=="3" (
    echo Computer will shutdown in 5 minutes...
    shutdown /s /t 300
    echo To cancel, run: shutdown /a
    pause
    goto MENU
)
if "%shutdownchoice%"=="4" (
    echo Computer will shutdown in 10 minutes...
    shutdown /s /t 600
    echo To cancel, run: shutdown /a
    pause
    goto MENU
)
if "%shutdownchoice%"=="5" (
    echo Cancelling any scheduled shutdown...
    shutdown /a
    echo.
    pause
    goto MENU
)
if "%shutdownchoice%"=="0" goto MENU
goto SHUTDOWN_COMPUTER

:RESTART_COMPUTER
cls
echo ========================================
echo       RESTART COMPUTER
echo ========================================
echo.
echo WARNING: This will restart your computer!
echo.
echo [1] Restart Immediately
echo [2] Restart in 1 minute
echo [3] Restart in 5 minutes
echo [4] Restart in 10 minutes
echo [5] Cancel Restart
echo [0] Back to Menu
echo.
set /p restartchoice="Enter your choice (0-5): "

if "%restartchoice%"=="1" (
    echo Restarting NOW...
    shutdown /r /t 0
)
if "%restartchoice%"=="2" (
    echo Computer will restart in 1 minute...
    shutdown /r /t 60
    echo To cancel, run: shutdown /a
    pause
    goto MENU
)
if "%restartchoice%"=="3" (
    echo Computer will restart in 5 minutes...
    shutdown /r /t 300
    echo To cancel, run: shutdown /a
    pause
    goto MENU
)
if "%restartchoice%"=="4" (
    echo Computer will restart in 10 minutes...
    shutdown /r /t 600
    echo To cancel, run: shutdown /a
    pause
    goto MENU
)
if "%restartchoice%"=="5" (
    echo Cancelling any scheduled restart...
    shutdown /a
    echo.
    pause
    goto MENU
)
if "%restartchoice%"=="0" goto MENU
goto RESTART_COMPUTER

:SWITCH_USER
cls
echo ========================================
echo         SWITCH USER
echo ========================================
echo.
set /p confirm="Are you sure you want to switch user? (Y/N): "
if /i "!confirm!"=="Y" (
    echo Switching user...
    rundll32.exe user32.dll,LockWorkStation
    echo.
    echo Note: After lock screen appears, you can click "Switch User"
    pause
) else (
    echo Switch user cancelled.
    pause
    goto MENU
)

:SIGNOUT
cls
echo ========================================
echo          SIGN OUT
echo ========================================
echo.
set /p confirm="Are you sure you want to sign out? (Y/N): "
if /i "!confirm!"=="Y" (
    echo Signing out...
    shutdown /l
) else (
    echo Sign out cancelled.
    pause
    goto MENU
)

:EXIT
cls
echo Thank you for using Desktop File and Folder Controller!
timeout /t 2 >nul
exit
