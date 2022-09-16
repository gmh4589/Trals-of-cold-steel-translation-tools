#include <MsgboxConstants.au3>
#include <File.au3>
#include <array.au3>
#include <Date.au3>
#include <String.au3>

; $out = '\out' ;папка с переводом
; $in = '\in' ;папка с оригиналом
$out = '\in' ;папка с переводом
$in = '\out' ;папка с оригиналом

Global $f_ar = _FileListToArray(@ScriptDir & $in, "*.dat")
$iFile3 = FileOpen("error_list.txt", 2)

ProgressOn('', 'Подождите... ', "", (@DesktopWidth / 2) - 150, (@DesktopHeight / 2) - 62, 18)

$zamen = 0

For $n = 1 to $f_ar[0]
	$iFile1 = FileOpen(@ScriptDir & $in & '\' & $f_ar[$n], 16)
	$iFile2 = FileOpen(@ScriptDir & $out & '\' & $f_ar[$n], 26)

	$b = FileRead($iFile1)

		; $arr = StringSplit($b, '5965730001006A01004E6F', 1) ;yes_no
		; $b = _ArrayToString($arr, "44610001006A0100486574", 1)
	
		$arr = StringSplit($b, '206F6B70656E6C26215E5E', 1)
		$b = _ArrayToString($arr, "206F6B70656E6C262101", 1)
	
	FileWrite($iFile2, $b)
	
	$Percent = ($n/100) * $f_ar[0]
	ProgressSet ($Percent, 'Файл: ' & $n & ' из ' & $f_ar[0] & @TAB & 'Замен: ' & $zamen & @CRLF & StringLeft ($Percent, 4) & ' %')
Next

ProgressOff()

MsgBox (0, '', 'DONE!')