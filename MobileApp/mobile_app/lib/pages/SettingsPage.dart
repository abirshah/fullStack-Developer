import 'package:flutter/material.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/pages/ToggleButton.dart';
import 'package:mobile_app/router.dart';

class SettingsPage extends StatelessWidget {
  String title = "";

  MainMenu() {
    this.title = "welcome";
  }

  build(context) {
    return Scaffold(
      appBar: buildAppBar(),
      body: createBody(context),
    );
  }

  Widget createBody(context)
  {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [

            createRoundedCornerRaisedButton("Add User" ,onPress:  (){ print("settings");},minWidth: 100,height: 50),
            createRoundedCornerRaisedButton("Edit",onPress: (){print("live camera");},minWidth: 100,height: 50),
        ],),

        createRoundedCornerRaisedButton("Delete User",onPress: (){},minWidth: 100,height: 50),
      ],
    );
  }

  Widget createButton(String title, void Function() callback )
  {
    return RaisedButton(onPressed:callback,child: Text(title),);
  }


  AppBar buildAppBar() {
    return AppBar(
      actions: [
        IconButton(
          icon: Icon(Icons.ac_unit_outlined),
          onPressed: () {},
        ),
        IconButton(
          icon: Icon(Icons.accessible_sharp),
          onPressed: () {},
        ),
        Container(
          child: ToggleButton(),
          width: 50,
          height: 50,
        )
      ],
    );
  }
}
