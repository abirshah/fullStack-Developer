import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

class Toast extends StatelessWidget
{
  final String message;

  Toast(this.message);

  build(context) =>Directionality(
    textDirection: TextDirection.rtl,
    child: Column(mainAxisAlignment: MainAxisAlignment.end,
      children: <Widget>[
        Dialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8.0),
          ),
          elevation: 0.0,
          backgroundColor: Colors.transparent,
          child: dialogContent(context, message),
        ),
      ],
    ),
  );
}

dialogContent(context, String message) {
  return Center(
    child: Container(
      padding: EdgeInsets.all(10.0),
      margin: EdgeInsets.only(top: 8.0),
      decoration: new BoxDecoration(
        color: Colors.white,
        shape: BoxShape.rectangle,
        borderRadius: BorderRadius.circular(8.0),
        boxShadow: [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 10.0,
            offset: const Offset(0.0, 10.0),
          ),
        ],
      ),
      child: Text(message, style: TextStyle(fontWeight: FontWeight.bold)),
    ),
  );
}


toast(String message,context) => showDialog(context: context,builder: (context)=>Toast(message));