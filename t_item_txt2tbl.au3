#include <array.au3>
#include <String.au3>
#include <endian.au3>
#include <File.au3>

$OldTXT =  FileOpen("t_item.txt", 16)
MsgBox(0, '', _FileCountLines("t_item.txt"))
Global $iArray['']
For $j = 1 to 972
	$String = FileReadLine ($OldTXT, $j)
	_ArrayAdd($iArray, $String)
Next

$NewTBL = FileOpen('t_item.tbl', 18)
FileWrite ($NewTBL, '0xCB03')

For $i = 0 to UBound($iArray)-1
	$Data = StringSplit ($iArray[$i], @TAB, 1)
	;_ArrayDisplay($Data)
	$Text1 = ''
		If UBound($Data) = 4 Then 
			$Text1 = $Data[3]
			$c = StringRegExp($Data[2], '\N\N', 3)
			; _ArrayDisplay($c)
			$z = UBound($c)-1
			$b = StringLen($Text1)
			$Long = _Endian(Hex($z+$b+4))
			; MsgBox(0, '', $z & @CRLF & $b & @CRLF & $Long)
		ElseIf UBound($Data) < 4 Then
			$c = StringRegExp($Data[2], '\N\N', 3)
			; _ArrayDisplay($c)
			$z = UBound($c)+1
			$Long = _Endian(Hex($z))
		EndIf
	$Num = _Endian(Hex($Data[1]))
	FileWrite ($NewTBL, '0x6974656D00')
	FileWrite ($NewTBL, StringTrimRight($Long, 2))
	FileWrite ($NewTBL, StringTrimRight($Num, 2))
	FileWrite ($NewTBL, $Data[2])
	If UBound($Data) = 4 Then FileWrite ($NewTBL, '0xFFFF')
	If UBound($Data) = 4 Then FileWrite ($NewTBL, $Data[3])
Next

MsgBox (0, '', "Done!")
