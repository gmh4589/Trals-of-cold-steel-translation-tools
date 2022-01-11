#include <WindowsConstants.au3>
#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <ComboConstants.au3>
#include <Constants.au3>
#include <File.au3>
#include <GDIPlus.au3>
#include <MsgboxConstants.au3>

Opt("GUIOnEventMode", 1)

$hGui = GUICreate("Text Converter", 175, 140)
GUISetIcon ("Data\i.ico")

Global $iDrive, $iDir, $iName, $iExp

GUISetOnEvent($GUI_EVENT_CLOSE, "AppClose")
$iCancel = GUICtrlCreateButton("Отмена", 45, 110, 80, 25)
GUICtrlSetTip(-1, 'Выйти из программы')
GUICtrlSetOnEvent($iCancel, "AppClose")

$iTXT = GUICtrlCreateButton("DAT2XML", 5, 5, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать DAT в XML')
GUICtrlSetOnEvent($iTXT, "DAT2XML")

$iPDF = GUICtrlCreateButton("TBL2XML", 90, 5, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать TBL в XML')
GUICtrlSetOnEvent($iPDF, "TBL2XML")

$iEPUB = GUICtrlCreateButton("DAT2XML(fol)", 5, 30, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать DAT в XML папкой')
GUICtrlSetOnEvent($iEPUB, "DAT2XML4FOLDER")

$iRTF = GUICtrlCreateButton("TBL2XML(fol)", 90, 30, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать TBL в XML папкой')
GUICtrlSetOnEvent($iRTF, "TBL2XML4FOLDER")

$iTXTZ = GUICtrlCreateButton("XML2DAT", 5, 55, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать XML в DAT')
GUICtrlSetOnEvent($iTXTZ, "XML2DAT")

$iDOCX = GUICtrlCreateButton("XML2TBL", 90, 55, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать XML в TBL')
GUICtrlSetOnEvent($iDOCX, "XML2TBL")

$iHTMLZ = GUICtrlCreateButton("XML2DAT(fol)", 5, 80, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать в XML в DAT папкой')
GUICtrlSetOnEvent($iHTMLZ, "XML2DAT4FOLDER")

$iPDB = GUICtrlCreateButton("XML2TBL(fol)", 90, 80, 80, 25)
GUICtrlSetTip(-1, 'Конвертировать в XML в DAT папкой')
GUICtrlSetOnEvent($iPDB, "XML2TBL4FOLDER")

GUISetState(@SW_SHOW)

While 1
	Sleep(1)
WEnd

Func AppClose()
  Exit
EndFunc 

Func DAT2XML()
	$FileName = FileOpenDialog ('', @ScriptDir, "DAT Files (*.dat)|All files (*.*)")
	ShellExecuteWait (@ScriptDir & '\dist\trails.exe', ' dat_to_xml "' & $FileName & '"', @ScriptDir)
EndFunc

Func TBL2XML()
	$FileName = FileOpenDialog ('', @ScriptDir, "TBL Files (*.tbl)|All files (*.*)")
	ShellExecuteWait (@ScriptDir & '\dist\trails.exe', ' tbl_to_xml "' & $FileName & '"', @ScriptDir)
EndFunc

Func XML2TBL()
	$FileName = FileOpenDialog ('', @ScriptDir, "XML Files (*.xml)|All files (*.*)")
	ShellExecuteWait (@ScriptDir & '\dist\trails.exe', ' xml_to_tbl "' & $FileName & '"', @ScriptDir)
EndFunc

Func XML2DAT()
	$FileName = FileOpenDialog ('', @ScriptDir, "XML Files (*.xml)|All files (*.*)")
	ShellExecuteWait (@ScriptDir & '\dist\trails.exe', ' xml_to_dat "' & $FileName & '"', @ScriptDir)
EndFunc

Func XML2DAT4FOLDER()
$iFolderList = FileSelectFolder('', 'C:\Users\40pja\Desktop\fl\tl\out')
	If @error <> 1 Then
		$iFile = FileOpen(@TempDir & "\temp.bat", 10)
		FileWriteLine ($iFile, "chcp 65001")
		FileWriteLine ($iFile, "@echo off")
		FileWriteLine ($iFile, "DIR/B/O:N/S """ & $iFolderList & """ > " & @TempDir & "\file_list.txt");
		FileClose ($iFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir, "open")
		Local $iStringCount = _FileCountLines(@TempDir & "\file_list.txt")
		$a = -1
		$aFile = FileOpen(@TempDir & "\temp.bat", 10)
			While $a <= $iStringCount
				$a += 1
				$FileName = FileReadLine (@TempDir & "\file_list.txt", $a+1)
				_PathSplit($FileName, $iDrive, $iDir, $iName, $iExp)
				If $iExp = ".xml" Then FileWriteLine ($aFile, @ScriptDir & '\dist\trails.exe xml_to_dat "' & $FileName & '"')
			Wend
		FileWriteLine ($aFile, "pause")
		FileClose ($aFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir)
		FileDelete (@TempDir & "\temp.bat")
		FileDelete (@TempDir & "\file_list.txt")
	EndIf
EndFunc

Func XML2TBL4FOLDER()
$iFolderList = FileSelectFolder("", "")
	If @error <> 1 Then
		$iFile = FileOpen(@TempDir & "\temp.bat", 10)
		FileWriteLine ($iFile, "chcp 65001")
		FileWriteLine ($iFile, "@echo off")
		FileWriteLine ($iFile, "DIR/B/O:N/S """ & $iFolderList & """ > " & @TempDir & "\file_list.txt");
		FileClose ($iFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir, "open")
		Local $iStringCount = _FileCountLines(@TempDir & "\file_list.txt")
		$a = -1
		$aFile = FileOpen(@TempDir & "\temp.bat", 10)
			While $a <= $iStringCount
				$a += 1
				$FileName = FileReadLine (@TempDir & "\file_list.txt", $a+1)
				_PathSplit($FileName, $iDrive, $iDir, $iName, $iExp)
				If $iExp = ".xml" Then FileWriteLine ($aFile, @ScriptDir & '\dist\trails.exe xml_to_tbl "' & $FileName & '"')
			Wend
		FileWriteLine ($aFile, "pause")
		FileClose ($aFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir)
		FileDelete (@TempDir & "\temp.bat")
		FileDelete (@TempDir & "\file_list.txt")
	EndIf
EndFunc

Func DAT2XML4FOLDER()
$iFolderList = FileSelectFolder("", "")
	If @error <> 1 Then
		$iFile = FileOpen(@TempDir & "\temp.bat", 10)
		FileWriteLine ($iFile, "chcp 65001")
		FileWriteLine ($iFile, "@echo off")
		FileWriteLine ($iFile, "DIR/B/O:N/S """ & $iFolderList & """ > " & @TempDir & "\file_list.txt");
		FileClose ($iFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir, "open")
		Local $iStringCount = _FileCountLines(@TempDir & "\file_list.txt")
		$a = -1
		$aFile = FileOpen(@TempDir & "\temp.bat", 10)
			While $a <= $iStringCount
				$a += 1
				$FileName = FileReadLine (@TempDir & "\file_list.txt", $a+1)
				_PathSplit($FileName, $iDrive, $iDir, $iName, $iExp)
				If $iExp = ".dat" Then FileWriteLine ($aFile, @ScriptDir & '\dist\trails.exe dat_to_xml "' & $FileName & '"')
			Wend
		FileWriteLine ($aFile, "pause")
		FileClose ($aFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir)
		FileDelete (@TempDir & "\temp.bat")
		FileDelete (@TempDir & "\file_list.txt")
	EndIf
EndFunc

Func TBL2XML4FOLDER()
$iFolderList = FileSelectFolder("", "")
	If @error <> 1 Then
		$iFile = FileOpen(@TempDir & "\temp.bat", 10)
		FileWriteLine ($iFile, "chcp 65001")
		FileWriteLine ($iFile, "@echo off")
		FileWriteLine ($iFile, "DIR/B/O:N/S """ & $iFolderList & """ > " & @TempDir & "\file_list.txt");
		FileClose ($iFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir, "open")
		Local $iStringCount = _FileCountLines(@TempDir & "\file_list.txt")
		$a = -1
		$aFile = FileOpen(@TempDir & "\temp.bat", 10)
			While $a <= $iStringCount
				$a += 1
				$FileName = FileReadLine (@TempDir & "\file_list.txt", $a+1)
				_PathSplit($FileName, $iDrive, $iDir, $iName, $iExp)
				If $iExp = ".tbl" Then FileWriteLine ($aFile, @ScriptDir & '\dist\trails.exe tbl_to_xml "' & $FileName & '"')
			Wend
		FileWriteLine ($aFile, "pause")
		FileClose ($aFile)
		ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir)
		FileDelete (@TempDir & "\temp.bat")
		FileDelete (@TempDir & "\file_list.txt")
	EndIf
EndFunc