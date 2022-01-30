

import 'dart:io';

import 'package:path_provider/path_provider.dart';

class FileManager
{
  FileManager._();
  static FileManager? _instance;
  static FileManager get instance{

    if(_instance == null)
      _instance = FileManager._();

    return _instance!;
  }

  Future saveToFile(String fileAbsPath,String content,{bool createIfNotExists = true}) async {

    File file = File(fileAbsPath);

    if(!file.existsSync() && !createIfNotExists)
      throw Exception("file did not exists and we were not allowed to create! $createIfNotExists");

    await file.create();
    await file.writeAsString(content);
  }

  Future<String> getContentOfFile(String fileAbsPath,{bool returnDefaultStringIfFileDoesNotExist= true,String defaultValue = ""}) async {
    File file = File(fileAbsPath);

    if(!file.existsSync()) {

      if(returnDefaultStringIfFileDoesNotExist)
        return defaultValue;

      throw Exception("file did not exist! $fileAbsPath");
    }

    return await file.readAsString();
  }

  Future deleteFile(String fileAbsPath) async {
    File file = File(fileAbsPath);
    await file.delete();
  }

  Future<bool> doesFileExist(String fileAbsPath) async{
    File file = File(fileAbsPath);
    return file.exists();
  }


  Future<File> getFileInsideSupportDir(String fileName) async {
    var directory = await getApplicationSupportDirectory();
    var file = File(directory.path+"/"+fileName);
    return file;
  }
}