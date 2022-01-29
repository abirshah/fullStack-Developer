

import 'package:flutter/material.dart';
import 'package:mobile_app/pages/LoginPage.dart';
import 'package:mobile_app/pages/MainMenu.dart';
import 'package:mobile_app/pages/SettingsPage.dart';
import 'package:mobile_app/pages/SignupPage.dart';
import 'package:mobile_app/pages/SplashPage.dart';

const String SplashPagePath = "/";
const String LoginPagePath = "login";
const String SignUpPagePath = "signup";
const String MainMenuPagePath = "main-menu";
const String SettingsPagePath = "setting";


MaterialPageRoute router(RouteSettings settings)
{
  switch(settings.name)
  {
    case SettingsPagePath:
      return _createRoute(SettingsPage());
    
    case SignUpPagePath:
      return _createRoute(SignupPage());
    
    case SplashPagePath:
      return _createRoute(SplashPage());

    case LoginPagePath:
      return _createRoute(LoginPage());

    case MainMenuPagePath:
      return _createRoute(MainMenu());

    default:
      return _createRoute(Center(child: Text("Unknown Page")));
  }
}

Future goToPage(context,name,{arguments}) => Navigator.pushNamed(context, name,arguments: arguments);

void goToPrevPage(context,{result}) => Navigator.pop(context,result);

void wipeAllPagesAndGoTo(context, path,{args}) =>
    Navigator.pushNamedAndRemoveUntil(context, path, (route) => false,arguments: args);


MaterialPageRoute _createRoute(Widget widget) => MaterialPageRoute(
    builder: (c) => Material(color: Colors.white, child: SafeArea(child: widget)));

void replaceTopPageWith(context, path,{args}) =>
    Navigator.popAndPushNamed(context, path,arguments: args);
