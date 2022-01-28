

import 'package:flutter/material.dart';
import 'package:mobile_app/pages/LoginPage.dart';
import 'package:mobile_app/pages/MainMenu.dart';

MaterialPageRoute router(RouteSettings settings)
{
  if(settings.name=="/")
    return MaterialPageRoute(builder: (context)=>LoginPage());


  //if(settings.name=="page1")
  return MaterialPageRoute(builder: (context)=>MainMenu(settings.arguments as String));
}

