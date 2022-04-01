


import 'dart:convert';

import 'package:mobile_app/model/dto/UserBase.dart';

class PetOwner extends UserBase
{
  PetOwner(String email, String userId, String password) : super(email, userId, password);


  String toJsonString() {

    return jsonEncode({
      "isAdmin":false,
      "userId":userId,
      "email":email,
      "password":password
    });
  }
}