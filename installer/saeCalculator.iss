; Installer for the SAE Fractional Calculator. Built with Inno Setup 6:
;
;     ISCC.exe installer\saeCalculator.iss
;
; It expects dist\saeCalculator\ to exist - the folder bundle, not the
; one-file exe. tools\buildInstaller.py builds that and passes the version in
; from appConfig, so the installer, the About box and the wheel cannot
; disagree about what this is; the default below is only what a bare ISCC run
; would use.
;
; Per-user by design. A calculator needs nothing machine-wide: it writes only
; its theme and donation flag to HKCU, and asking for administrator rights to
; install a calculator is how a small tool becomes a thing IT has to approve.

#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

#define AppName "SAE Fractional Calculator"
#define ShortName "SAE Calculator"
#define Publisher "Charette AI Group, LLC"
#define AppUrl "https://saecalculator.com"
#define RepoUrl "https://github.com/Charette-AI-Group/saeCalculator"
#define ExeName "saeCalculator.exe"
#define BundleDir "..\dist\saeCalculator"

[Setup]
; Fixed for the life of the application: this is what lets an upgrade replace
; an install rather than sit beside it, and what the uninstaller is found by.
AppId={{9A75578F-9E4D-4EF9-A017-1AF72D92ABE4}
AppName={#AppName}
AppVersion={#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher={#Publisher}
AppPublisherURL={#AppUrl}
AppSupportURL={#RepoUrl}
AppUpdatesURL={#RepoUrl}/releases
DefaultDirName={autopf}\{#ShortName}
DefaultGroupName={#ShortName}
DisableProgramGroupPage=yes
SetupIconFile=..\src\saeCalculator\resources\icon.ico
UninstallDisplayIcon={app}\{#ExeName}
UninstallDisplayName={#AppName}
OutputDir=..\dist
OutputBaseFilename=saeCalculatorSetup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
; Per-user, so there is no UAC prompt and no Program Files. The application
; writes only to HKCU, so nothing here needs more than the user has.
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; Shown on the first page, so the licence is read before anything is written.
LicenseFile=..\LICENSE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
Source: "{#BundleDir}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\{#ShortName}"; Filename: "{app}\{#ExeName}"
Name: "{group}\Uninstall {#ShortName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#ShortName}"; Filename: "{app}\{#ExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#ExeName}"; Description: "Start {#ShortName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; The bundle only. Deliberately not the settings under HKCU: an uninstall that
; silently discards somebody's theme choice - and the flag that remembers they
; already donated - is a surprise, and a reinstall is the commonest reason to
; uninstall.
Type: filesandordirs; Name: "{app}\_internal"

[Code]
{ A running copy holds its own files open, so replacing them mid-upgrade
  fails with a message about a file in use that says nothing about why. Ask
  first instead, in words that name the application. The main window's title
  is exactly the application name (appConfig.windowTitle).

  SuppressibleMsgBox, not MsgBox: a plain MsgBox still appears under
  /SUPPRESSMSGBOXES and would hang a silent install. Silently, the answer is
  No - abort cleanly rather than fail halfway on a file in use. }
function InitializeSetup(): Boolean;
var
  WindowHandle: HWND;
begin
  Result := True;
  WindowHandle := FindWindowByWindowName('{#AppName}');
  if WindowHandle <> 0 then
    Result := SuppressibleMsgBox(
      '{#ShortName} appears to be running.' + #13#10#13#10 +
      'Close it before continuing, or setup cannot replace its files.' + #13#10#13#10 +
      'Continue anyway?',
      mbConfirmation, MB_YESNO, IDNO) = IDYES;
end;
