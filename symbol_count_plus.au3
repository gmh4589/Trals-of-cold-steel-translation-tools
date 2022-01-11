#include <MsgboxConstants.au3>
#include <File.au3>
#include <array.au3>
#include <Date.au3>

Global $REPLACE = [ ["А", "A"], ["Б", "S"], ["В", "B"], ["Г", "G"], ["Д", "D"], ["Е", "E"], ["Ё", "E"], ["З", "3"], ["И", "I"], ["К", "K"], ["Л", "L"], ["М", "M"], ["Н", "H"], ["О", "O"], ["П", "N"], ["Р", "P"], ["С", "C"], ["Т", "T"], ["У", "Y"], ["Ф", "F"], ["Х", "X"], ["Ч", "V"], ["Э", "'"], ["Ю", "Q"], ["Я", "R"], ["а", "a"], ["б", "U"], ["в", "b"], ["г", "g"], ["д", "d"], ["е", "e"], ["ё", "e"], ["ж", "s"], ["з", "z"], ["и", "&amp;"], ["й", "j"], ["к", "k"], ["л", "l"], ["м", "m"], ["н", "h"], ["о", "o"], ["п", "n"], ["р", "p"], ["с", "c"], ["т", "t"], ["у", "y"], ["ф", "f"], ["х", "x"], ["ц", "u"], ["ч", "v"], ["ш", "w"], ["щ", "W"], ["ы", "J"], ["ь", "i"], ["э", "Z"], ["ю", "q"], ["я", "r"], ["Mod\OUmeh      ", "   Mod\OUmeh   "], ["3atovka         ", "     3atovka     "] ]
Global $REMOVE = ["Й", "Ц", "Ш", "Щ", "ъ", "Ъ", "Ж", "Ы", "Ь"]
Global $REMOVE2 = ["ウ", "女", "男"]
Global $iFlag = 1 ; Поставить 1 если нужно обрубать длинные концы
Global $f_ar = _FileListToArray(@ScriptDir & '\in')
Global $space = '                                                                                                    '
Global $begin = TimerInit(), $iDrive, $iDir, $iName, $iExp, $z = UBound ($REPLACE) - 1, $Hour, $Mins, $Secs, $FileO, $FileT, $next = 0, $y = UBound ($REMOVE) - 1, $x = UBound ($REMOVE2) - 1

$iFile3 = FileOpen("error_list.txt", 2)

For $n = 1 to $f_ar[0]
	$iFile2 = ('in\' & $f_ar[$n])
	$iFile1 = ('new_fix\' & $f_ar[$n])

	_FileReadToArray ($iFile1, $FileO)
	_FileReadToArray ($iFile2, $FileT)
	$iStringCountO = UBound($FileO) - 1
	$iStringCountT = UBound($FileT) - 1
	$a = $iStringCountT
		
	If $iStringCountO = $iStringCountT Then

		$iFile4 = FileOpen("out\" & $f_ar[$n], 2)
		ProgressOn('', 'Подождите... ', "", (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
		
			For $i = 1 to $iStringCountO
				$line1 = $FileO[$i]
				$line2 = $FileT[$i]
					For $j = 0 to $z
						$line2 = StringReplace ($line2, $REPLACE[$j][0], $REPLACE[$j][1], 0, 1)
					Next
				$iRplLine = StringReplace ($line2, "&amp;", "&")
				$line1 = StringReplace ($line1, "&amp;", "&")
				$b = StringLen ($line1) - StringLen ($iRplLine)
					For $k = 0 to $y
						If StringInStr ($line2, $REMOVE[$k], 1) Then 
							StringReplace ($line2, $REMOVE[$k], $REMOVE[$k], 0, 1)
							$b -= @extended
						EndIf
					Next
					For $k = 0 to $x
						If StringInStr ($line2, $REMOVE2[$k], 1) Then $b -= 2
					Next
						If $b >= 0 Then
							If StringInStr ($line2, '<', 0, 2)  >10 Then
								$tab = StringSplit($line2,'<')
								FileWriteLine ($iFile4, $tab[1] & '<' & $tab[2] & StringRight ($space, $b) & '<' & $tab[3])
							Else
								FileWriteLine ($iFile4, $line2 & StringRight ($space, $b))
							EndIf
						ElseIf $b < 0 Then
							$line2 = StringReplace ($line2, "&amp;", "&")
							If $iFlag = 1 Then
								$iline2 = StringSplit($line2, '<')
								$linenew = StringReplace (StringTrimRight($iline2[2], Abs($b)), "&", "&amp;")  ; удаляет длинные концы!!!
								$line2 = $iline2[1] & '<' & $linenew & '<' & $iline2[3]
							EndIf
							FileWriteLine ($iFile4, $line2)
							If Mod($i, 2) = 1 Then FileWriteLine ($iFile3, $f_ar[$n] & @TAB & $i & @TAB & $b & ' символов' & @TAB & $FileT[$i])
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
			
		FileWriteLine ($iFile3,'======================================================')
		$dif = TimerDiff($begin)
		_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
		$dif = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
		ProgressSet(100, "Готово!" & @CRLF & "Прошло: "  & $dif)
		; MsgBox (0, 'Сообщение', 'Готово!')
		ProgressOff()
	Else 
		FileWriteLine ($iFile3,'Разное кол-во строк' & @TAB & $iStringCountO & @TAB & $iStringCountT & @TAB & $iFile1)
		FileWriteLine ($iFile3,'======================================================')
	EndIf
	
Next

;ShellExecute ("error_list.txt")


