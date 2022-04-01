

import 'dart:convert';

import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/model/dto/PetOwner.dart';

abstract class UserBase
{
  String email = "";
  String userId = "";
  String password = "";


  UserBase(this.email, this.userId, this.password);

  static fromJson(String  json)
  {
    var decoded = jsonDecode(json);
    var isAdmin = decoded["isAdmin"];
    var email = decoded["email"];
    var userId = decoded["userId"];
    var password = decoded["password"];

    if(isAdmin)
      return Admin(email, userId, password);

    return PetOwner(email, userId, password);
  }



  String toJsonString() ;
}