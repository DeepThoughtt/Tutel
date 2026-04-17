#define Publisher "DeepThoughtt"
#define AppName "Tutel"
#define Exe "Tutel.exe"

[Setup]
AppName={#AppName}
AppVersion=0.1.0
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

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Files]
Source: "..\dist\Tutel.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Tutel"; Filename: "{app}\{#Exe}"
Name: "{commondesktop}\Tutel"; Filename: "{app}\{#Exe}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalOptions}"; Flags: unchecked

[CustomMessages]
english.CreateDesktopIcon=Create a desktop icon
italian.CreateDesktopIcon=Crea un'icona sul desktop
english.AdditionalOptions=Additional options:
italian.AdditionalOptions=Opzioni aggiuntive:
english.RunTutel=Run Tutel
italian.RunTutel=Avvia Tutel

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Run]
Filename: "{app}\{#Exe}"; Description: "{cm:RunTutel}"; Flags: nowait postinstall skipifsilent
