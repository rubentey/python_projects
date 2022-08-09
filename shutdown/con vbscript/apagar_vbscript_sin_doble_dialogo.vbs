Set Shell = CreateObject("WScript.Shell")

     Answer = MsgBox("Quieres salir de la sesion?",vbYesNo,"Salir de Citrix:")
     If Answer = vbYes Then
          Shell.run "shutdown.exe -s -t 60"
          Ending = 1
     ElseIf Answer = vbNo Then
     End If