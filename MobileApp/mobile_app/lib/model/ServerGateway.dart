

import 'dart:io';

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
      //  _instance = ServerGatewayImplementation();
        _instance = ServerGatewayMock();
      }

    return _instance!;
  }

  Future<void> initialize();

  Future<void> signup(String email,String userId,String password);
  Future<void> signIn(String userId,String password);

  Future<List<Pet>> fetchPets();


  Future<void> logout();
  Future<bool> isUserSignedIn();
  Future<UserBase?> getSignedInUser();

  Future<void> addPet(Pet pet) ;

}