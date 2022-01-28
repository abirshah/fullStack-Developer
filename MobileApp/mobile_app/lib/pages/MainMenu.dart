import 'package:flutter/material.dart';
import 'package:mobile_app/pages/ToggleButton.dart';

class MainMenu extends StatelessWidget {
  String title = "";

  MainMenu(String title) {
    this.title = title;
  }

  build(context) {
    return Scaffold(
      appBar: buildAppBar(),
      body: createBody(),
    );
  }

  Widget createBody()
  {
    return Column(

      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
          createButton("Settings" , (){ print("settings");}),
          createButton("Live Camera",(){print("live camera");}),
        ],),

        createButton("Captured Images",(){}),
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
