#include <array.au3>
#include <String.au3>
#include <endian.au3>

$File = FileOpen ("t_item.tbl", 16)
$File2 = FileOpen ("t_item.txt", 18+32)

$iData = FileRead ($File)

$iArray = StringSplit ($iData, "6974656D", 1)

For $i = 2 to $iArray[0]
	$iNum = Dec(StringTrimLeft(_Endian("0x" & StringMid ($iArray[$i], 7, 4)), 2))
	$iCode = StringMid ($iArray[$i], 11)
	$iText = StringSplit ($iCode, "FFFF", 1)
	If UBound($iText) >= 3 Then
		$iText1 = _HexToString($iText[UBound($iText)-1])
		$iText1 = StringReplace($iText1, @LF, "\n")
		$iText2 = _ArrayToString ($iText, "FFFF", 1, UBound($iText)-2)
		FileWriteLine ($File2, $iNum & @TAB & '0x' & $iText2 & @TAB & $iText1 & @CRLF)
	Else
		FileWriteLine ($File2, $iNum & @TAB & '0x' & $iCode & @CRLF)
	EndIf
Next

MsgBox (0, '', "Done!")
