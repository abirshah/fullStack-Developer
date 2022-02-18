

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../router.dart';

class StartWidget extends StatelessWidget
{
  build(context) => MaterialApp(
      debugShowCheckedModeBanner: false,
      onGenerateRoute: router,
      initialRoute: SplashPagePath,
      color: Colors.white,
      theme: ThemeData(
        buttonTheme: ButtonThemeData(
            materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
            minWidth: 0,
            height: 0,
            padding: EdgeInsets.zero),
        primarySwatch: Colors.blue,
      ));
}