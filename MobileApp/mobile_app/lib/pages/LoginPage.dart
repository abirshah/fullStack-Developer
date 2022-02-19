import 'package:flutter/material.dart';
import 'package:flutter_general/TextFields.dart';
import 'package:flutter_general/Toast.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/exception/PasswordDoesNotMatch.dart';
import 'package:mobile_app/model/exception/UserWithIdDoesNotExist.dart';
import 'package:mobile_app/pages/SignupPage.dart';
import 'package:mobile_app/router.dart';

class LoginPage extends StatelessWidget {

  String userId = "";
  String password = "";

  build(context) {
    return Scaffold(
      backgroundColor: Color(0xffe6e6e6),
      body: Column(
        children: [
          Spacer(flex: 2),
          Text("Automated Pet Door", style: TextStyle(fontSize: 20),),
          SizedBox(height: 20,),
          Text("XGaurd"),
          Spacer(flex: 1),
          FancyTextField(title: "User Id",onValueChanged: (value){userId = value;},),
          Spacer(flex: 1),
          FancyTextField(title: "Password",onValueChanged: (value){password = value;},),
          Spacer(flex: 1),
          createRoundedCornerRaisedButton("Login", onPress: () {

            if(userId=="")
              {
                toast("user id cannot be empty", context);
                return;
              }

            Future<void> result = ServerGateway.instance().signIn(userId, password);
            result.then((value) {
              wipeAllPagesAndGoTo(context, MainMenuPagePath);
            });

            result.onError((error, stackTrace)  {

              if(error is UserWithIdDoesNotExist)
                toast("user with id $userId does not exist!",context);
              else if(error is PasswordDoesNotMatch)
                toast("wrong password!!!",context);
              else
                toast("failed with unknown reason!", context);
            });

          },minWidth: 100),

          Spacer(flex: 1),
          Text("Don't Have Account ?"),
          Spacer(flex: 1),
          createRoundedCornerRaisedButton("Register", onPress: () {
            goToPage(context, SignUpPagePath);
          },minWidth: 100),
          Spacer(flex: 2),
        ],
      ),
    );
  }

}

