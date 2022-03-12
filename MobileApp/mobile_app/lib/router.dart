

import 'package:flutter/material.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/pages/AccessInformationPage.dart';
import 'package:mobile_app/pages/AddPetPage.dart';
import 'package:mobile_app/pages/CapturedImagesOrVideosPage.dart';
import 'package:mobile_app/pages/ImageOrVideoPreviewPage.dart';
import 'package:mobile_app/pages/LoginPage.dart';
import 'package:mobile_app/pages/MainMenu.dart';
import 'package:mobile_app/pages/NotificationPage.dart';
import 'package:mobile_app/pages/SettingsPage.dart';
import 'package:mobile_app/pages/SignupPage.dart';
import 'package:mobile_app/pages/SplashPage.dart';

import 'model/dto/CapturedImageOrVideo.dart';

const String SplashPagePath = "/";
const String LoginPagePath = "login";
const String SignUpPagePath = "signup";
const String MainMenuPagePath = "main-menu";
const String SettingsPagePath = "setting";
const String AddPetPagePath = "add-pet";
const String NotificationsPath = "notifications";
const String AccessInfoPath = "access-info";
const String CapturedImagesPath = "captured-images";
const String CapturedVideosPath = "captured-videos";
const String PreviewVideoOrImage = "preview-file";


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

    case AddPetPagePath:
      return _createRoute(AddPetPage());

    case NotificationsPath:
      return _createRoute(NotificationsPage());

    case AccessInfoPath:
      return _createRoute(AccessInformationPage());

    case PreviewVideoOrImage:
      return _createRoute(ImageOrVideoPreviewPage(settings.arguments as CapturedImageOrVideo));


    case CapturedImagesPath:
      return _createRoute(CapturedImagesOrVideosPage(ServerGateway.instance().fetchCapturedImages()));

    case CapturedVideosPath:
      return _createRoute(CapturedImagesOrVideosPage(ServerGateway.instance().fetchCapturedVideos()));

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
