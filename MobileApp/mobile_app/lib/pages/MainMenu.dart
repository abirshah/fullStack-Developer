import 'package:flutter/material.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/pages/ToggleButton.dart';
import 'package:mobile_app/router.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:android_intent_plus/android_intent.dart';

class MainMenu extends StatelessWidget {
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


  Widget createBody(context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            if (ServerGateway.instance().signedInUser is Admin)
              createRoundedCornerRaisedButton("Settings", onPress: () {
                goToPage(context, SettingsPagePath);
              }, minWidth: 100, height: 50),
            createRoundedCornerRaisedButton("Live Camera", onPress: () async {


               await launch("http://10.0.2.2:8000/video");
            }, minWidth: 100, height: 50),
          ],
        ),
        createRoundedCornerRaisedButton("Open Door", onPress: () {
          goToPage(context, CapturedImagesPath);
        }, minWidth: 100, height: 50),
        createRoundedCornerRaisedButton("Captured Videos", onPress: () {
          goToPage(context, CapturedVideosPath);
        }, minWidth: 100, height: 50),
        createRoundedCornerRaisedButton("Add Pet", onPress: () {
          goToPage(context, AddPetPagePath);
        }, minWidth: 100, height: 50),
        createRoundedCornerRaisedButton("Notifications", onPress: () {
          goToPage(context, NotificationsPath);
        }, minWidth: 100, height: 50),
        createRoundedCornerRaisedButton("Access Information", onPress: () {
          goToPage(context, AccessInfoPath);
        }, minWidth: 100, height: 50),
        createRoundedCornerRaisedButton("Logout", onPress: () async {
          await ServerGateway.instance().logout();
          wipeAllPagesAndGoTo(context, LoginPagePath);
        }, minWidth: 100, height: 50),
      ],
    );
  }

  Widget createButton(String title, void Function() callback) {
    return RaisedButton(
      onPressed: callback,
      child: Text(title),
    );
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
