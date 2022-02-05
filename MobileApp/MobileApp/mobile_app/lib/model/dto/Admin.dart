


import 'dart:convert';

import 'package:mobile_app/model/dto/UserBase.dart';

class Admin extends UserBase
{
  Admin(String email, String userId, String password) : super(email, userId, password);

  String toJsonString() {

    return jsonEncode({
      "isAdmin":true,
      "userId":userId,
      "email":email,
      "password":password
    });
  }


}