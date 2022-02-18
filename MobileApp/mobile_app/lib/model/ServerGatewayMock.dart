

import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/model/dto/Pet.dart';
import 'package:mobile_app/model/dto/PetOwner.dart';
import 'package:mobile_app/model/exception/UserIdAlreadyTaken.dart';
import 'package:path_provider/path_provider.dart';

import 'ServerGateway.dart';
import 'dto/UserBase.dart';
import 'exception/PasswordDoesNotMatch.dart';
import 'exception/UserWithIdDoesNotExist.dart';


class ServerGatewayMock extends ServerGateway
{
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
    return Future.value();
  }


  ServerGatewayMock();
  
  
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
    var directory = await getApplicationSupportDirectory();
    var file = File(directory.path+"/"+fileName);
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
}