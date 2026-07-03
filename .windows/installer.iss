#define Publisher "DeepThoughtt"
#define AppName "Tutel"
#define Exe "Tutel.exe"

[Setup]
AppName={#AppName}
AppVersion=1.0.1
AppVerName={#AppName}
AppPublisher={#Publisher}
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}

OutputDir=output
OutputBaseFilename=Tutel-Windows-Installer
SetupIconFile=..\assets\icons\tutel.ico
UninstallDisplayIcon={app}\Tutel.exe
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
LanguageDetectionMethod=locale

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[CustomMessages]
english.CreateDesktopIcon=Create a desktop icon
italian.CreateDesktopIcon=Crea un'icona sul desktop
english.AdditionalOptions=Additional options:
italian.AdditionalOptions=Opzioni aggiuntive:
english.RunTutel=Run Tutel
italian.RunTutel=Avvia Tutel
english.DeleteUserData=Do you want to delete the saved user data?
italian.DeleteUserData=Vuoi cancellare i dati utente salvati?

[Files]
Source: "..\dist\Tutel\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Tutel"; Filename: "{app}\{#Exe}"
Name: "{commondesktop}\Tutel"; Filename: "{app}\{#Exe}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalOptions}"; Flags: unchecked

[Code]
 procedure CurUninstallStepChanged (CurUninstallStep: TUninstallStep);
 var
     mres : integer;
 begin
    case CurUninstallStep of                   
      usUninstall:
        begin
          mres := MsgBox(CustomMessage('DeleteUserData'), mbConfirmation, MB_YESNO or MB_DEFBUTTON2)
          if mres = IDYES then
            DelTree(ExpandConstant('{userappdata}\Myapp'), True, True, True);
       end;
   end;
end; 

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Run]
Filename: "{app}\{#Exe}"; Description: "{cm:RunTutel}"; Flags: nowait postinstall skipifsilent
