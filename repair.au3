
#include <File.au3>
#include <array.au3>

Global $Array = _FileListToArray(@ScriptDir & '\in', '*.xml')

Global $iDrive, $iDir, $iName, $iExt, $iTranslate, $iRepair
Global $iLogile = FileOpen ('log.txt', 10)
;_ArrayDisplay ($Array)

ProgressOn('', 'Подождите...', "", (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)

For $j = 1 to $Array[0]
	$File2 = (@ScriptDir & '\in\' & $Array[$j])
	; MsgBox (0, 'Сообщение', $File2)
	_PathSplit($File2, $iDrive, $iDir, $iName, $iExt)
	If Not FileExists ($File2) Then
		;MsgBox (0, 'Сообщение', "Файл " & $File2 & " не существует!")
		FileWriteLine ($iLogile, "Файл " & $File2 & " не существует!")
		ContinueLoop
	EndIf

	_FileReadToArray($File2, $iTranslate)
	If FileExists(@ScriptDir & '\new_fix\' & $Array[$j]) Then 
		_FileReadToArray(@ScriptDir & '\new_fix\' & $Array[$j], $iRepair)
	Else
		MsgBox(0, '', 'Файл не существует!')
		ContinueLoop
	EndIf
	$iNewFile = FileOpen (@ScriptDir & '\out\' & $iName & '.xml', 10)

	$a = $iTranslate[0]
	$b = $iRepair[0]

	If $a <> $b Then
		MsgBox (0, 'Собщение', $Array[$j] & " Разное кол-во строк!" & @CR & "Перевод: " & $a & @CR & "Оригинал: " & $b)
		FileWriteLine ($iLogile, $File2 & ": Разное кол-во строк! Перевод: " & $a & " Оригинал: " & $b)
		FileClose ($iNewFile)
		FileDelete (@ScriptDir & '\out\' & $iName & '.xml')
		ContinueLoop
	EndIf

	For $i = 0 to $a
		If StringInStr($iTranslate[$i], '[[') Then $iTranslate[$i] = $iRepair[$i]
		If Mod($i, 2) = 0 Then $iTranslate[$i] = $iRepair[$i]
		$Percent = (100/$a) * $i
		If Mod($i, 100) = 0 Then ProgressSet ($Percent, 'Строка: ' & $i & ' из ' & $a & _
		@CRLF & 'Файл: ' & $j & ' из ' & $Array[0] )
	Next
		
		_FileWriteFromArray ($iNewFile, $iTranslate, 1)
		FileClose ($iNewFile)
		; FileMove ($File2, @ScriptDir & '\' & $iName & '_bak.xml')
		; FileMove ($iDrive & $iDir & $iName & '_new.xml', $iDrive & $iDir & $iName & '.xml')
		
		; FileWriteLine ($iLogile, $File2 & " Готово!")
Next

ProgressSet(100, "Готово!")
MsgBox (0, 'Собщение', 'Готово!')
FileWriteLine ($iLogile, "Готово!")
ProgressOff()

;ShellExecute("log.txt")
