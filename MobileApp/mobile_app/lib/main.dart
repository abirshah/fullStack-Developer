import 'package:flutter/material.dart';
import 'package:mobile_app/router.dart';



void main() {

  runApp(
    MaterialApp(
      onGenerateRoute: router,
      initialRoute: "/",
    )
  );
}
