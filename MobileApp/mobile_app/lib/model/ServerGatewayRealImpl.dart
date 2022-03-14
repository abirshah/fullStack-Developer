

import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

import 'package:flutter/material.dart';
import 'package:mobile_app/model/dto/AccessInfo.dart';
import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/model/dto/CapturedImageOrVideo.dart';
import 'package:mobile_app/model/dto/Event.dart';
import 'package:mobile_app/model/dto/NotificationInfo.dart';
import 'package:mobile_app/model/dto/Pet.dart';
import 'package:mobile_app/model/dto/PetOwner.dart';
import 'package:mobile_app/model/exception/UserIdAlreadyTaken.dart';
import 'package:path_provider/path_provider.dart';

import 'ServerGateway.dart';
import 'dto/UserBase.dart';
import 'exception/PasswordDoesNotMatch.dart';
import 'exception/UserWithIdDoesNotExist.dart';
import 'package:flutter/services.dart' show rootBundle;

class ServerGatewayRealImpl extends ServerGateway
{
  StreamController<NotificationInfo> _notificationsStreamController = StreamController<NotificationInfo>.broadcast();
  int delayMillis = 1000;
  UserBase? get signedInUser => _signedInUser;
  UserBase? _signedInUser = null;
  List<Pet> petsList = [
    Pet("Pet 1","Dog",[]),
    Pet("Pet 2","Cat",[]),
    Pet("Pet 3","Frog",[]),
    Pet("Pet 4","Rabbit",[]),
    Pet("Pet 5","Dog",[]),
    Pet("Pet 6","Cat",[]),
  ];
  

  Future<void> initialize() async{
    await getSignedInUser();
    await _saveToFile("info", "{}");
/*


    Timer.periodic(Duration(seconds: 3), (timer) {

      _notificationsStreamController.sink.add(NotificationInfo( "type  ${timer.tick}", "access  ${timer.tick}", "date  ${timer.tick}"));

    });
*/


    return Future.value();
  }


  ServerGatewayRealImpl();
  
  
  @override
  Future<UserBase?> getSignedInUser() {
    return _doAfterDelay(() async{

      if(await _doesFileExist("loggedInUser")) {
        _signedInUser = UserBase.fromJson(await _getContentOfFile("loggedInUser"));
        return _signedInUser;
      }

      return null;
    });
  }

  @override
  Future<bool> isUserSignedIn() {
    return _doAfterDelay(() async{
      await getSignedInUser();
      return _signedInUser!=null;
    });
  }

  @override
  Future<void> logout() {
    return _doAfterDelay(() {
      _signedInUser = null;
      _deleteTempFile("loggedInUser");
    });
  }


  @override
  Future<void> signIn(String userId, String password) async{
    await Future.delayed(Duration(seconds: 2));
    await throwExceptionIfUserIdDoesNotExist(userId);
    var user = UserBase.fromJson(await _getContentOfFile("user_$userId"));

    if(user.password!=password)
      throw PasswordDoesNotMatch();

    _signedInUser = user;
    await _saveToFile("loggedInUser", user.toJsonString());
  }

  @override
  Future<void> signup(String email, String userId, String password) async{
    await throwExceptionIfUserIdIsAlreadyTaken(userId);
    UserBase user;
    if(await _getNumberOfRegisteredUsers() == 0)
       user = Admin(email,userId,password);
    else
      user = PetOwner(email, userId, password);

    await _updateInfo("usersCount", 1);
    await _saveToFile("user_$userId",user.toJsonString());
  }



  Future<void> _updateInfo(String key,dynamic value)
  async {
    var infoFile = await getInfoFileContent();
    infoFile[key] = value;
    await _saveToFile("info", jsonEncode(infoFile));
  }

  Future<int> _getNumberOfRegisteredUsers()
  async{

    var infoFile = await getInfoFileContent();
    if(infoFile.containsKey("usersCount"))
      return infoFile["usersCount"] as int;
    else
      return 0;

  }

  Future<Map> getInfoFileContent()
  async{
    return jsonDecode(await _getContentOfFile("info"));
  }


  Future _saveToFile(String fileName,String content) async {

    File file = await getTempFile(fileName);
    await file.create();

    await file.writeAsString(content);
  }

  Future<String> _getContentOfFile(String fileName) async {
    File file = await getTempFile(fileName);
    return await file.readAsString();
  }

  Future _deleteTempFile(String fileName) async {
    File file = await getTempFile(fileName);
    await file.delete();
  }

  Future<File> getTempFile(String fileName) async {
    var directory = await getExternalStorageDirectory();
    var file = File(directory!.path+"/"+fileName);
    return file;
  }


  Future<bool> _doesFileExist(String fileName) async{
    File file = await getTempFile(fileName);
    return file.exists();
  }

  Future<T> _doAfterDelay <T> (FutureOr<T> Function() task)
  {
    return Future.delayed(Duration(milliseconds: delayMillis),(){
      return task();
    });
  }

  Future<void> throwExceptionIfUserIdIsAlreadyTaken(String userId) async{
    if(await _doesFileExist("user_$userId"))
      throw UserIdAlreadyTaken();
  }

  Future<void> throwExceptionIfUserIdDoesNotExist(String userId) async{
    if(!(await _doesFileExist("user_$userId")))
      throw UserWithIdDoesNotExist();
  }

  @override
  Future<List<Pet>> fetchPets() {
    return _doAfterDelay(() {
      return petsList;
    });
  }

  Future<void> addPet(Pet pet)
  {
    return _doAfterDelay(() {
      petsList.add(pet);
    });
  }

  @override
  Stream<NotificationInfo> notificationsStream() {

     _extractEventsContent().then((value) async{
       var list = value.map<NotificationInfo>((e) => NotificationInfo(e.type,e.access,e.date)).toList();

       if(list.isEmpty)
         return;

       if(list.length>3)
         list = list.sublist(list.length-3,list.length);


       var index = 0;
       Timer timer ;

       timer = Timer.periodic(Duration(seconds: 1), (timer) {

         if(list.length>index)
         {
           _notificationsStreamController.sink.add(list[index]);
           index++;
         }else
           timer.cancel();

       });


     });


    return _notificationsStreamController.stream;

  }

  @override
  Future<List<AccessInfo>> fetchAccessInfo() async{

    var list = await _extractEventsContent();
    return list.map<AccessInfo>((e) => AccessInfo(
        e.type,e.access,e.date
    )).toList();

  }

  @override
  Future<List<CapturedImageOrVideo>> fetchCapturedImages() {

    return _doAfterDelay(()  async{
      return [
      ];
    });
  }

  @override
  Future<List<CapturedImageOrVideo>> fetchCapturedVideos() async {

    var list = await _extractEventsContent();
    return list.map<CapturedImageOrVideo>((e) => CapturedImageOrVideo(
      e.type,e.date,e.fileUrl,true
    )).toList();
  }

  Future<List<Event>> _extractEventsContent() async {
    var response = await http.get(Uri.parse("http://10.0.2.2:8000/events"));
    var eventsList = jsonDecode(response.body) as List;
    return eventsList.map<Event>((e) {
      var m = e as Map;
      var type = m["classes"].toString();
      var date = m["ts"].toString();
      var access_granted = m["access_granted"].toString();
      var id = m["id"].toString();
      var url = "https://video-snapshots.s3.amazonaws.com/"+ m["video"].toString();
      return  Event(type,access_granted,date,id,url);
    }).toList();
  }


  Future<File> getImageFileFromAssets(String assetPath,String destFileName) async {
    final byteData = await rootBundle.load(assetPath);

    final file = File('${(await getTemporaryDirectory()).path}/$destFileName');
    await file.create();
    await file.writeAsBytes(byteData.buffer.asUint8List(byteData.offsetInBytes, byteData.lengthInBytes));

    return file;
  }

  @override
  Future<File> downloadFile(String imageOrVideoUrl) async{
    print("going to download $imageOrVideoUrl");

    var response = await http.get(Uri.parse(imageOrVideoUrl));
    final bytes = utf8.encode(imageOrVideoUrl);
    final base64Str = base64.encode(bytes);
    var file = await getTempFile(base64Str);
    file.create();
    print("file was download and it was ${response.bodyBytes.length}");
    print("file path : "+file.path);
    file.writeAsBytesSync(response.bodyBytes);
    return file;
  }

}