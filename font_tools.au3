
#include <File.au3>
#include <Array.au3>
#include <Binary.au3>
#include <WinAPI.au3>
#include <Excel.au3>

Local $iDrive, $iDir, $iName, $iExp

$oFile = FileOpenDialog('Пожалуйста, выберите файл *.itf', @ScriptDir, ' (*.itf)', 1)

If $oFile = '' Then Exit

_PathSplit($oFile, $iDrive, $iDir, $iName, $iExp)

$File = FileOpen($oFile, 16)
$head = FileRead($file, 64)

FileSetPos($File, 8, 0)
$Chars = _BinaryToInt32(FileRead($File,4))
FileSetPos($File, 64, 0)

Global $Ch[$Chars][9], $Raw[$Chars]
Global $Cols = ['Символ', 'Смещение', 'Смещение2', 'Ширина', 'Высота', 'Отступ сверху', 'Отступ слева', 'Отступ справа', 'Тип']
$abc = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
$abcA = StringSplit($abc, '')

For $h = 0 to 8
	$Ch[0][$h] = $Cols[$h]
Next

For $i = 1 to $Chars - 1
	$Raw[$i] = FileRead($File, 4)
	$Ch[$i][0] = _BinaryToInt32($Raw[$i])
	$Ch[$i][1] = _BinaryToInt32(FileRead($File, 4))
	$Ch[$i][2] = FileGetPos($File) - 8
Next

$pos = FileGetPos($File)
$EndOF = FileRead($file)
FileSetPos($File, $pos, 0)

For $j = 1 to $Chars - 1
	If $Ch[$j][0] == -1 Then
		$Ch[$j][0] = '-'
			For $k = 1 to 8
				$Ch[$j][$k] = '-'
			Next
	Else
		FileSetPos($File, $Ch[$j][1], 0)
			For $i = 3 to 8
				$Ch[$j][$i] = _BinaryToInt32(FileRead($File, 2))
			Next
		$Ch[$j][0] = ChrW($Ch[$j][0])
		If _ArraySearch($abcA, $Ch[$j][0]) > -1 Then $Ch[$j][7] = 0
	EndIf
Next

Global $oExcel = _Excel_Open(0)
Global $oWorkbook = _Excel_BookNew($oExcel)

Global $colArray = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
Global $arr[$Chars]

For $col = 0 to 8
	For $i = 0 to $Chars - 1
		$arr[$i] = $Ch[$i][$col]
	Next
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $arr, $colArray[$col])
Next

_Excel_BookSaveAs($oWorkbook, @ScriptDir & "\" & $iName & ".xlsx", Default, True)
_Excel_BookClose($oWorkbook)

_ArrayDisplay($Ch, 'Шрифт: ' & $iName & '.itf')

$origChar = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrsTtUuvWwXxYyZz@$'&"
$replaceChar = "АаВвСсДдЕеФфГгНнИьыйКкЛлМмПпОоРрЮюЯяжТтбцчщшХхУуэзБЧЭи"

$origCA = StringSplit($origChar, '')
$repCA = StringSplit($replaceChar, '')

$newFile = FileOpen(@ScriptDir & '\' & $iName & '_new.itf', 26)
	FileWrite($newFile, $head)
		For $i = 1 to $Chars - 1
			$index = _ArraySearch($origCA, $Ch[$i][0], 0, UBound($origCA) - 1, 1, 0, 0, 0)
			$off = $Ch[$i][1]
			If $index > -1 Then $off = $Ch[_ArraySearch($Ch, $repCA[$index], 0, UBound($Ch) - 1, 1, 0, 0, 0)][1]
			FileWrite($newFile, $Raw[$i])
			FileWrite($newFile, _BinaryFromInt32($off))
		Next
	FileWrite($newFile, $EndOF)
FileClose($newFile)

MsgBox(0, '', 'Done!')
