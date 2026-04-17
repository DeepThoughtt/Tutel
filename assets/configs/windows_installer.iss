#define Publisher "DeepThoughtt"
#define AppName "Tutel"
#define Exe "Tutel.exe"
#define Version GetFileVersion("..\dist\Tutel.exe")

[Setup]
AppName={#AppName}
AppVersion={#Version}
AppPublisher={#Publisher}
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}

OutputDir=output
OutputBaseFilename=TutelInstaller
SetupIconFile=..\assets\icons\tutel.ico
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
LanguageDetectionMethod=locale
DefaultLanguage=english

[Languages]
Name: "english"
Name: "italian"

[Files]
Source: "..\dist\Tutel.exe"

[Icons]
Name: "{group}\Tutel"
Name: "{commondesktop}\Tutel"

[Tasks]
Name: "desktopicon"

[UninstallDelete]
Type: filesandordirs

[Run]
Filename: "{app}\{#Exe}"
