

import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:mobile_app/model/ServerGatewayRealImpl.dart';
import 'package:mobile_app/model/dto/AccessInfo.dart';
import 'package:mobile_app/model/dto/CapturedImageOrVideo.dart';
import 'package:mobile_app/model/dto/NotificationInfo.dart';
import 'package:mobile_app/model/dto/Pet.dart';

import 'ServerGatewayMock.dart';
import 'dto/UserBase.dart';


abstract class ServerGateway{

  static ServerGateway? _instance;
  UserBase? get signedInUser;

  static ServerGateway instance()
  {
    if(_instance == null)
      {
        _instance = ServerGatewayRealImpl();
        //_instance = ServerGatewayMock();
      }

    return _instance!;
  }

  Future<void> initialize();

  Future<void> signup(String email,String userId,String password);
  Future<void> signIn(String userId,String password);

  Future<List<Pet>> fetchPets();
  Future<List<AccessInfo>> fetchAccessInfo();
  Future<List<CapturedImageOrVideo>> fetchCapturedImages();
  Future<List<CapturedImageOrVideo>> fetchCapturedVideos();


  Future<void> logout();
  Future<bool> isUserSignedIn();
  Future<UserBase?> getSignedInUser();

  Stream<NotificationInfo> notificationsStream();

  Future<void> addPet(Pet pet) ;

  Future<File> downloadFile(String imageOrVideoUrl) ;

}