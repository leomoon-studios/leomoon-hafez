#define AppName "LeoMoon Hafez"
#define AppExeName "LeoMoon Hafez.exe"
#define AppId "{{A084FE1D-8309-4828-8A26-8BAF48506327}"

#ifndef AppVersion
  #error AppVersion must be passed with /DAppVersion.
#endif
#ifndef StageDir
  #error StageDir must be passed with /DStageDir.
#endif
#ifndef OutputDir
  #error OutputDir must be passed with /DOutputDir.
#endif
#ifndef LicenseFile
  #error LicenseFile must be passed with /DLicenseFile.
#endif
#ifndef AppArchitecture
  #error AppArchitecture must be passed with /DAppArchitecture.
#endif

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher=LeoMoon Studios
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
LicenseFile={#LicenseFile}
OutputDir={#OutputDir}
OutputBaseFilename=leomoon-hafez-{#AppVersion}-windows-{#AppArchitecture}-setup
ArchitecturesAllowed={#AppArchitecture}
ArchitecturesInstallIn64BitMode={#AppArchitecture}
AppMutex=LeoMoonHafez
CloseApplications=yes
CloseApplicationsFilter={#AppExeName}
RestartApplications=no
Compression=lzma2/ultra64
SolidCompression=yes
UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#StageDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
