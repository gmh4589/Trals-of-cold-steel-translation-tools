#include <MsgboxConstants.au3>
#include <File.au3>
#include <array.au3>
#include <Date.au3>
#include <String.au3>

$op = '\out' ;папка с переводом
$tp = '\orig' ;папка с оригиналом


Global $f_ar = _FileListToArray(@ScriptDir & $op, "*.dat")
$iFile3 = FileOpen("error_list.txt", 2)

Global $begin = TimerInit(), $Hour, $Mins, $Secs

For $n = 1 to $f_ar[0]
	$iFile2 = FileOpen(@ScriptDir & $op & '\' & $f_ar[$n], 16)
	$iFile1 = FileOpen(@ScriptDir & $tp & '\' & $f_ar[$n], 16)
	
	ProgressOn('', 'Подождите... ', "", (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
		
	$s = FileGetSize(@ScriptDir & $op & '\' & $f_ar[$n])
	For $i = 0 to $s
		$a = FileRead($iFile2, 1)
		$b = FileRead($iFile1, 1)
		
		
		If $a <> $b Then
			If StringIsASCII(_HexToString($a)) = 0 and StringIsASCII(_HexToString($b)) = 0 then 
				MsgBox (0, '', $f_ar[$n] & @TAB & Hex($i))
				;FileWriteLine($iFile3, $f_ar[$n] & @TAB & Hex($i))
				ExitLoop
			EndIf
			;MsgBox (0, '', $a & '<>' & $b)
		EndIf
		
		$Percent = (100/$s) * $i
		$dif = TimerDiff($begin)
		$elaps = (($dif/$i) * $a) - $dif
		_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
		$time = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
		_TicksToTime(Int($elaps), $Hour, $Mins, $Secs)
		$elaps = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
		If Mod($i, 10240) = 0 Then ProgressSet ($Percent, 'Файл: ' & $n & ' из ' & UBound($f_ar)-1 & @TAB & 'Чтение: ' & $i & ' из ' & $s & @CRLF & StringLeft ($Percent, 4) & ' %' & @CRLF & "Прошло: " & $time & @TAB & "Осталось: " & $elaps)
	Next
Next

ProgressOff()

;MsgBox (0, '', 'DONE!')