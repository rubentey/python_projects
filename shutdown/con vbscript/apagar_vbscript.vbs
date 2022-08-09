Set Shell = CreateObject("WScript.Shell")

     Answer = MsgBox("Do You Want To" & vbNewLine & "Shut Down Your Computer?",vbYesNo,"Shutdown:")
     If Answer = vbYes Then
          Shell.run "shutdown.exe -s -t 60"
          Ending = 1
     ElseIf Answer = vbNo Then
          Stopping = MsgBox("Do You Wish To Quit?",vbYesNo,"Quit:")
          If Stopping = vbYes Then
               WScript.Quit 0
          End If
     End If