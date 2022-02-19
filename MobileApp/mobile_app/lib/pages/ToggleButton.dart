

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class ToggleButton extends StatefulWidget
{
  State<StatefulWidget> createState() => ToggleButtonState();
}

class ToggleButtonState extends State<ToggleButton>
{
  bool isChecked = false;

  build(context)
  {
    return Container(
      width: 50,height: 50,
      child: RaisedButton(onPressed: (){
        isChecked = !isChecked;
        setState(() {});
      },child: Container(color: isChecked? Colors.red:Colors.blue,
      ),),
    );
  }
}