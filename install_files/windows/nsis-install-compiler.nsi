# Script to create an NSIS exe to install EcoAssist on Windows
# Peter van Lunteren, last edit on 6 Jan 2025
# Var VERSION will be defined by github actions by adding a line above like '!define VERSION "v6.34"'

# Name and output location for the installer
Outfile "EcoAssist-${VERSION}-windows.exe"

# Define variables
Var archiveUrl
Var archiveName

# Include NSIS MUI for a modern interface
!include MUI2.nsh
!include Sections.nsh

# Set execution level
RequestExecutionLevel user

# UI Pages
Name "EcoAssist ${VERSION}"
!define MUI_PAGE_HEADER_TEXT "Step 1 of 3"
!define MUI_PAGE_HEADER_SUBTEXT "Uninstalling previous EcoAssist version..."
!define MUI_FINISHPAGE_TITLE "Installation Complete!"
!define MUI_FINISHPAGE_TEXT "EcoAssist has been successfully installed. A shortcut has been created on your desktop.$\r$\n$\r$\n'$DESKTOP\EcoAssist'"
!define MUI_FINISHPAGE_RUN "$INSTDIR\EcoAssist ${VERSION}.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Open EcoAssist application directly after clicking 'Finish'"
!define MUI_FINISHPAGE_LINK "Read more on the EcoAssist website"
!define MUI_FINISHPAGE_LINK_LOCATION "https://addaxdatascience.com/ecoassist/"
!define MUI_ICON "logo.ico"
!define MUI_UNICON "logo.ico"
!define MUI_WELCOMEPAGE_TITLE "EcoAssist ${VERSION} installer"
!define MUI_WELCOMEPAGE_TEXT "This install consists of three steps:$\r$\n$\r$\n   1 - Uninstall current EcoAssist version if present$\r$\n   2 - Download EcoAssist version ${VERSION}$\r$\n   3 - Extract and clean up files"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

# Section for installation steps
Section "Install"

    # Set fixed installation directory without prompting the user
    StrCpy $INSTDIR "$PROFILE\EcoAssist"

    # Hide progress bar
    Push "false"
    Call ShowProgressBar

    # Step 1: Remove old files and directory if they exist
    DetailPrint "Removing previous files... "
    SetOutPath $INSTDIR

    SetDetailsPrint none
    DetailPrint "Deleting files... 0%"
    RMDir /r $INSTDIR/cameratraps
    DetailPrint "Deleting files... 10%"
    RMDir /r $INSTDIR/EcoAssist
    DetailPrint "Deleting files... 20%"
    RMDir /r $INSTDIR/envs
    DetailPrint "Deleting files... 30%"
    RMDir /r $INSTDIR/Human-in-the-loop
    DetailPrint "Deleting files... 40%"
    RMDir /r $INSTDIR/models
    DetailPrint "Deleting files... 50%"
    RMDir /r $INSTDIR/visualise_detection
    DetailPrint "Deleting files... 60%"
    RMDir /r $INSTDIR/yolov5_versions
    DetailPrint "Deleting files... 70%"
    RMDir /r $INSTDIR
    DetailPrint "Deleting files... 100%"
    SetDetailsPrint both

    # remove dir all together
    RMDir $INSTDIR

    # add dir 
    CreateDirectory "$INSTDIR"

    # adjust header
    !insertmacro MUI_HEADER_TEXT "Step 2 of 3" "Downloading EcoAssist version ${VERSION}..."

    # Download the 7z archive
    DetailPrint "Downloading files..."
    StrCpy $archiveUrl "https://storage.googleapis.com/github-release-files-storage/${VERSION}/windows-${VERSION}.7z"
    StrCpy $archiveName "$INSTDIR\windows-${VERSION}.7z"
    NSISdl::download $archiveUrl $archiveName
    # inetc::get $archiveUrl $archiveName
    Pop $0

    # Check if download was successful
    IntCmp $0 0 downloadSuccess downloadFail
    downloadSuccess:
        DetailPrint "Downloaded archive successfully."
        Goto downloadDone
    downloadFail:
        DetailPrint "Failed to download archive. Exiting."
        Abort
    downloadDone:

    # Show progress bar
    Push "true"
    Call ShowProgressBar

    # adjust header
    !insertmacro MUI_HEADER_TEXT "Step 3 of 3" "Extracting files..."

    # Extract the 7z archrive
    Nsis7z::ExtractWithDetails "$INSTDIR\windows-${VERSION}.7z" "Extracting files... %s"

    # clean up temporary files
    Delete "$INSTDIR\windows-${VERSION}.7z"

    # Installation completed successfully
    DetailPrint "Installation completed successfully."

    # Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstaller.exe"

    ; Create a shortcut on the desktop
    CreateShortcut "$DESKTOP\EcoAssist.lnk" "$INSTDIR\EcoAssist ${VERSION}.exe" "" "$INSTDIR\EcoAssist\logo.ico" 0 SW_SHOWNORMAL

    ; Notify user
    DetailPrint "Shortcut created on the desktop."

SectionEnd

# Uninstaller section (optional)
Section "Uninstall"

    # Set fixed installation directory without prompting the user
    StrCpy $INSTDIR "$PROFILE\EcoAssist" 

    # Remove installed files and directories during uninstallation
    DetailPrint "Uninstalling..."
    RMDir /r $INSTDIR
    DetailPrint "Uninstallation complete."

SectionEnd

Function ShowProgressBar
    Exch $0
    FindWindow $1 "#32770" "" $HWNDPARENT
    GetDlgItem $2 $1 1004 ; The control ID for the progress bar is typically 1004
    IntCmp $2 0 skip

    StrCmp $0 "true" show hide

    show:
        ShowWindow $2 1
        Return

    hide:
        ShowWindow $2 0
        Return

    skip:
        MessageBox MB_OK "Progress bar control not found."
FunctionEnd
