#include <MsgboxConstants.au3>
#include <File.au3>
#include <array.au3>
#include <Date.au3>

Global $REPLACE = [ ["и", "&amp;"], ["и", "iiiii"], ["А", "A"], ["Б", "S"], ["В", "B"], ["Г", "G"], ["Д", "D"], ["Е", "E"], ["Ё", "E"], ["З", "3"], ["И", "I"], ["К", "K"], ["Л", "L"], ["М", "M"], ["Н", "H"], ["О", "O"], ["П", "N"], ["Р", "P"], ["С", "C"], ["Т", "T"], ["У", "Y"], ["Ф", "F"], ["Х", "X"], ["Ч", "V"], ["Э", "'"], ["Ю", "Q"], ["Я", "R"], ["а", "a"], ["б", "U"], ["в", "b"], ["г", "g"], ["д", "d"], ["е", "e"], ["ё", "e"], ["ж", "s"], ["з", "z"], ["й", "j"], ["к", "k"], ["л", "l"], ["м", "m"], ["н", "h"], ["о", "o"], ["п", "n"], ["р", "p"], ["с", "c"], ["т", "t"], ["у", "y"], ["ф", "f"], ["х", "x"], ["ц", "u"], ["ч", "v"], ["ш", "w"], ["щ", "W"], ["ы", "J"], ["ь", "i"], ["э", "Z"], ["ю", "q"], ["я", "r"], ["Entry", "Ептяу"] ]

Global $f_ar = _FileListToArray(@ScriptDir & '\in'), $z = UBound ($REPLACE) - 1, $FileO, $begin = TimerInit(), $Hour, $Mins, $Secs


For $n = 1 to $f_ar[0]
	$iFile = ('in\' & $f_ar[$n])

	_FileReadToArray ($iFile, $FileO)
	$a = $FileO[0]

		$iFile4 = FileOpen("out\" & $f_ar[$n], 2)
		ProgressOn('', 'Подождите... ', "", (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
			
			For $i = 0 to 5
				FileWriteLine ($iFile4, $FileO[$i])
			Next
		
			For $i = 6 to $a
				$line2 = $FileO[$i]
				If Mod($i, 2) = 1 Then
						For $j = 0 to $z
							$line2 = StringReplace ($line2, $REPLACE[$j][1], $REPLACE[$j][0], 0, 1)
						Next
					FileWriteLine ($iFile4, $line2)
				Else
					FileWriteLine ($iFile4, $line2)
				EndIf
				$Percent = (100/$a) * $i
				$dif = TimerDiff($begin)
				$elaps = (($dif/$i) * $a) - $dif
				_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
				$time = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
				_TicksToTime(Int($elaps), $Hour, $Mins, $Secs)
				$elaps = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
				If Mod($i, 100) = 0 Then ProgressSet ($Percent, 'Файл: ' & $n & ' из ' & UBound($f_ar)-1 & @TAB & 'Строка: ' & $i & ' из ' & $a & @CRLF & StringLeft ($Percent, 4) & ' %' & @CRLF & "Прошло: " & $time & @TAB & "Осталось: " & $elaps)
			Next
			
		$dif = TimerDiff($begin)
		_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
		$dif = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
		ProgressSet(100, "Готово!" & @CRLF & "Прошло: "  & $dif)
		; MsgBox (0, 'Сообщение', 'Готово!')
		ProgressOff()
Next
