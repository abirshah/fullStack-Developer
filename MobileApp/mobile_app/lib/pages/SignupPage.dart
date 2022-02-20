import 'package:flutter/material.dart';
import 'package:flutter_general/TextFields.dart';
import 'package:flutter_general/Toast.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/exception/UserIdAlreadyTaken.dart';
import 'package:mobile_app/model/exception/UserWithIdDoesNotExist.dart';
import 'package:mobile_app/router.dart';

class SignupPage extends StatelessWidget {

  String userId = "";
  String password = "";
  String email = "";

  build(context) {
    return Scaffold(
      backgroundColor: Color(0xffe6e6e6),
      body: Column(
        children: [
          Spacer(flex: 2),
          halveticaBoldText("Please Register ...",fontSize: 30),
          SizedBox(height: 20,),
          Spacer(flex: 1),
          FancyTextField(title: "Email",onValueChanged: (value){email = value;},),
          Spacer(flex: 1),
          FancyTextField(title: "User Id",onValueChanged: (value){userId = value;},),
          Spacer(flex: 1),
          FancyTextField(title: "Password",onValueChanged: (value){password = value;},),
          Spacer(flex: 1),
          createRoundedCornerRaisedButton("Register", onPress: () {

            Future<void> result = ServerGateway.instance().signup(email,userId, password);
            result.then((value) {
              wipeAllPagesAndGoTo(context, LoginPagePath);
            });

            result.onError((error, stackTrace)  {

              if(error is UserIdAlreadyTaken)
                toast("user with id $userId already exist!",context);
              else
                toast("failed with unknown reason!", context);
            });

          },minWidth: 100),


          Spacer(flex: 2),
        ],
      ),
    );
  }

}

