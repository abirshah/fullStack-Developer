



import 'package:flutter/material.dart';

class LoginPage extends StatelessWidget
{

  String text1="";
  String text2="";

  build(context){
    return Scaffold(
      body: Column(
        children: [
          Spacer(flex: 2),
          Text("Automated Pet Door",style: TextStyle(fontSize: 20),),
          Text("XGaurd"),
          Spacer(flex: 1),
          TextField( onChanged: (t){text1=t;},),
          Spacer(flex: 1),
          TextField( onChanged: (t){text2=t;},),
          Spacer(flex: 1),
          RaisedButton(onPressed: (){
            print("$text1  $text2");
            Navigator.pushNamed(context, "page1",arguments: "$text1 $text2");

          },child: Text("Login"),),
          Spacer(flex: 1),
          Text("Don't Have Account ?"),
          Spacer(flex: 1),
          RaisedButton(onPressed: (){},child: Text("Register"),),
          Spacer(flex: 2),
        ],
      ),
    );
  }

}

